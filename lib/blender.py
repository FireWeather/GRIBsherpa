# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import urllib.error
import pygrib
import psycopg2
import os
import math
import numpy
import scipy.interpolate
import lib.logger as log


## This class wraps pygrib functionality and breaks data down in a way that can then be stored in the database.
# Typical workflow includes:
# 1. Search a grib file for a message(s) with "getMessage()"
# 2. Retrieve fields from that message either by grabbing all of them OR by getting those specified in a list
# 3. Store in database
class Blender(object):


    ## "Message of Interest" These are the messages within the grib that we care about.
    # These will each have many key/value pairs. The message format matches exactly the grib format.
    # Note: for queries containing multiple heights, there will be several repeated (but different) messages for each height
    # MP: Not finding -- precipital water -- its listing below is a best guess at the Message name/format.
    MOI = ['Best (4-layer) lifted index', 'Convective available potential energy', 'Geopotential Height', 'Precipital water', 'Surface lifted index', 'Temperature', 'Realative humidity', 'Surface pressure',  'U component of wind', 'V component of wind', 'Wind speed']


    ## "Fields of Interest" These are the fields contained within the messages (above) that we want to capture.
    # Note that some of these fields (latitudes for example) will contain multiple values.
    FOI = ['name', 'level', 'values', 'units', 'latitudes', 'longitudes', 'distinctLongitudes', 'distinctLatitudes']


    # TODO: clean up comments
    ## This is the work horse of the blender class.  It searches the grib for matching messages and returns a <??>
    #  of all data found for the matching fields.  If the msgs and fields params are left as None, the above
    #  hardcoded values will be used (MOI, FOI)
    #  @param msgs      The messages to look for. Type: Array
    #  @param fields    The fields to return for each message. Type: Array
    #  @param grib      The grib file to use. Type: grib
    #  @return          Returns a <type> of all data found
    #
    # { "Geopotential Height" : [
    #                             { level : 500, units : "mbar", "120, 95" : 243, "120, 94" : 243, "120, 93" : 243, ... },
    #                             { level : 550, units : "mbar", "120, 95" : 243, "120, 94" : 243, "120, 93" : 243, ... },
    #                           ],
    #   "Precipital Water"    : [
    #                             { level : ..... }
    #                           ]
    # }
    #
    def getSpecificData(self, gribPath, latLons, msgs=None, fields=None):
        toReturn = {}
        gribMsgsFound = []
        fp = self.__openGrib(gribPath)

        # check if nothing passed in and conditionally set params
        if msgs is None:
            msgs = self.MOI
        if fields is None:
            fields = self.FOI

        # Find all matching messages (safety check to ensure messages we're trying to find actually exist)
        # ValueError appended here if message isn't found in __getMessage function.
        # This returns a 2d "list of lists"
        for str in msgs:
            gribMsgsFound.append( self.__getMessage(str, fp) )

        # For each array of matching grib messages (1..*)
        for gribMsgs in gribMsgsFound:
            if type(gribMsgs) != ValueError:
                # use the first name of 1..* in toReturn[name] as all names should all be the same
                toReturn[gribMsgs[0].name] = self.__parseGribMsg(gribMsgs, latLons)

        # At this point, all data for each message type should be organized in toReturn
        return toReturn



    ## Returns a list of all matching messages found. Msgs can either be a
    #  single message type (ex. "Temperature") or it can be a list of messages
    #  (ex. ["Temperature", "Geopotential Height",...])
    #  @param msgs    single item (string) or array
    #  @return        returns an array of matches
    def getMessages(self, msgs, grib):
        fp = self.__openGrib(grib)
        toReturn = []
        if type(msgs) == list:
            for msg in msgs:
                matches = self.__getMessage(msg, grib)
                for match in matches:
                    toReturn.append(match)
            return toReturn
        else:
            return self.__getMessage(msgs, grib)


    # todo: depreciate this
    ## Breaks down msg (pygrib mesage) into a dictionary. Will return all fields
    # if list is not specified else will try to return fields specified in list.
    # @param msg pygrib message
    # @param list fields you want data for
    # @return Dictionary of data for message
    def getMessageFields(self, msg, list=None):
        dict = {}
        if list is None:
            for key in msg.keys():
                val = msg[key]
                dict[key] = val
        else:
            for field in list:
                if field in msg.keys():
                    dict[field] = msg[field]
                else:
                    dict[field] = "NOT FOUND"
        return dict


    ## This returns data for a specific point in a grid.  If data is requested for a point that doesn't exist
    #  within the message then interpolation will be performed.
    def getValuesAtPoint(self, lat, lon, message, function):
        points = self.formLatLonPairs(message["latitudes"], message["longitudes"])
        lats, lons = message["latitudes"], message["longitudes"]
        values = message["values"]

        # Check if the lat, lon we want data for is actually in the message, if not, continue below
        for point in points:
            if point == [lat, lon]:
                return message["values"][points.index(point)]

        # Not found so return interpolation
        return function(lat, lon, message)


    def iRectSphereBivariateSpline(self, lat, lon, message):
        lats, lons, vals = self.getScipyValues(message)
        interp = scipy.interpolate.RectSphereBivariateSpline(lats, lons, vals)
        return interp[lat, lon]

    def iRectBivariateSpline(self, lat, lon, message):
        lats, lons, vals = self.getScipyValues(message)
        interp = scipy.interpolate.RectBivariateSpline(lats, lons, vals)
        return interp[lat, lon]

    def iNoInterp(self, lat, lon, message):
        vals = message["values"]
        return vals[lat][lon]

    ## Returns values (sorted lats, sorted lons, value pairs) in required format of Scipy.
    def getScipyValues(self, message):
        # Loop through array of [lat1, lon1, value1, ...] building mapped structure. Increment each
        # index (lat, lon, val) by 3
        lat, lon, val = 0, 1, 2
        mapped_lats, mapped_lons = {}, {}
        latLonValues = message["latLonValues"]
        while val < latLonValues.size:
            mapped_lats[latLonValues[lat]] = latLonValues[val]
            mapped_lons[latLonValues[lon]] = latLonValues[val]
            lat += 3
            lon += 3
            val += 3
        # Loop through sorted lat/lon arrays building 2d array of vals correponding to lat/lon
        # lats = [lat0, lat1, ...] lons = [lon0, lon1, ...] mapped_vals = [lat0.val, lon0.val]
        lats = numpy.sort(message["latitudes"], None, 'mergesort')
        lons = numpy.sort(message["longitudes"], None, 'mergesort')
        index = 0
        mapped_vals = []
        while index < (lats.size - 1):
            mapped_vals.append([mapped_lats[lats[index]], mapped_lons[lons[index]]])
            index += 1

        # Todo: rectSphereBiv takes radians from 0-Pi, pair on finishing the below conversion
        # numpy factory "vectorize"
        convertToRadians = numpy.vectorize(self.__convertToRadians)
        l = convertToRadians(lats[:10])

        return lats, lons, mapped_vals


    ## Takes two numpy arrays and combines them into tuples
    #  @return    array of tuples corresponding to lat lon pairs
    def formLatLonPairs(self, numpyLats, numpyLons):
        latLons = []
        index = 0
        for item in numpyLats:
            newPair = [item, numpyLons[index]]
            index += 1
            latLons.append(newPair)
        return latLons


