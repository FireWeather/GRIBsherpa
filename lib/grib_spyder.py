# Copyright (c) 2013 Matthew Pate
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
__author__ = 'MCP'

import urllib.request
import urllib.error
import lib.html_parser
import os
import re


#() holds any inheritance
class GribSpyder(object):

    partial_grib_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_750_mb=on&lev_800_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$%2Fmaster'
    forecast_hr_format = 'gfs.t$MRHOUR$z.mastergrb2f$FHOUR$'
    model_run_format = 'gfs.$MRDATE$'

    def __init__(self, args):
        self.link_parser = lib.html_parser.GRIBLinkParser()
        #optionally initialize url
        self.url = self.__default_url(args)
        # optionally initialize storage location
        self.store_loc = self.__default_store_loc(args)

    # -opens url in try catch block. Will need to extend catches based on request type
    # -error object can hold server response. There is a dict of common responses (see bookmark)
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

    # Gets html, makes sure link exists, attempts to download it.
    def download_file_by_link(self, link):
        html = self.get_html(self.url)
        print("url response type: " + str(type(html)))
        #link_exists = self.link_parser.grib_link_exists(link, html)
        if self.__link_exists_in_html(link, html):
            to_download = self.__build_link(self.url, link)
            self.__download(to_download)
        else:
            print("link to download does not seem to exist.")

    def download_file_by_url(self, url):
        self.__download(url)

    #this should be passed the exact text that changes in the path
    def download_param_grib(self, model_run, forecast_hr):
        path = self.__search_replace_partial_path(self.partial_grib_path, model_run, forecast_hr)
        self.__download(path)

    def download_param_gribs_dict(self, dict):
        for key in dict:
            for item in dict[key]:
                print('attempting to download: ' + key + ' - ' + item)
                self.download_param_grib(key, item)

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
        # Add in the part of the forecast path related to the model run: gfs.t$$z...
        forecast_hour = self.__add_to_forecast_hr('\$MRHOUR\$', self.forecast_hr_format, mr[-2:])
        # Add in the part of the forecast path related to the forecast hour
        while start < end:
            # Add in the part of the forecast path related to the forecast hour
            one = self.__add_to_forecast_hr('\$FHOUR\$', forecast_hour, start)
            # Add the completed partial_path above into the main partial_grib_path along with the model run
            path = self.__search_replace_partial_path(self.partial_grib_path, model_run, one)
            self.__download(path)
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

    def __add_forecast_hr_forecast(self, string, hour):
        hr = hour
        #perform checks to avoid truncating leading 0
        if type(hour) == int:
            if hour == 0:
                hr = '00'

        string = str(string)
        hour = str(hour)
        return re.sub('\$FHOUR\$', hour, string)

    def __build_model_run(self, dateHour):
        return re.sub('\$MRDATE\$', str(dateHour), self.model_run_format)

    def __default_store_loc(self, args):
        if 'store_loc' in args:
            return args['store_loc']
        else:
            return self.__build_path_to_tmp()

    def __default_url(self, args):
        if 'url' in args:
            return args['url']
        else:
            return None

    # 1. expects there to be a temp directory
    # 2. builds storage file path based on tmp path and base of url being downloaded
    # 3. attempts to download file
    def __download(self, url):
        store_loc = self.store_loc + self.__get_url_base(url)
        print("attempting to download to tmp: " + url)
        urllib.request.urlretrieve(url, store_loc)
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
        print("modified 'partial' grib path: " + p)
        return p



