__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import unittest
import numpy
import lib.blender

class TestBlender(unittest.TestCase):

    def setUp(self):
        self.blender = lib.blender.Blender()
        self.grib = './grib.grib2'
        self.arr = [1,2,3,4,5]


    def tearDown(self):
        pass

    def test_get_messages_valid(self):
        message = self.blender.getMessages('Temperature', self.grib)
        self.assertIsInstance(message, list)

    def test_get_values(self):
        # Note I'm getting the first message in the list here
        message = self.blender.getMessages('Temperature', self.grib)[0]
        vals = self.blender.getValues(90, 270, message)
        print(vals)
        # todo: add assertion here

    def test_form_lat_lon_pairs(self):
        #create a numpy array
        vals = numpy.array([1,2,3,4,5])
        result = self.blender.formLatLonPairs(vals, vals)
        self.assertEqual(result, [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])




if __name__ == '__main__':
    unittest.main()