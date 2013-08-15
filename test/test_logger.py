# --------------------------------------------------------
# Copyright (c) 2013 Matthew Pate and Daniel Catalano
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source distribution
# of this software for license terms.
# --------------------------------------------------------

#import the test suite
import unittest
#import the class you want to test
import lib.logger as logger

#idiomatic way to name your test. Be sure to include "(unittest.TestCase)"
class TestGlobal(unittest.TestCase):

    def test_logging_works_from_global(self):
        logger.log.info("UnitTest: You should see this in the logfile")


if __name__ == '__main__':
    unittest.main()