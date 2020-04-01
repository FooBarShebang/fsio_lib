#!/usr/bin/python
"""
Module fsio_lib.Tests.ut006_LoggingFSIO

Implements unit testing of the module LogingFSIO. See test report TE003.
"""

__version__ = "0.1.0.0"
__date__ = "26-03-2020"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import shutil
import unittest
import hashlib
import logging

#+ tested module

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))

LIB_ROOT = os.path.dirname(TEST_ROOT)

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.LoggingFSIO as TestModule

#globals

LOG_FILE = os.path.join(TEST_ROOT, 'Output', 'ut006.log')

#classes

#+ test cases

class Test_LoggingFSIO(unittest.TestCase):
    """
    Test cases for the class LoggingFSIO from the module LoggingFSIO.
    
    Implements tests ID TEST-T-300, TEST-T-310, TEST-T-311, TEST-T-320,
    TEST-T-321, TEST-T-330, TEST-T-331, TEST-T-340, TEST-T-341, TEST-T-350 and
    TEST-T-351.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = TestModule.LoggingFSIO
        cls.CheckSum = hashlib.md5('test').hexdigest()
        cls.Filename = os.path.join(TEST_ROOT, 'a.txt')
        if not os.path.isfile(cls.Filename):
            with open(cls.Filename, 'wt') as fFile:
                fFile.write('test')
        cls.ModTime = os.path.getmtime(cls.Filename)
        cls.TestClass.changeLogFile(LOG_FILE)
        cls.TestClass.setLoggingLevel(logging.DEBUG)
        cls.TestClass.setConsoleLoggingLevel(logging.ERROR)
        cls.TestClass.setFileLoggingLevel(logging.DEBUG)
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning up, done only once.
        """
        if os.path.isfile(cls.Filename):
            os.remove(cls.Filename)

    def test_makeDirs(self):
        """
        Checks that the method makeDirs() can create the complete missing path.

        Test ID - TEST-T-310. Covers requirements REQ-FUN-311, REQ-AWM-310 and
        REQ-AWM-311.
        """
        strPath = os.path.join(TEST_ROOT, 'a', 'b')
        iError, _ = self.TestClass.makeDirs(strPath)
        self.assertEqual(iError, 0, msg = 'Cannot create new folders!')
        self.assertTrue(os.path.isdir(strPath),
                                            msg = 'Cannot create new folders!')
        shutil.copy2(self.Filename, strPath)
        iError, _ = self.TestClass.makeDirs(strPath)
        self.assertEqual(iError, 0, msg = 'Cannot skip existing folders!')
        self.assertTrue(os.path.isdir(strPath),
                                         msg = 'Cannot skip existing folders!')
        self.assertTrue(os.path.isfile(os.path.join(strPath,
                                        os.path.basename(self.Filename))),
                                        msg = 'Folders are overwritten')
        shutil.rmtree(os.path.join(TEST_ROOT, 'a'))
        self.assertFalse(os.path.isdir(strPath),
                                         msg = 'Cannot remove created folders!')
    
    def test_makeDirs_Errors(self):
        """
        Checks that the method makeDirs() properly intercepts and reports errors
        occured in the process.

        Test ID - TEST-T-311. Covers requirements REQ-FUN-310, REQ-AWM-310 and
        REQ-AWM-311.
        """
        for gTemp in [1, 2.0, int, True, (1,), {'a' : 'b'}, str]:
            iError, _ = self.TestClass.makeDirs(gTemp)
            self.assertEqual(iError, 1)
        if os.name == 'posix':
            iError, _ = self.TestClass.makeDirs('/test')
            # should not be allowed in POSIX!
            self.assertEqual(iError, 3)
        #TODO - some way to check with permissions on Windows.
    
    def test_copyFile(self):
        """
        Checks that the method copyFile() performs as specified.

        Test ID - TEST-T-320. Covers requirements REQ-FUN-311, REQ-AWM-310 and
        REQ-AWM-311.
        """
        #copy localy with renaming
        #+ explicit target folder
        iError, _ = self.TestClass.copyFile(self.Filename, TEST_ROOT, 'b.txt')
        self.assertEqual(iError, 0)
        strNewPath = os.path.join(TEST_ROOT, 'b.txt')
        self.assertTrue(os.path.isfile(strNewPath))
        with open(strNewPath, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewPath), 4)
        os.remove(strNewPath)
        #+ implicit target folder
        iError, _ = self.TestClass.copyFile(self.Filename,
                                                    strNewBaseName = 'b.txt')
        self.assertEqual(iError, 0)
        self.assertTrue(os.path.isfile(strNewPath))
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewPath), 4)
        with open(strNewPath, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        os.remove(strNewPath)
        strTarget = os.path.join(TEST_ROOT, 'a', 'b')
        #copy into another folder
        #+ without renaming
        iError, _ = self.TestClass.copyFile(self.Filename, strTarget)
        self.assertEqual(iError, 0)
        strNewPath = os.path.join(strTarget, 'a.txt')
        self.assertTrue(os.path.isfile(strNewPath))
        with open(strNewPath, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewPath), 4)
        #+ with renaming
        iError, _ = self.TestClass.copyFile(self.Filename, strTarget,
                                                    strNewBaseName = 'b.txt')
        self.assertEqual(iError, 0)
        strNewPath = os.path.join(strTarget, 'b.txt')
        self.assertTrue(os.path.isfile(strNewPath))
        with open(strNewPath, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewPath), 4)
        shutil.rmtree(os.path.join(TEST_ROOT, 'a'))
        self.assertFalse(os.path.isdir(strTarget),
                                         msg = 'Cannot remove created folders!')

    def test_copyFile_Errors(self):
        """
        Checks that the method copyFile() properly intercepts and reports errors
        occured in the process.

        Test ID - TEST-T-321. Covers requirements REQ-FUN-310, REQ-AWM-310 and
        REQ-AWM-311.
        """
        for gTemp in [1, 2.0, int, True, (1,), {'a' : 'b'}, str]:
            #not string source
            iError, _ = self.TestClass.copyFile(gTemp, TEST_ROOT)
            self.assertEqual(iError, 1)
            #not string target
            iError, _ = self.TestClass.copyFile(self.Filename, gTemp)
            self.assertEqual(iError, 1)
            #not string base filename
            iError, _ = self.TestClass.copyFile(self.Filename, TEST_ROOT, gTemp)
            self.assertEqual(iError, 1)
        iError, _ = self.TestClass.copyFile(os.path.join(TEST_ROOT, 'c.txt'),
                                                                    TEST_ROOT)
        self.assertEqual(iError, 2)
        if os.name == 'posix':
            # should not be allowed in POSIX!
            iError, _ = self.TestClass.copyFile(self.Filename, '/test')
            self.assertEqual(iError, 3)
            iError, _ = self.TestClass.copyFile(self.Filename, '/var')
            self.assertEqual(iError, 3)
        #TODO - some way to check with permissions on Windows.
    
    def test_deleteFile(self):
        """
        Checks that the method deleteFile() can remove a file.

        Test ID - TEST-T-330. Covers requirements REQ-FUN-311, REQ-AWM-310 and
        REQ-AWM-311.
        """
        self.TestClass.copyFile(self.Filename, strNewBaseName = 'b.txt')
        strPath = os.path.join(TEST_ROOT, 'b.txt')
        self.assertTrue(os.path.isfile(strPath))
        iError, _ = self.TestClass.deleteFile(strPath)
        self.assertEqual(iError, 0)
        self.assertFalse(os.path.isfile(strPath))
    
    def test_deleteFile_Errors(self):
        """
        Checks that the method deleteFile() properly intercepts and reports
        errors occured in the process.

        Test ID - TEST-T-331. Covers requirements REQ-FUN-310, REQ-AWM-310 and
        REQ-AWM-311.
        """
        for gTemp in [1, 2.0, int, True, (1,), {'a' : 'b'}, str]:
            iError, _ = self.TestClass.deleteFile(gTemp)
            self.assertEqual(iError, 1)
        strPath = os.path.join(TEST_ROOT, 'super_test.txt')
        iError, _ = self.TestClass.deleteFile(strPath)
        self.assertEqual(iError, 2)
        strPath = os.path.join(TEST_ROOT, 'Output')
        iError, _ = self.TestClass.deleteFile(strPath) #not a file!
        self.assertEqual(iError, 3)
    
    def test_moveFile(self):
        """
        Checks that the method deleteFile() can move a file with or without
        renaming.

        Test ID - TEST-T-340. Covers requirements REQ-FUN-311, REQ-AWM-310 and
        REQ-AWM-311.
        """
        self.TestClass.copyFile(self.Filename, strNewBaseName = 'b.txt')
        strPath = os.path.join(TEST_ROOT, 'a', 'b')
        strOldPath = os.path.join(TEST_ROOT, 'b.txt')
        strNewName = os.path.join(strPath, 'b.txt')
        iError, _ = self.TestClass.moveFile(strOldPath, strPath)
        self.assertEqual(iError, 0)
        self.assertTrue(os.path.isfile(strNewName))
        with open(strNewName, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewName), 4)
        self.TestClass.copyFile(self.Filename, strNewBaseName = 'b.txt')
        strNewName = os.path.join(strPath, 'c.txt')
        iError, _ = self.TestClass.moveFile(strOldPath, strPath, 'c.txt')
        self.assertEqual(iError, 0)
        self.assertTrue(os.path.isfile(strNewName))
        with open(strNewName, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewName), 4)
        shutil.rmtree(os.path.join(TEST_ROOT, 'a'))
        self.assertFalse(os.path.isdir(strPath),
                                         msg = 'Cannot remove created folders!')

    def test_moveFile_Errors(self):
        """
        Checks that the method moveFile() properly intercepts and reports errors
        occured in the process.

        Test ID - TEST-T-341. Covers requirements REQ-FUN-310, REQ-AWM-310 and
        REQ-AWM-311.
        """
        for gTemp in [1, 2.0, int, True, (1,), {'a' : 'b'}, str]:
            #not string source
            iError, _ = self.TestClass.moveFile(gTemp, TEST_ROOT)
            self.assertEqual(iError, 1)
            #not string target
            iError, _ = self.TestClass.moveFile(self.Filename, gTemp)
            self.assertEqual(iError, 1)
            #not string base filename
            iError, _ = self.TestClass.moveFile(self.Filename, TEST_ROOT, gTemp)
            self.assertEqual(iError, 1)
        iError, _ = self.TestClass.moveFile(os.path.join(TEST_ROOT, 'test.txt'),
                                                                    TEST_ROOT)
        self.assertEqual(iError, 2)
        if os.name == 'posix':
            # should not be allowed in POSIX!
            iError, _ = self.TestClass.moveFile(self.Filename, '/test')
            self.assertEqual(iError, 3)
            iError, _ = self.TestClass.moveFile(self.Filename, '/var')
            self.assertEqual(iError, 3)
        #TODO - some way to check with permissions on Windows.
    
    def test_renameFile(self):
        """
        Checks that the method renameFile() can rename a file.

        Test ID - TEST-T-350. Covers requirements REQ-FUN-311, REQ-AWM-310 and
        REQ-AWM-311.
        """
        self.TestClass.copyFile(self.Filename, strNewBaseName = 'b.txt')
        strPath = os.path.join(TEST_ROOT, 'b.txt')
        self.assertTrue(os.path.isfile(strPath))
        iError, _ = self.TestClass.renameFile(strPath, 'c.txt')
        strNewPath = os.path.join(TEST_ROOT, 'c.txt')
        self.assertEqual(iError, 0)
        self.assertTrue(os.path.isfile(strNewPath))
        with open(strNewPath, 'rt') as fFile:
            strCheck = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheck, self.CheckSum)
        self.assertAlmostEqual(self.ModTime, os.path.getmtime(strNewPath), 4)
        os.remove(strNewPath)
    
    def test_renameFile_Errors(self):
        """
        Checks that the method renameFile() properly intercepts and reports
        errors occured in the process.

        Test ID - TEST-T-351. Covers requirements REQ-FUN-310, REQ-AWM-310 and
        REQ-AWM-311.
        """
        for gTemp in [1, 2.0, int, True, (1,), {'a' : 'b'}, str]:
            iError, _ = self.TestClass.renameFile(gTemp, 'c.txt')
            self.assertEqual(iError, 1)
            iError, _ = self.TestClass.renameFile(self.Filename, gTemp)
        strPath = os.path.join(TEST_ROOT, 'super_test.txt')
        iError, _ = self.TestClass.renameFile(strPath, 'c.txt')
        self.assertEqual(iError, 2)
        iError, _ = self.TestClass.renameFile(self.Filename, 'Output/c.txt')
        #not a base filename!
        self.assertEqual(iError, 2)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_LoggingFSIO)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.LoggingFSIO module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)