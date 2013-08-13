For Python UnitTest framework see test_fetcher for examples.

To enable running tests from the commandline the following must be at the bottom of each test file:
if __name__ == '__main__':
    unittest.main()

With the above declaration you can then run tests from the commandline as follows:
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method

BETTER, you can run the tests through pycharm by "right" clicking the test and selecting "run".
This should run the tests on the VM (as long as your configurations are set-up correctly...see below).

Testing Configurations
In order to run tests on the VM you will not only have to select the VM interpreter as the "default", but you
will also have to map the pertinent directories on your local machine to their corresponding directories
on the VM.  This is done through selecting:
test dropdown on main toolbar --> Edit Configurations...
You can then edit "Path Mappings" so that the important directories are mapped.  This includes:
/test
/tmp
/lib
/     <-- project root