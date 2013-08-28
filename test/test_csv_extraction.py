# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

from sys import path
import unittest
path.append('.')
from lib.csv_data_extraction import CsvDataExtraction

class TestCsvDataExtraction(unittest.TestCase):

    def setUp(self):
        file = 'data/regions.csv'
        self.csvExtractor = CsvDataExtraction(file)

    def tearDown(self):
        pass

    def test_csv_contents(self):
        self.csvExtractor.getCSVDict()

if __name__ == '__main__':
    unittest.main()