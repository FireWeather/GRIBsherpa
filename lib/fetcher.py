# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import urllib.request
import urllib.error
import lib.url_parser
import lib.logger as log
import os
import re


## Fetcher is a GRIB specific class that assists with downloading GRIB files.
# Initialization variables are optional and if used should be passed in using a dictionary with
# keys specifying the variable name that you want to initialize.
#
# Fetcher expects the "tmp" project directory to exist and will download files to that location
# unless a different location ("store_loc") is specified at initialization.
# This class has dependencies on two other classes:
# 1. GribHtmlParser (html_parser.py)
# 2. UrlParser (defined below)
class Fetcher(object):


    ## @param args A dictionary of initialization params
    def __init__(self, args=None):
        self.url_parser = lib.url_parser.UrlParser()
        self.store_loc = self.__default_args("store_loc", args)


    ## Downloads multiple grib files as specified by the parameters.
    # @param model_type:          String describing model type (ex. 'nam', 'gfs', etc.)
    # @param model_run_dateHour:  integer describing dateHour (YYYYMMDDHH, ex. 2013070100)
    # @param fh_start:            integer describing the hour to start 00, 03, 06, etc. (or greater)
    # @param fh_end:              integer describing the hour to end (inclusive)
    # @param increment:           integer describing how to increment the forecast hours being downloaded
    # @param degree:              float specifying the degree to use (with 'gfs' files) - not used when downloading 'nam' files
    # NOTE: the increment must correspond to an actual increment provided by NOAA, otherwise
    # errors will be thrown. If this happens the method will continue trying to downloading
    # any files that it find matches for until fh_end has been reached.
    def download_param_grib_range(self, model_type, model_run_dateHour, fh_start, fh_end, increment, degree=None):
        start = fh_start
        end = fh_end
        inc = increment
        print("Downloading GRIB range for model run type: " + model_type + "\n" +
              "............dateHour = " + str(model_run_dateHour) + "\n" +
              "............start = " + str(start) + "\n" +
              "............end = " + str(end) + "\n" +
              "............increment = " + str(inc) + "\n" +
              "............degree = " + str(degree))
        while start <= end:
            to_download = self.url_parser.build_download_url(model_type, model_run_dateHour, start, degree)
            file_name = str(model_run_dateHour)[:4] + "_" + str(model_run_dateHour)[4:6] + "_" + str(model_run_dateHour)[6:8] + "_" + str(model_run_dateHour)[8:] + "_" + self.__three_hr_fh(start) + ".grib"   
            self.__download(to_download, file_name)
            start += inc


    # ------------------------------------------ Private -------------------------------------------------------

    def __build_link(self, url, link):
        return url + link


    ## Builds a path to 'tmp' which should be in project tree/directory
    # NOTE: this expects tmp to exist one dir above location of this file, this
    # may need to be more flexible in the future...
    def __build_path_to_tmp(self):
        tmp_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'tmp/')
        assert(os.path.exists(tmp_dir))
        return tmp_dir


    ## This is used to return meaningful default args in __init__. It contains particular
    #  functionality for making sure there is a default store location for downloads. Otherwise
    #  it returns type in args (if it exists) or returns none.
    def __default_args(self, type, args):
        if args is None or not args.contains(type):
            if type == "store_loc":
                return self.__build_path_to_tmp()
            else:
                return None
        return args[type]


    # Actual download of file.
    # 1. expects there to be a temp directory
    # 2. builds storage file path based on tmp path and the url being downloaded (or file_name passed in)
    # 3. attempts to download file
    # 4. Logs success or failure and prints to console upon success (to aid in visual aspect of tests)
    def __download(self, url, file_name=None):
        store_loc = ""
        if file_name is not None:
            store_loc = self.store_loc + file_name
        else:
            store_loc = self.store_loc + url
        log.write.info("Attempting to download to tmp: " + url)
        try:
            urllib.request.urlretrieve(url, store_loc)
        except urllib.error.URLError as err:
            log.write.error(str(err))
            return
        except urllib.error.HTTPError as err:
            log.write.error(str(err))
            return
        log.write.info("Success")
        print("Success")


    # Takes an integer (fh) and returns a 3 char string representation of it.
    def __three_hr_fh(self, fh):
        if fh == 0:
            return "000"
        elif fh < 10:
            return "00" + str(fh)
        elif fh < 100:
            return "0" + str(fh)
        else:
            return str(fh)
