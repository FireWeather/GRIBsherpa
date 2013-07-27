#!/usr/bin/python3.3

# adds project root directory to PYTHONPATH needed for the next import statement

# TODO add copyright via Matt's script
from sys import path
path.append('..')

from lib.grib_spyder import GribSpyder

spider = GribSpyder()
spider.download_param_grib_range('gfs', 2013072700, 00, 240, 12)
