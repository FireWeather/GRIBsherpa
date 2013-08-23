# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------
# This is the logging module.  When using the Python "logging" class, certain variables
# are typically set in "main" that configure the "logger" (I believe it's a singleton). Then
# the logger is available to any modules that "import logging".  Since we don't have a main
# yet but want the logger available everywhere, I've created and set the defaults here. Now
# all you have to do is import this module and the logger will be available through:
#
# Usage: (in a module you want to have logging in)
#   import lib.logger
#   (In the init method for the class you want to use logging in, define "self.log = lib.logger")
#   self.log.write("")          <-- this defaults to the default: "info"
#   self.log.write.warning("")
#   self.log.write.error("")
#   self.log.write.debug("")


import logging
import os
import datetime


# verify log directory
log_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'log/')
if not os.path.exists(log_dir):
    print("Error in logger::createLogFile - " + log_dir + " does not exist.")

# Create a logfile using today's date
logFile = log_dir + str(datetime.date.today()) + ".log"

# Tell logging what it's file is and what it's default level is
logging.basicConfig(filename=logFile, level=logging.INFO)

# Create an alias so we can call it in other modules.
write = logging


