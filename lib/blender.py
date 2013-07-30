__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import pygrib
import os


class Blender(object):

    ## "Message of Interest" These are the messages within the grib that we care about.
    # These will each have many key/value pairs. The message format matches exactly the grib format.
    # Note: for queries containing multiple heights, there will be several repeated (but different) messages for each height
    # MP: Not finding -- precipital water -- its listing below is a best guess at the Message name/format.
    MOI = [ 'Best (4-layer) lifted index', 'Convective available potential energy', 'Geopotential Height', 'Precipital water', 'Surface lifted index', 'Temperature', 'Realative humidity', 'Surface pressure',  'U component of wind', 'V component of wind', 'Wind speed' ]

    def __init__(self, path=None):
        self._grib = path

    @property
    def grib(self):
        return self._grib

    @grib.setter
    def grib(self, path):
        if path is None:
            self._grib = None
            return
        else:
            if os.path.isfile(path):
                self._grib = path
                return
            else:
                print("Error: {} is not a file.".format(path))
                return

    def messages(self):
        if self.grib is None:
            print("No grib file is specified so nothing to show.")
        else:
            try:
                gf = pygrib.open(self._grib)
            except Exception as error:
                print("Error type: {0} when opening gribfile".format(error))
                return
            # reset incase calling again
            gf.seek(0)
            for item in gf:
                print(item.name)
            #pygrib.close(self.grib)

    def message_details(self, message_name):
        if self.grib is None:
            print("No grib file is specified so nothing to show.")
        else:
            gf = self.__open(self._grib)
            gf.seek(0)
            try:
                msg = gf.select(name="{0}".format(message_name))
            except Exception as error:
                print("Error during select: {0}".format(error))
                return
            for i in msg:
                print(i)



    # ------------------------- Private ----------------------------
    
    ## Opens the grib file passed in
    # @return Returns open pygrib file
    def __open(self, grib):
        try:
            gf = pygrib.open(grib)
        except Exception as error:
            print("Error type: {0} when opening gribfile".format(error))
            return
        return gf

