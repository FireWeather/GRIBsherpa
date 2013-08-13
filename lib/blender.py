# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import pygrib
import psycopg2
import os
import numpy
import csv


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


    # todo: make sure you understand how this works (numpy functionality)
    ## This looks for the closest coordinates to what we are looking for and, once found
    #  gets corresponding data fields.
    #def getValues(self, lat, lon, message):
    #    # Get the coordinates closest to what we're looking for
    #    cords = [self.__findNearest(message['distinctLatitudes'], lat),
    #            self.__findNearest(message['distinctLongitudes'], lon)]
    #    val = message.values[cords[0], cords[1]]
    #    return {'lat': cords[0], 'lon': cords[1], 'val': val, 'name': message['name'], 'val_units': message['units'],
    #            'level': message['level'], 'level_units': message['typeOfLevel'], 'year': message['year'],
    #            'month': message['month'], 'day': message['day'], 'hour': message['hour']}

    def getValues(self, lat, lon, message):
        return self.__interpolate(lat, lon, message)



    # ----------------------------------- Private ------------------------------------

    # -------------------------------- Test Doubles ----------------------------------
    # The following methods are test dummies for verifying/testing private methods.
    #  They should be commented out (as should their tests) once debugging is finalized.
    # todo: comment these out
    def formLatLonPairs(self, numpyLats, numpyLons):
        return self.__formLatLonPairs(numpyLats, numpyLons)

    # ----------------------------- End Test Doubles ---------------------------------


    ## This solution for finding the nearest value in a numpy array came from stackoverflow.
    #  http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    #def __findNearest(self, array, value):
    #   index = (numpy.abs(array-value)).argmin()
    #    return array[index]

    def __interpolate(self, lat, lon, message):
        # Form array of tuples of lat lon pairs
        points = self.__formLatLonPairs(message["latitudes"], message["longitudes"])
        values = message["values"]
        xi = [lat, lon]


    ## Takes two numpy arrays and combines them into tuples
    #  @return    array of tuples corresponding to lat lon pairs
    def __formLatLonPairs(self, numpyLats, numpyLons):
        latLons = []
        index = 0
        for item in numpyLats:
            newPair = [item, numpyLons[index]]
            index += 1
            latLons.append(newPair)
        return latLons


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

    ## Import the lat/lon values we are looking for as specified in CSV files
    def __importCsvLatLon(self, csv_file):
        values = []
        try:
            f = open(csv, 'r')
        except FileNotFoundError as err:
            print("Error in url_parser::__importCsvLatLon - csv file not found")
            return
        reader = csv.reader(f)
        for row in reader:
            values.append([row[1], row[2]])
        return values


    ## This wraps Pygrib.open in a try catch block.
    def __openGrib(self, file):
        try:
            f = pygrib.open(file)
        except FileNotFoundError as err:
            print("Error in blender::__openGrib - File Not found")
            return
        return f








