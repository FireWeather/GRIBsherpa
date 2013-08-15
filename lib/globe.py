# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import logging
import os
import datetime


# ---------------------------- Logging global config ------------------------
# In subsequent modules the logger will be used with the following call:
# > global.logging.info()
# > global.logging.warn()
# > global.logging.debug()

# This sets the initial logging functionality.  The first call through this sets the vars
# the second + calls are essentially no ops as per the documentation.

# verify log directory
log_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'log/')
if not os.path.exists(log_dir):
    print("Error in logger::createLogFile - " + log_dir + " does not exist.")

# name logfile ...log/todaysdate
logFile = log_dir + str(datetime.date.today())

logging.basicConfig(filename=logFile, level=logging.INFO)

log = logging


