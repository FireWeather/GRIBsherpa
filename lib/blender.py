__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import pygrib
import psycopg2
import os


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

    ## Gets the msg from grib.
    # @return Error (OSError or ValueError) if grib not found or msg doesn't exist in grib
    # @return List of messages found
    def getMessage(self, msg, grib):
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
                    dict[field] = "NOT FOUND" #todo change this depending on database standards for empty fields
        return dict






