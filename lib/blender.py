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
                print("Error: {} is not a file.".format(grib))
                return

    def message_names(self):
        if self.grib is None:
            print("No grib file is specified so nothing to show.")
        else:
            try:
                gf = pygrib.open(grib)
            except Exception as error:
                print("Error type: {0} when opening gribfile".format(error))
            #gf = self.__open(self.grib, test)    
            #test.seek(0)
            for item in gf:
                print(item.name)
            #pygrib.close(self.grib)

    def message_items(self, message_name):
        if self.grib is None:
            print("No grib file is specified so nothing to show.")
        else:
            gf = self.__open(self.grib)
            gf.seek(0)
            msg = gf.select(name="{0}".format(message_name))
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

