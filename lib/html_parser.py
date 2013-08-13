# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import re


## The GribHtmlParser class contains functionality to parse html. The class is
# thin right now but if/when the Fetcher starts actually crawling for weather
# data this class will hold much more logic.
class GribHtmlParser:

    def __init__(self):
        pass

    ## Converts link text to html equivalent (text with brackets) and
    # searches html for match
    def link_exists_in_html(self, link, html):
        regex = self.__grib_link_regex(link)
        match = regex.search(html)
        if match is None:
            return False
        else:
            return True


    # Private ----------------------------------------------------------------

    def __grib_link_regex(self, link):
        link = '>' + link + '<'
        regex = re.compile(link)
        return regex

