__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------
# GribSpyder is a GRIB specific class that assists with downloading GRIB files.  It can be initialized with a dictionary
# containing a default url to work from and a default storage location ( {'url' : 'urlpath', 'store_loc' : 'pathToStorage'} ).
# If these values are not provided the hardcoded class variable for GRIB files and the hardcoded path to the project "tmp"
# folder will be used as defaults.  Note that .gitignore should disregard any files except the README that exist
# within this directory. See specific methods for any questions you might have.

import urllib.request
import urllib.error
import lib.html_parser
import os
import re


class GribSpyder(object):

    # 0.5 degree hyperlink
    # partial_grib_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$%2Fmaster'
    # forecast_hr_format = 'gfs.t$MRHOUR$z.mastergrb2f$FHOUR$'

    # 1.0 degree hyperlink
    partial_grib_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&lev_surface=on&all_var=on&leftlon=-133&rightlon=-95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$' # changes for 1.0 degree resolution data
    forecast_hr_format = 'gfs.t$MRHOUR$z.pgrbf$FHOUR$.grib2'

    model_run_format = 'gfs.$MRDATE$'


    def __init__(self, args=None):
        self.link_parser = lib.html_parser.GRIBLinkParser()
        self.url = self.__default_args("url", args)
        self.store_loc = self.__default_args("store_loc", args)


    # Opens url, reads it's contents, converts to string and returns (or returns error)
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


    # Gets html string, makes sure link exists within, attempts to download it.
    # This only works if you've specified a url for the class (self.url) where all the
    # downloadable files are.
    # Example Usage: mySpyder.download_file_by_link('gfs.t12z.goessimpgrb2f00.1p0deg'
    def download_file_by_link(self, link):
        html = self.get_html(self.url)
        print("url response type: " + str(type(html)))
        #link_exists = self.link_parser.grib_link_exists(link, html)
        if self.__link_exists_in_html(link, html):
            to_download = self.__build_link(self.url, link)
            self.__download(to_download)
        else:
            print("link to download does not seem to exist.")


    # Downloads using the full url passed in (direct path to file).
    def download_file_by_url(self, url):
        self.__download(url)


    # Uses class variables, substitutes in the model_run and forecast_hr (using regex),
    # and tries to download the files that the resulting full path specifies.  Note that
    # model_run and forecast_hr should specify the exact text to replace in the class variables.
    # Example Usage: mySpyder.download_param_grib('gfs.2013070100', 'gfs.t00z.mastergrb2f00')
    def download_param_grib(self, model_run, forecast_hr):
        path = self.__search_replace_partial_path(self.partial_grib_path, model_run, forecast_hr)
        self.__download(path)


    # Downloads gribs as specified in a dictionary. Note sure of how useful this is. May be worth deleting.
    # Example: spyder.download_param_gribs_dict({'gfs.2013070100' : ['gfs.t00z.mastergrb2f00', 'gfs.t00z.mastergrb2f03', etc.]})
    def download_param_gribs_dict(self, dict):
        for key in dict:
            for item in dict[key]:
                print('attempting to download: ' + key + ' - ' + item)
                self.download_param_grib(key, item)


    # Downloads multiple grib files as specified by the parameters.
    # model_run_dateHour:  integer describing dateHour (YYYYMMDDHH, ex. 2013070100)
    # fh_start:            integer describing the hour to start 00, 03, 06, etc. (or greater)
    # fh_end:              integer describing the hour to end (inclusive)
    # increment:           integer describing how to increment the forecast hours being downloaded
    # NOTE: the increment must correspond to an actual increment provided by NOAA, otherwise
    # errors will be thrown. If this happens the method will continue trying to downloading
    # any files that it find matches for until fh_end has been reached.
    def download_param_grib_range(self, model_run_dateHour, fh_start, fh_end, increment):
        start = int(fh_start)
        end = int(fh_end)
        inc = int(increment)
        mr = str(model_run_dateHour)
        model_run = self.__build_model_run(model_run_dateHour)
        print("Downloading GRIB range for model run: " + str(model_run) + "\n" +
              "............start = " + str(start) + "\n" +
              "............end = " + str(end) + "\n" +
              "............increment = " + str(inc))
        # ----------- Build the full url to download in 3 steps ----------
        # 1. Add model run hour part to the forecast path: gfs.t$$z... This stays the same for below iterations.
        forecast_hour = self.__add_to_forecast_hr('\$MRHOUR\$', self.forecast_hr_format, mr[-2:])
        while start <= end:
            # 2. Add forecast hour to the forecast path. This iterates from fh_start to fh_end in increments.
            tmp = self.__add_to_forecast_hr('\$FHOUR\$', forecast_hour, start)
            # 3. Add the path created above to the main partial_grib_path along with the model run.
            path = self.__search_replace_partial_path(self.partial_grib_path, model_run, tmp)
            # create name for file: YYYMMDDHH_FHHH.grib
            file_name = str(model_run_dateHour) + "_" + self.__three_hr_fh(start) + ".grib"
            self.__download(path, file_name)
            start += inc



    # Private -------------------------------------------------------

    def __build_link(self, url, link):
        return url + link


    # builds a path to 'tmp' which should be in project tree
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


    # turns var into gfs.
    def __build_model_run(self, dateHour):
        return re.sub('\$MRDATE\$', str(dateHour), self.model_run_format)


    def __default_args(self, type, args):
        if args is None or not args.contains(type):
            if type == "store_loc":
                return self.__build_path_to_tmp()
            else:
                return None
        return args[type]


    # 1. expects there to be a temp directory
    # 2. builds storage file path based on tmp path and base of url being downloaded
    # 3. attempts to download file
    def __download(self, url, file_name=None):
        store_loc = ""
        if file_name is not None:
            store_loc = self.store_loc + file_name
        else:
            store_loc = self.store_loc + self.__get_url_base(url)
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


    # gets part of url after last slash
    def __get_url_base(self, url):
        return url.rsplit('/', 1)[1]


    # verifies that a link (text) exists in the html
    def __link_exists_in_html(self, link, html):
        return self.link_parser.grib_link_exists(link, html)


    def __search_replace_partial_path(self, partial_path, model_run=None, forecast_hr=None):
        p = ''
        if model_run:
            p = re.sub('\$MODELRUN\$', model_run, partial_path)
        if forecast_hr:
            p = re.sub('\$FORECASTHOUR\$', forecast_hr, p)
        return p


    def __three_hr_fh(self, fh):
        if fh == 0:
            return "000"
        elif fh < 10:
            return "00" + str(fh)
        elif fh < 100:
            return "0" + str(fh)
        else:
            return str(fh)

