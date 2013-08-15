# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

# This module is for holding any global variables that need to be set/used.
# It was created initially to configure and instantiate the global "logger" so that all
# modules could use logging functionality by simply including this module.  This
# allows the use of logging without necessarily having to be the
# "__main__" module (this is where the examples use and initialize the logger
# typically).

import logging
import os
import datetime


# ---------------------------- Logging global config ------------------------
# In subsequent modules the logger will be used with the following call:
# > globe.log.info()
# > globe.log.warn()
# > globe.log.debug()

# This sets the initial logging functionality.  The first call through this sets the vars
# the second + calls are essentially no ops as per the documentation.

# verify log directory
log_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'log/')
if not os.path.exists(log_dir):
    print("Error in logger::createLogFile - " + log_dir + " does not exist.")

# name logfile ...log/todaysdate
logFile = log_dir + str(datetime.date.today()) + ".log"

logging.basicConfig(filename=logFile, level=logging.INFO)

log = logging


