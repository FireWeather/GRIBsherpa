# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

#import the test suite
import unittest
#import the class you want to test
import lib.global

#idiomatic way to name your test. Be sure to include "(unittest.TestCase)"
class TestGlobal(unittest.TestCase):

    def test_logging_works_from_global(self):
        pass


if __name__ == '__main__':
    unittest.main()