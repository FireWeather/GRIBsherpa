#!/usr/bin/python3

# import os, sys, inspect
# # realpath() with make your script run, even if you symlink it :)
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
# if cmd_folder not in sys.path:
#     sys.path.insert(0, cmd_folder)

import lib.blender as blender
import lib.logger as log
import lib.record_keeper as rc


# def script():
#TODO: include messages of interest here?  Or DB query for them here?

# --------------------- Data Extraction ------------------------
grib = blender.Blender("../test/grib.grib2")

mrData = grib.modelRun()
fhData = grib.forecastHour()
metParams = grib.metParams("Geopotential Height")
values = grib.values("Geopotential Height")

log.write.info("In extractAndInsertData: data extracted from GRIB")

# --------------------- Data Formatting for DB ----------------------

# --------------------- Data Insertion --------------------
db = rc.RecordKeeper("dbname=stormking user=susherpa password=susherpa")

# Insert model run info
db.generalInsert('model_run', ['model_run_date', 'model_run_time'], [mrData["date"], mrData["hour"]])

# Insert forecast hour info
db.generalInsert('forecast_hour', ['forecast_hour'], [fhData["hour"]])

# if __name__ == "__main__":
#     script()
