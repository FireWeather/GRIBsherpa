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
    MOI = ['Best (4-layer) lifted index', 'Convective available potential energy', 'Geopotential Height', 'Precipital water', 'Surface lifted index', 'Temperature', 'Relative humidity', 'Surface pressure',  'U component of wind', 'V component of wind', 'Wind speed']


    ## "Fields of Interest" These are the fields contained within the messages (above) that we want to capture.
    # Note that some of these fields (latitudes for example) will contain multiple values.
    FOI = ['name', 'level', 'values', 'units', 'latitudes', 'longitudes', 'distinctLongitudes', 'distinctLatitudes']

    ## Takes a path to the grib file to work with.  Tries to open it for subsequent work.
    #  currentMsg is the message type that is currently being "worked" with.
    def __init__(self, pathToGrib):
        self.grib = self.__openGrib(pathToGrib)

    ## Returns the date and time of the model run for the first msg in the grib (they should all be the same).
    #  Returns date and hour in format needed for SQL conversion (to date and time with single quotes)
    def modelRun(self):
        firstMsg = self.grib[1]
        date = "'" + str(firstMsg.year) + "-" + self.__formatDate(firstMsg.month) + "-" + self.__formatDate(firstMsg.day) + "'"
        hour = "'" + self.__formatTime(firstMsg.dataTime) + "'"
        return {"date": date, "hour": hour}

    ## Returns the forecast hour for the first msg in the grib (they should all be the same).
    def forecastHour(self):
        firstMsg = self.grib[1]
        return {"hour": "'" + str(firstMsg.forecastTime) + " hours'"}

    ## Finds the first matching msgType in the grib and returns in order: attribute, attribute_unit, level, level_unit
    # TODO: figure out if pressureUnits is right param and if it's ok to return vals for the first msg of msgType (ie. is the first indicitive of the rest)
    def metParams(self, msgType):
        toReturn = {}
        msgs = self.__getMessage(msgType, self.grib)
        for msg in msgs:
            toReturn[msg.level] = {"attribute": "'" + msg.name + "'", "attribute_unit": "'" + msg.units + "'",
                                   "level": "'" + str(msg.level) + "'", "level_unit": "'" + msg.pressureUnits + "'"}
        return toReturn

    ## Get's all (0...N) of specified msgType in grib and returns a dictionary of "<level> : <1darray of values>"
    #  TODO: (eventually) modify this to return interpolated values vs. all values (which it's doing now)
    def values(self, msgType):
        toReturn = {}
        msgs = self.__getMessage(msgType, self.grib)
        for msg in msgs:
            # Using Numpy ndarray method
            toReturn[msg.level] = msg.values.flatten().tolist()
        return toReturn



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
    ## Formats single digits to be two digit format which Postgres can convert (SQL standard).
    def __formatDate(self, num):
        if num == 0:
            return "00"
        elif num < 10:
            return "0" + str(num)
        else:
            return str(num)

    ## Formats basic time in "int" to time format Postgres can convert (SQL standard).
    def __formatTime(self, time):
        t = str(time)
        if time == 0:
            return "00:00:00"
        elif time < 1000:
            return "0" + t[0] + ":00:00"
        else:
            return t[0:2] + ":00:00"

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
        # This allows passing in of open grib (and therefore specific msg). This is for simplicity in grad project...
        if type(file) == pygrib.open:
            return file
        try:
            f = pygrib.open(file)
        except FileNotFoundError as err:
            log.write.error("Error in blender::__openGrib - Grib file not found")
            raise err
        return f






