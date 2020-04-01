#!/usr/bin/python
"""
Module fsio_lib.Tests.ut005_dynamic_import

Implements unit testing of the module dynamic_import. See test report TE002.
"""

__version__ = "0.1.0.0"
__date__ = "25-03-2020"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.dynamic_import as TestModule

#globals - helper test values

FILENAME = os.path.basename(__file__)

#helper functions

def UnloadOS():
    """
    Unloads the package 'os', hence all its modules.
    """
    if 'os' in dir():
        del os
        sys.stdout.write('\nModule "os" is not unloaded\n')
        sys.stdout.flush()
        sys.exit(1)
    try:
        print os.path.basename(__file__)
    except NameError:
        sys.stdout.write('\nModule "os" is unloaded\n')
        sys.stdout.flush()

#classes

#+ test cases

class Test_import_module(unittest.TestCase):
    """
    Test cases for the function import_module from the module dynamic_import.
    
    Implements tests ID TEST-T-200, TEST-T-201.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.import_module)
    
    def tearDown(self):
        """
        Executed after each unit test method - unloads the os package
        """
        UnloadOS()
    
    def test_import_module(self):
        """
        Tests the functional importing of a module.

        Test ID - TEST-T-200. Covers requirements REQ-FUN-200, REQ-FUN-220
        and REQ-FUN-221
        """
        Temp = self.TestFunction('os.path', dictGlobals = globals())
        self.assertEqual(Temp.basename(__file__), FILENAME,
                                                    msg = 'By module reference')
        self.assertEqual(os.path.basename(__file__), FILENAME,
                                                    msg = 'By module name')
        del Temp
        Temp = None
    
    def test_import_module_alias(self):
        """
        Tests the functional importing of a module with aliasing.

        Test ID - TEST-T-201. Covers requirements REQ-FUN-201, REQ-FUN-220
        and REQ-FUN-221
        """
        Temp = self.TestFunction('os.path', 'Alias', dictGlobals = globals())
        self.assertEqual(Temp.basename(__file__), FILENAME,
                                                    msg = 'By module reference')
        self.assertEqual(Alias.basename(__file__), FILENAME,
                                                    msg = 'By module alias')
        del Temp
        Temp = None

class Test_import_from_module(unittest.TestCase):
    """
    Test cases for the function import_from_module from the module
    dynamic_import.
    
    Implements tests ID TEST-T-210, TEST-T-211.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.import_from_module)
    
    def tearDown(self):
        """
        Executed after each unit test method - unloads the os package
        """
        UnloadOS()
    
    def test_import_from_module(self):
        """
        Tests the functional importing of a module.

        Test ID - TEST-T-210. Covers requirements REQ-FUN-210, REQ-FUN-220
        and REQ-FUN-221
        """
        Temp = self.TestFunction('os.path', 'basename', dictGlobals = globals())
        self.assertEqual(Temp(__file__), FILENAME,
                                                msg = 'By function reference')
        self.assertEqual(basename(__file__), FILENAME,
                                                msg = 'By function name')
        del Temp
        Temp = None
    
    def test_import_from_module_alias(self):
        """
        Tests the functional importing of a module with aliasing.

        Test ID - TEST-T-211. Covers requirements REQ-FUN-211, REQ-FUN-220
        and REQ-FUN-221
        """
        Temp = self.TestFunction('os.path', 'basename', 'Alias',
                                                    dictGlobals = globals())
        self.assertEqual(Temp(__file__), FILENAME,
                                                msg = 'By function reference')
        self.assertEqual(Alias(__file__), FILENAME,
                                                msg = 'By function alias')
        del Temp
        Temp = None

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_import_module)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_import_from_module)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.dynamic_import module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)