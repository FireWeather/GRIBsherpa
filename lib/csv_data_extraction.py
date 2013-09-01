# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------
import os
import csv


class CsvDataExtraction(object):

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(filename):
            print('file \'' + filename +'\' does not exist')
            exit(1)
        temp = open(self.filename)
        self.dict = csv.DictReader(temp)
        # temp.close()

    def getCSVDict(self):
        return self.dict