#!/usr/bin/python3

import sys
sys.path.append("..")

import lib.logger as log
import lib.record_keeper as rc
import lib.csv_data_extraction as cde


# Prep db connection
db = rc.RecordKeeper("dbname=stormking user=vagrant password=vagrant")
db.openDbConnection()


# ------------------------------------- Insert Region and Geo Data -------------------------------------
# Get csv data dictionaries for regions and geo data
regionDict = cde.CsvDataExtraction('/grib/data/regions.csv')
geoDict = cde.CsvDataExtraction('/grib/data/latlon/csv/NWCC_lg_grid.csv')

# Insert region data
db.insertRegionData(regionDict)

# Insert grid points
db.insertGeoDataDummy(geoDict, "'NWCC'")


# ------------------------------- Insert Default Msgs/Fields of Interest --------------------------------
# TODO: figure out where we want this pulled in from (a config file?) or if this location is fine.

# "Message of Interest" These are the messages within the grib that we care about.
# The message format matches exactly the grib format.
MOI = ['Best (4-layer) lifted index', 'Convective available potential energy', 'Geopotential Height', 'Precipital water', 'Surface lifted index', 'Temperature', 'Relative humidity', 'Surface pressure', 'U component of wind', 'V component of wind', 'Wind speed']

for type in MOI:
    db.generalInsert('message_types', ['name'], [type])


db.closeDbConnection()
