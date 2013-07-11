__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import re


# contains basic parsing functionality, will be extended
class GRIBLinkParser:

    def __init__(self):
        pass

    # appends href brackets to search for link text
    def grib_link_exists(self, link, html):
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

