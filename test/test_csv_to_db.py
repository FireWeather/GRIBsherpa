#!/usr/bin/python3.3
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------
import os
import re
from sys import path
path.append('.')
from lib.record_keeper import RecordKeeper
from lib.csv_data_extraction import CsvDataExtraction

pathToGridPoints = 'data/latlon/csv/'
pathToRegionsData = 'data/regions.csv'

cde = CsvDataExtraction(pathToRegionsData)

reSearch = '(^[A-Z]+)(_)([a-z]*)(_)*(grid\.csv$)'


rc = RecordKeeper("dbname=stormking user=susherpa password=susherpa")
rc.openDbConnection()
rc.insertRegionData(cde)

if os.path.isdir(pathToGridPoints):
    for filename in os.listdir(pathToGridPoints):
        cde = CsvDataExtraction(pathToGridPoints + filename)
        match = re.search(reSearch, filename)
        print(filename)
        if match.group(4) is None:
            # print(match.group(1))
            rc.insertGeoData(cde, match.group(1))
        else:
            # print(match.group(1) + ':' + match.group(3))
            rc.insertGeoData(cde, match.group(1), match.group(3))


# rc = RecordKeeper("dbname=stormking user=susherpa password=susherpa")
# rc.openDbConnection()
#
# rc.insertRegionData(cde)
#
# rc.closeDbConnection()