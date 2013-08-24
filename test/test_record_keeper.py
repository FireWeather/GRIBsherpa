# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import unittest
import lib.record_keeper

class TestRecordKeeper(unittest.TestCase):

    def setUp(self):
        self.rk = lib.record_keeper.RecordKeeper("temp") # Todo: decide on default behavior

    def test_insert_grid_points(self):
        testString = self.rk.insertGridPoints(1, 2, 3, "???", "model_grid_points")
        print(testString)
        assert(testString == "INSERT INTO model_grid_points (region_number, region_ref_number, national_ref_number, location) VALUES (1, 2, 3, ???)")


if __name__ == '__main__':
    unittest.main()