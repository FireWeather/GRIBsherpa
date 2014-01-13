#! /usr/bin/env python3

# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import sys
sys.path.append('/grib')

from lib.database import Database

db_name = "stormking"
user = "vagrant"
password = "vagrant"

database = Database()

database.setup_connection(db_name, user, pword)
database.open_connection()
database.close_connection()