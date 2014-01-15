#! /usr/bin/env python3

# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import re
import os
import sys
sys.path.append('/grib')
from lib.database import Database
from lib.csv_data_extraction import CsvDataExtraction

class CoreData:

    def __init__(self, simple=None, aggregate=None):
        self.path_to_simple_dir = "./data/simple/"
        self.path_to_aggregate_dir = "./data/aggregate/"

    def populate_simple(self):
        db_name = "stormking"
        user = "vagrant"
        password = "vagrant"
        db = Database(db_name, user, password)

        for file in os.listdir(self.path_to_simple_dir):

            name_of_table = os.path.splitext(file)[0] #gathers only the name of the file not the extension
            full_path = self.path_to_simple_dir + file

            fh = open(full_path)
            full_table_name = "development." + name_of_table
            headers = fh.readline()
            headers = headers.strip('\n')

            headers = headers.split(',')
            # # print(headers)
            # columns = ""
            # for t in headers:
            #     columns += '\'' + t + '\', '
                # print(columns)
            # columns = columns[:-2]
            # print(columns)

            db.populate_simple(full_table_name, fh, headers)
            fh.close()

        db.close_connection()