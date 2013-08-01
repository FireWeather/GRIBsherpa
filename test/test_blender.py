__author__ = 'MCP'
# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

import unittest
import lib.blender

class TestBlender(unittest.TestCase):

    def setUp(self):
        self.blender = lib.blender.Blender('./grib.grib2')

    def tearDown(self):
        pass

    def test_get_message_valid(self):
        message = self.blender.get_message('Temperature', './grib.grib2')
        self.assertIsInstance(message, list)

