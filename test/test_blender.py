# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import unittest
import numpy
import lib.blender
import pygrib

class TestBlender(unittest.TestCase):

    def setUp(self):
        self.blender = lib.blender.Blender()
        self.grib = './grib.grib2'
        self.arr = [1,2,3,4,5]
        self.grib = pygrib.open(self.grib)
        self.temps = self.grib.select(name="Temperature")[0]


    def tearDown(self):
        pass

    def test_get_messages_valid(self):
        message = self.blender.getMessages('Temperature', self.grib)
        self.assertIsInstance(message, list)


    def test_form_lat_lon_pairs(self):
        #create a numpy array
        vals = numpy.array([1,2,3,4,5])
        result = self.blender.formLatLonPairs(vals, vals)
        self.assertEqual(result, [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])

    def test_getScipyValues(self):
        lats = self.temps["latitudes"][:10]
        lons = self.temps["longitudes"][:10]


    def test_getValuesAtPoint_with_iNoInterp(self):
        val = self.blender.getValuesAtPoint(99.9999, 44.44444, self.temps, self.blender.iNoInterp)
        print("\n" + str(val) + "\n")

    def test_getValuesAtPoint_with_iRectSphereBivariateSpline(self):
        val = self.blender.getValuesAtPoint(99.9999, 44.44444, self.temps, self.blender.iRectSphereBivariateSpline)
        print("\n" + str(val) + "\n")






if __name__ == '__main__':
    unittest.main()
