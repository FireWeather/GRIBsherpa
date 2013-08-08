__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------
import re

class UrlParser(object):

    ## The following class variables are used to specify download urls
    gfs = {0.5 : 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=gfs.t$MRHOUR$z.mastergrb2f$FHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2Fgfs.$MRDATE$%2Fmaster',
           1.0 : 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=gfs.t$MRHOUR$z.pgrbf$FHOUR$.grib2&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2Fgfs.$MRDATE$',
           2.5 : 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_2p5.pl?file=gfs.t$MRHOUR$z.pgrbf$FHOUR$.2p5deg.grib2&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2Fgfs.$MRDATE$'
           }
    # todo: verify what variables we need for nam, including lat/lon
    nam = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_nam_na.pl?file=nam.t$MRHOUR$z.awip32$FHOUR$.tm00.grib2&all_lev=on&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fnam.$MRDATE$'


    # todo: eventually set up ability to dynamically add url variables
    #lev_filters = { "all levels" : "all_levels=on",
    #                "500 mb" : "lev_500_mb=on",
    #                "700 mb" : "lev_700_mb=on",
    #                "750 mb" : "lev_750_mb=on",
    #                "800 mb" : "lev_800_mb=on",
    #                "850 mb" : "lev_850_mb=on",
    #                "1000 mb" : "lev_1000_mb=on" }
    #var_filters = { "all variables" : "all_var=on" }
    #box_filters = {"left": "leftlon=",
    #               "right": "rightlon=",
    #               "top": "toplat=",
    #               "bottom": "bottomlat="}


    ## Creates a url to be used in downloading files.
    #  If using to create a 'gfs' url then a degree must be specified.
    def build_download_url(self, model_type, mr_dateHour, forecast_hr, degree=None):
        if model_type.lower() == 'gfs':
            if degree is None:
                print("Error in url_parser::build_download_url - degree should not be None")
                return
            else:
                partial_path = self.gfs[degree]
                final_path = self.__build_path(partial_path, mr_dateHour, forecast_hr)
                return final_path
        elif model_type.lower() == 'nam':
            partial_path = self.nam
            final_path = self.__build_path(partial_path, mr_dateHour, forecast_hr, 'nam')
            return final_path
        else:
            print('Error in url_parser::build_download_url - unknown model type')


    # -------------------------------- Private -------------------------------------

    ## Works through the partial path specified (organized by degree in class variable) from
    #  left to right, subbing in key fields.
    #  @type    only used to specify whether 'nam' due to nam's different use of mr_dateHour
    def __build_path(self, partial_path, mr_dateHour, forecast_hr, type=None):
        # add in the model run hour                                        # get last two digits of int
        pWithMrHour = self.__add_to_forecast_hr('\$MRHOUR\$', partial_path, int(str(mr_dateHour)[-2:]))
        # add in the forecast hour
        pWithFhour = self.__add_to_forecast_hr('\$FHOUR\$', pWithMrHour, forecast_hr)
        # add in the model run date
        if type is None:
            return re.sub('\$MRDATE\$', str(mr_dateHour), pWithFhour)
        else:
            # 'nam' doesn't use the hour part of the model run datehour
            return re.sub('\$MRDATE\$', str(mr_dateHour)[:8], pWithFhour)


    ## This transforms the integer 'hour' into an appropriate string, making sure that
    #  concatenation does NOT happen.
    #  Example: If we pass in 00 or 05 we want to make sure that we don't loose the leading 0
    #  when subbing into the string.
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
