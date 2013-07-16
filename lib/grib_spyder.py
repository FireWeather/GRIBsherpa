__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import urllib.request
import urllib.error
import lib.html_parser
import os
import re


## GribSpyder is a GRIB specific class that assists with downloading GRIB files.
# Initialization variables are optional and if used should be passed in using a dictionary with
# keys specifying the variable name that you want to initialize.
#
# GribSpyder expects the "tmp" project directory to exist and will download files to that location
# unless a different location ("store_loc") is specified at initialization.
# This class has dependencies on two other classes:
# 1. GribHtmlParser (html_parser.py)
# 2. UrlParser (defined below)
class GribSpyder(object):


    ## @param args A dictionary of initialization params
    def __init__(self, args=None):
        self.url_parser = UrlParser() #defined below
        self.html_parser = lib.html_parser.GribHtmlParser()
        self.url = self.__default_args("url", args)
        self.store_loc = self.__default_args("store_loc", args)


    ## Opens url, reads it's contents, converts to string and returns (or returns error)
    # @params url A string specifying the url to get_html for
    def get_html(self, url):
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.HTTPError as err:
            return err
        except urllib.error.URLError as err:
            return err
        except ValueError as err:
            return err
        return str(response.readall())


    ## Gets html string (of url), makes sure link exists within string, attempts to download it.
    # Example Usage: mySpyder.download_file_by_link('gfs.t12z.goessimpgrb2f00.1p0deg')
    def download_file_by_link(self, link, url):
        html = self.get_html(url)
        print("url response type: " + str(type(html)))
        #link_exists = self.html_parser.grib_link_exists(link, html)
        if self.html_parser.link_exists_in_html(link, html):
            to_download = self.__build_link(url, link)
            self.__download(to_download)
        else:
            print("link to download does not seem to exist.")


    ## Downloads using the full url passed in (direct path to file).
    def download_file_by_url(self, url):
        self.__download(url)


    ## Downloads multiple grib files as specified by the parameters.
    # @param model_type:          String describing model type (ex. 'nam', 'gfs', etc.)
    # @param model_run_dateHour:  integer describing dateHour (YYYYMMDDHH, ex. 2013070100)
    # @param fh_start:            integer describing the hour to start 00, 03, 06, etc. (or greater)
    # @param fh_end:              integer describing the hour to end (inclusive)
    # @param increment:           integer describing how to increment the forecast hours being downloaded
    # NOTE: the increment must correspond to an actual increment provided by NOAA, otherwise
    # errors will be thrown. If this happens the method will continue trying to downloading
    # any files that it find matches for until fh_end has been reached.
    def download_param_grib_range(self, model_type, model_run_dateHour, fh_start, fh_end, increment):
        start = fh_start
        end = fh_end
        inc = increment
        print("Downloading GRIB range for model run type: " + model_type + "\n" +
              "............dateHour = " + str(model_run_dateHour) + "\n" +
              "............start = " + str(start) + "\n" +
              "............end = " + str(end) + "\n" +
              "............increment = " + str(inc))
        while start <= end:
            to_download = self.url_parser.build_download_url(model_type, model_run_dateHour, start)
            file_name = str(model_run_dateHour) + "_" + self.__three_hr_fh(start) + ".grib"
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
        if os.path.exists(tmp_dir):
            print("found tmp for storage: " + tmp_dir)
            return tmp_dir
        else:
            print("ERROR in GribSpyder.__build_path_to_tmp: tmp directory not found")
            return None


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
    # 4. return err if encountered or prints "done" to console
    def __download(self, url, file_name=None):
        store_loc = ""
        if file_name is not None:
            store_loc = self.store_loc + file_name
        else:
            store_loc = self.store_loc + url
        print("attempting to download to tmp: " + url)
        try:
            urllib.request.urlretrieve(url, store_loc)
        except urllib.error.URLError as err:
            print(str(err))
            return err
        except urllib.error.HTTPError as err:
            print(str(err))
            return err
        print("done")


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



class UrlParser(object):

    ## The following class variables are used to specify download urls (and/or aspects of that url)
    # ---- 0.5 degree hyperlink ----
    # partial_gfs_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$%2Fmaster'
    # gfs_fh_format = 'gfs.t$MRHOUR$z.mastergrb2f$FHOUR$'

    # ---- 1.0 degree hyperlink ----
    partial_gfs_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&lev_surface=on&all_var=on&leftlon=-133&rightlon=-95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$'
    gfs_fh_format = 'gfs.t$MRHOUR$z.pgrbf$FHOUR$.grib2'
    gfs_mr_format = 'gfs.$MRDATE$'

    partial_nam_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_nam_na.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$'
    nam_fh_format = 'nam.t$MRHOUR$z.awip32$FHOUR$.tm00.grib2'
    nam_mr_format = 'nam.$MRDATE$'

    ## Uses mr_type and dateHour to build the corresponding model run
    def build_model_run(self, mr_type, date_hour):
        if mr_type.lower() == 'gfs':
            return re.sub('\$MRDATE\$', str(date_hour), self.gfs_mr_format)
        elif mr_type.lower() == 'nam':
            return re.sub('\$MRDATE\$', str(date_hour), self.nam_mr_format)
        else:
            print('toots')

    def build_download_url(self, model_type, mr_dateHour, forecast_hr):
        model_run = self.build_model_run(model_type, mr_dateHour)
        forecast_hour = self.__build_forecast_hr(model_type, mr_dateHour, forecast_hr)
        if model_type.lower() == 'gfs':
            return self.__search_replace_partial_path(self.partial_gfs_path, model_run, forecast_hour)
        elif model_type.lower() == 'nam':
            return self.__search_replace_partial_path(self.partial_nam_path, model_run, forecast_hour)
        else:
            print('euro model')

    # -------------------------------- Private -------------------------------------
    # expects '$HOUR$' to be in string, replaces it with 'hour'
    def __add_to_forecast_hr(self, regex, string, hour):
        hr = hour
        #perform checks to avoid truncating leading 0
        if type(hour) == int:
            if hour == 0:
                hr = '00'
            elif hour < 10:
                hr = '0' + str(hour)
            else:
                hr = str(hour)
        return re.sub(regex, hr, string)

    def __build_forecast_hr(self, mr_type, date_hour, forecast_hr):
        mr = str(date_hour) #need str so index can happen below
        if mr_type.lower() == 'gfs':
            #add model run hour
            tmp = self.__add_to_forecast_hr('\$MRHOUR\$', self.gfs_fh_format, mr[-2:])
            #add forecast hour and return
            return self.__add_to_forecast_hr('\$FHOUR\$', tmp, forecast_hr)
        elif mr_type.lower() == 'nam':
            #add model run hour todo: figure out where model run hour changes
            tmp = self.__add_to_forecast_hr('\$MRHOUR\$', self.nam_fh_format, '00')
            return self.__add_to_forecast_hr('\$FHOUR\$', tmp, forecast_hr)
        else:
            print('euro model')

    def __search_replace_partial_path(self, partial_path, model_run=None, forecast_hr=None):
        p = ''
        if model_run:
            p = re.sub('\$MODELRUN\$', model_run, partial_path)
        if forecast_hr:
            p = re.sub('\$FORECASTHOUR\$', forecast_hr, p)
        return p