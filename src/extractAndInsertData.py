#!/usr/bin/python3

import sys
sys.path.append("..")

import lib.blender as blender
import lib.logger as log
import lib.record_keeper as rc
import time


# Create a lambda that we can call later for timing of procedures (converting to millis)
current_time_millis = lambda: int(round(time.time() * 1000))


#TODO: include messages of interest here?  Or DB query for them here?

# --------------------------- Data Extraction -----------------------------
t1 = current_time_millis()

grib = blender.Blender("../test/grib.grib2")

mrData = grib.modelRun()
fhData = grib.forecastHour()
metParams = grib.metParams("Geopotential Height")
values = grib.values("Geopotential Height")

log.write.info("In extractAndInsertData: data extracted from GRIB")

t2 = current_time_millis()
print("Data extraction complete in: " + str(t2 - t1) + "millis")

# ------------------------ Data Formatting for DB ------------------------

# --------------------------- Data Insertion --------------------------
t1 = current_time_millis()

db = rc.RecordKeeper("dbname=stormking user=vagrant password=vagrant")
db.openDbConnection()


# 1. Insert model run info (this should go through unless this script is being re-run for the same data)
db.generalInsert('model_run', ['model_run_date', 'model_run_time'], [mrData["date"], mrData["hour"]])

# 2. Insert forecast hour info (may or may not go through as after a while we should always have the same forecast hrs)
db.generalInsert('forecast_hour', ['forecast_hour'], [fhData["hour"]])




# 3. Insert into linking table for model_run and forecast_hour - this should always work (unless re-run as in #1)
# NOTE: This requires a query to get the primary key from model_run and forecast_hour

# Get the foreign key from model_run
mrPK = db.sql("SELECT model_run_pkey FROM model_run WHERE model_run_date = " + mrData['date'] + \
              " AND model_run_time = " + mrData['hour'] + ";")

# Get the foreign key from forecast_hour
fhPK = db.sql("SELECT forecast_hour_pkey FROM forecast_hour WHERE forecast_hour = " + fhData['hour'] + ";")

# The above should return an array of tuples with 1 tuple and 1 val: ( ex. [(1, )] )
# Since we're always querying one value, we should be able to trim the result from above the same way every time.
db.generalInsert('model_forecast_relation', ['model_run_pkey', 'forecast_hour_pkey'], [mrPK[0][0], fhPK[0][0]])




# 4. Insert met params.  Right now this always works, just inserts duplicates.  At some point this will, like #2 & #3,
# not a actually insert as we will be trying to put in duplicate values. In that case it will just log that it didn't
# enter anything because of a duplicate value error.
for key in metParams.keys():
    paramsPerLevel = metParams[key]
    db.generalInsert('met_param', ['attribute', 'attribute_unit', 'level', 'level_unit'],
                     [paramsPerLevel['attribute'], paramsPerLevel['attribute_unit'],
                      paramsPerLevel['level'], paramsPerLevel['level_unit']])




# 5. Insert values.  NOTE: This requires queries to get the primary keys for model_forecast_relation and
# met_param and model_grid_points.

# Blender.values returns a dict of { level:values }. Therefore:
# A. model_forecast_relation foreign key will be the same
# B. met_param foreign key will change each level so re-query for each level in values.

# Get foreign key from model_forecast_relation. This won't change as we iterate through values/level (so get once).
mfrPK = db.sql("SELECT model_forecast_relation_pkey FROM model_forecast_relation \
               WHERE model_run_pkey='" + str(mrPK[0][0]) + "' AND forecast_hour_pkey='" + str(fhPK[0][0]) + "';")
if mfrPK is None:
    log.write.error("In extractAndInsertData: getting None from mfrPK")

# The metParams and values change for each level so get these on a per level basis.
# NOTE: key for "values" dict is same as key for "metParams" dict, namely "level"
for key in values.keys():
    # get the metParams info for the "level" of values we're looking at
    paramsAtLevel = metParams[key]
    valsAtLevel = values[key]

    # Get the foreign key from met_param
    mpPK = db.sql("SELECT met_param_pkey FROM met_param WHERE level=" + paramsAtLevel['level'] + \
              " AND attribute=" + paramsAtLevel['attribute'] + ";")
    if mpPK is None:
        log.write.error("In extractAndInsertData: getting None from mpPK")

    # Iterate through values, entering each one with the same foreign keys
    for val in valsAtLevel:
        #TODO: fix hardcoded "location" value once postGIS is fixed
        db.generalInsert('met_data', ['value', 'met_param_pkey', 'model_grid_points_pkey', 'model_forecast_relation_pkey'],
                         [val, mpPK[0][0], 11, mfrPK[0][0]])

t2 = current_time_millis()
print("Data Insertion complete in: " + str(t2 - t1) + "millis/" + str((t2 - t1)/1000) + "seconds")

db.closeDbConnection()

