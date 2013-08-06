__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import unittest
import re
import lib.url_parser

# todo: hardcode expected url's for assertions/comparisons
class TestUrlParser(unittest.TestCase):

    def setUp(self):
        self.urlParser = lib.url_parser.UrlParser()

    def tearDown(self):
        pass

    def test_build_path_half(self):
        path = self.urlParser.build_download_url("gfs", 0.5, 2013080606, 00)
        print(path)

    def test_build_path_one(self):
        path = self.urlParser.build_download_url('gfs', 1.0, 2013080606, 00)
        print(path)

    def test_build_path_twoFive(self):
        path = self.urlParser.build_download_url('gfs', 2.5, 2013080606, 00)
        print(path)

if __name__ == '__main__':
    unittest.main()