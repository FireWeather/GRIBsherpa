For Python UnitTest framework see test_fetcher for examples.

To enable running tests from the commandline the following must be at the bottom of each test file:
if __name__ == '__main__':
    unittest.main()

With the above declaration you can then run tests as follows:
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method