# ---------------------------------------------- PRIVATE -------------------------------------------------
    ## Gets the message specified from grib.
    # Note the grib should already by open when passing in.
    # @return Error (OSError or ValueError) if grib not found or msg doesn't exist in grib
    # @return **List** of messages found
    def __getMessage(self, message, openGrib):
        try:
            msg = openGrib.select(name="{0}".format(message))
        except ValueError as err:
            log.write.error(err)
            return err
        return msg

    ## Returns a radian representation of the degree number passed in.
    def __convertToRadians(self, degree_num):
        return math.radians(degree_num)

    ## This wraps Pygrib.open in a try catch block.
    def __openGrib(self, file):
        try:
            f = pygrib.open(file)
        except FileNotFoundError as err:
            log.write.error("Error in blender::__openGrib - Grib file not found")
            raise err
        return f

    ## Parses data out of grib messages.
    #  @return  Array of dictionaries, 1 for each gribMsg in gribMsgs corresponding to level
    def __parseGribMsg(self, gribMsgs, latLons):
        toReturn = []
        levelData = {}

        for msg in gribMsgs:
            levelData["level"] = msg.level
            levelData["units"] = msg.units

            # TODO: figure out how to append to dataFound ' latLon : value ' Not sure what latLon is. Eventually this step will involve interpolated data
            #for loc in latLons:
            #    dataFound[loc] = gribMsg["values"][##somepoint##]

            toReturn.append(levelData)
            levelData = {}

        return toReturn




