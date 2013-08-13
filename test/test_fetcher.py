# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

#import the test suite
import unittest
#import the class you want to test
import lib.fetcher

#idiomatic way to name your test. Be sure to include "(unittest.TestCase)"
class TestFetcher(unittest.TestCase):

    #do any set-up you need for the tests. Anything instantiated here persists through the test suite
    #whereas anything created in each testing "method" expires at the end of said method. None of the
    #tests can take parameters except for "(self)"
    def setUp(self):
        self.fetcher = lib.fetcher.Fetcher()
        self.mrDhour = 2013080300

    #get rid of anything you created for testing that you don't want to live on. I usually would use this
    #for cleaning up files or temporary folders or something.
    def tearDown(self):
        pass

    #idiomatic way to name your tests. Typical procedure is:
    #1. create your test stored in a variable (or whatever)
    #2. perform some sort of assertion on what you expect
    #basic rules: DON'T test private functions. Keep the tests VERY small and simple. Ideally these can be
    #written before you write the actual code. The idea is "red, green, refactor"
    #Python assertions: http://docs.python.org/3.3/library/unittest.html
    #great talk on TDD: http://www.confreaks.com/videos/2452-railsconf2013-the-magic-tricks-of-testing
    def test_get_html_valid_url(self):
        html = self.fetcher.get_html('www.google.com')
        self.assertIsNot(html, IOError)

    def test_get_html_invalid_url(self):
        html = self.fetcher.get_html('www.hopefullythisurldoesntexist.com')
        self.assertIsInstance(html, ValueError)

    # todo: figure out a way to assert downloads occured
    def test_download_gfs_files(self):
        self.fetcher.download_param_grib_range('gfs', self.mrDhour, 00, 6, 6, 0.5)
        self.fetcher.download_param_grib_range('gfs', self.mrDhour, 00, 6, 6, 1.0)
        self.fetcher.download_param_grib_range('gfs', self.mrDhour, 00, 6, 6, 2.5)

    def test_download_nam_file(self):
        self.fetcher.download_param_grib_range('nam', self.mrDhour, 00, 6, 6)

# This allows the tests to be run as a stand alone module.
if __name__ == '__main__':
    unittest.main()
