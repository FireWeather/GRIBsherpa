# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import pygrib
import psycopg2
import os
import math
import numpy
import scipy.interpolate


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


    ## Returns a list of all matching messages found. Msgs can either be a
    #  single message type (ex. "Temperature") or it can be a list of messages
    #  (ex. ["Temperature", "Geopotential Height",...])
    #  @param msgs    single item (string) or array
    #  @return        returns an array of matches
    def getMessages(self, msgs, grib):
        toReturn = []
        if type(msgs) == list:
            for msg in msgs:
                matches = self.getMessage(msg, grib)
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
        print(lats[:10])
        print(lons[:10])
        l = convertToRadians(lats[:10])
        print(l)
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
    ## Gets the msg from grib.
    # @return Error (OSError or ValueError) if grib not found or msg doesn't exist in grib
    # @return List of messages found
    def __getMessage(self, msg, grib):
        try:
            f = pygrib.open(grib)
        except OSError as err:
            print(err)
            return err
        try:
            msgs = f.select(name="{0}".format(msg))
        except ValueError as err:
            print(err)
            return err
        return msgs

    ## Returns a radian representation of the degree number passed in.
    def __convertToRadians(self, degree_num):
        return math.radians(degree_num)

    ## This wraps Pygrib.open in a try catch block.
    def __openGrib(self, file):
        try:
            f = pygrib.open(file)
        except FileNotFoundError as err:
            print("Error in blender::__openGrib - File Not found")
            return
        return f







