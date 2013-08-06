__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------


class UrlParser(object):

    ## The following class variables are used to specify download urls (and/or aspects of that url)
    # ---- 0.5 degree hyperlink ----
    # partial_gfs_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$%2Fmaster'
    # gfs_fh_format = 'gfs.t$MRHOUR$z.mastergrb2f$FHOUR$'

    # ---- 1.0 degree hyperlink ----
    # This is used for testing.
    #partial_gfs_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=$FORECASTHOUR$&lev_850_mb=on&all_var=on&subregion=leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$'

    partial_gfs_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&lev_1000_mb=on&lev_surface=on&all_var=on&leftlon=-133&rightlon=-95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$'
    gfs_fh_format = 'gfs.t$MRHOUR$z.pgrbf$FHOUR$.grib2'
    gfs_mr_format = 'gfs.$MRDATE$'

    partial_nam_path = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_nam_na.pl?file=$FORECASTHOUR$&lev_500_mb=on&lev_700_mb=on&lev_850_mb=on&all_var=on&leftlon=133&rightlon=95&toplat=55&bottomlat=25&dir=%2F$MODELRUN$'
    nam_fh_format = 'nam.t$MRHOUR$z.awip32$FHOUR$.tm00.grib2'
    nam_mr_format = 'nam.$MRDATE$'

    #lev_filters = { "all levels" : "all_levels=on",
    #                "500 mb" : "lev_500_mb=on",
    #                "700 mb" : "lev_700_mb=on",
    #                "750 mb" : "lev_750_mb=on",
    #                "800 mb" : "lev_800_mb=on",
    #                "850 mb" : "lev_850_mb=on",
    #                "1000 mb" : "lev_1000_mb=on" }


    #var_filters = { "all variables" : "all_var=on" }


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
