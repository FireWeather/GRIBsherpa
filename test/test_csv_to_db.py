# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

from sys import path
path.append('.')
from lib.record_keeper import RecordKeeper
from lib.csv_data_extraction import CsvDataExtraction

cde = CsvDataExtraction('data/regions.csv')
regionDict = cde.getCSVDict()
cde.displayCSVDict()

rc = RecordKeeper("dbname=stormking user=susherpa password=susherpa")
rc.openDbConnection()
rc.closeDbConnection()

