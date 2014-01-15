#! /usr/bin/env python3

# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------


import os
import csv
import sys
sys.path.append('/grib')
from lib.database import Database

db_name = "stormking"
user = "vagrant"
password = "vagrant"

csv_file = "some name here"

database = Database()

database.setup_connection(db_name, user, password)
database.open_connection()



database.populate_simple(table_name, csv_file)

database.close_connection()


def csv_extract(filename):
    if not os.path.isfile(filename):
        print('file \'' + filename + '\' does not exist')
        exit(1)
    temp = open(filename)
    return csv.DictReader(temp)