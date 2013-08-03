#!/usr/bin/python3.3
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

# adds project root directory to PYTHONPATH needed for the next import statement

from sys import path
path.append('..')

from lib.fetcher import Fetcher

spider = Fetcher()
spider.download_param_grib_range('gfs', 2013080300, 00, 240, 12)
