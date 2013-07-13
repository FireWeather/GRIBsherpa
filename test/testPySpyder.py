__author__ = 'dwc2'

from lib.grib_spyder import GribSpyder

spider = GribSpyder()

spider.download_param_grib_range(2013071300, 00, 240, 12)
