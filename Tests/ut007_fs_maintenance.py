#!/usr/bin/python
"""
Module fsio_lib.Tests.ut007_fs_maintenance

Implements unit testing of the module fs_maitenance. See test report TE005.
"""

__version__ = "0.1.0.0"
__date__ = "30-03-2020"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import shutil
import unittest
import hashlib
import time

#+ tested module

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))

LIB_ROOT = os.path.dirname(TEST_ROOT)

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.fs_maintenance as TestModule

#classes

#+ test cases

class Test_fs_maitenance(unittest.TestCase):
    """
    Test cases for the all functions from the module fs_maintenance.
    
    Implements tests ID TEST-T-500, TEST-T-510, TEST-T-520, .
    """

    def test_TouchFolder(self):
        """
        Tests the performance of the function TouchFolder().

        Test ID - TEST-T-500. Covers requirement REQ-FUN-500.
        """
        strPath1 = os.path.join(TEST_ROOT, 'a')
        strPath2 = os.path.join(strPath1, 'b')
        self.assertFalse(os.path.isdir(strPath1))
        self.assertFalse(os.path.isdir(strPath2))
        TestModule.TouchFolder(strPath2)
        self.assertTrue(os.path.isdir(strPath1))
        self.assertTrue(os.path.isdir(strPath2))
        with open(os.path.join(strPath1, 'test.txt'), 'wt') as fFile:
            fFile.write('1')
        with open(os.path.join(strPath1, 'test.txt'), 'rt') as fFile:
            strCheckSum1 = hashlib.md5(fFile.read()).hexdigest()
        dModTime1 = os.path.getmtime(os.path.join(strPath1, 'test.txt'))
        with open(os.path.join(strPath2, 'test.txt'), 'wt') as fFile:
            fFile.write('2')
        with open(os.path.join(strPath2, 'test.txt'), 'rt') as fFile:
            strCheckSum2 = hashlib.md5(fFile.read()).hexdigest()
        dModTime2 = os.path.getmtime(os.path.join(strPath2, 'test.txt'))
        TestModule.TouchFolder(strPath2)
        with open(os.path.join(strPath1, 'test.txt'), 'rt') as fFile:
            self.assertEqual(strCheckSum1,hashlib.md5(fFile.read()).hexdigest())
        with open(os.path.join(strPath2, 'test.txt'), 'rt') as fFile:
            self.assertEqual(strCheckSum2,hashlib.md5(fFile.read()).hexdigest())
        self.assertAlmostEqual(dModTime1,
                        os.path.getmtime(os.path.join(strPath1, 'test.txt')), 4)
        self.assertAlmostEqual(dModTime2,
                        os.path.getmtime(os.path.join(strPath2, 'test.txt')), 4)
        self.assertListEqual(os.listdir(strPath1), ['b', 'test.txt'])
        self.assertListEqual(os.listdir(strPath2), ['test.txt'])
        shutil.rmtree(strPath1)
        self.assertFalse(os.path.isdir(strPath1))
        self.assertFalse(os.path.isdir(strPath2))
    
    def test_SmartCopy(self):
        """
        Tests the performance of the function SmartCopy().

        Test ID - TEST-T-510. Covers requirement REQ-FUN-510.
        """
        strPath1 = os.path.join(TEST_ROOT, 'source')
        strPath2 = os.path.join(TEST_ROOT, 'target')
        strTestFile = os.path.join(strPath1, 'test.txt')
        TestModule.TouchFolder(strPath1)
        TestModule.TouchFolder(strPath2)
        with open(strTestFile, 'wt') as fFile:
            fFile.write('1')
        with open(strTestFile, 'rt') as fFile:
            strCheckSum = hashlib.md5(fFile.read()).hexdigest()
        dModTime = os.path.getmtime(strTestFile)
        self.assertEqual(len(os.listdir(strPath2)), 0)
        strCheckFile = os.path.join(strPath2, 'test.txt')
        for _ in [1,2]:
            TestModule.SmartCopy(strTestFile, strPath2)
            self.assertListEqual(os.listdir(strPath2), ['test.txt'])
            with open(strCheckFile, 'rt') as fFile:
                self.assertEqual(strCheckSum,
                                        hashlib.md5(fFile.read()).hexdigest())
            self.assertAlmostEqual(dModTime, os.path.getmtime(strCheckFile), 4)
        with open(strTestFile, 'wt') as fFile:
            fFile.write('2')
        with open(strTestFile, 'rt') as fFile:
            strCheckSum = hashlib.md5(fFile.read()).hexdigest()
        dModTime = os.path.getmtime(strTestFile)
        strCheckFile = os.path.join(strPath2, 'test (copy).txt')
        for _ in [1,2]:
            TestModule.SmartCopy(strTestFile, strPath2)
            self.assertItemsEqual(os.listdir(strPath2), ['test.txt',
                                                            'test (copy).txt'])
            with open(strCheckFile, 'rt') as fFile:
                self.assertEqual(strCheckSum,
                                        hashlib.md5(fFile.read()).hexdigest())
            self.assertAlmostEqual(dModTime, os.path.getmtime(strCheckFile), 4)
        with open(strTestFile, 'wt') as fFile:
            fFile.write('3')
        with open(strTestFile, 'rt') as fFile:
            strCheckSum = hashlib.md5(fFile.read()).hexdigest()
        dModTime = os.path.getmtime(strTestFile)
        strCheckFile = os.path.join(strPath2, 'test (copy 1).txt')
        for _ in [1,2]:
            TestModule.SmartCopy(strTestFile, strPath2)
            self.assertItemsEqual(os.listdir(strPath2), ['test.txt',
                                        'test (copy).txt', 'test (copy 1).txt'])
            with open(strCheckFile, 'rt') as fFile:
                self.assertEqual(strCheckSum,
                                        hashlib.md5(fFile.read()).hexdigest())
            self.assertAlmostEqual(dModTime, os.path.getmtime(strCheckFile), 4)
        with open(strTestFile, 'wt') as fFile:
            fFile.write('4')
        with open(strTestFile, 'rt') as fFile:
            strCheckSum = hashlib.md5(fFile.read()).hexdigest()
        dModTime = os.path.getmtime(strTestFile)
        strCheckFile = os.path.join(strPath2, 'test (copy 2).txt')
        for _ in [1,2]:
            TestModule.SmartCopy(strTestFile, strPath2)
            self.assertItemsEqual(os.listdir(strPath2), ['test.txt',
                'test (copy).txt', 'test (copy 1).txt', 'test (copy 2).txt'])
            with open(strCheckFile, 'rt') as fFile:
                self.assertEqual(strCheckSum,
                                        hashlib.md5(fFile.read()).hexdigest())
            self.assertAlmostEqual(dModTime, os.path.getmtime(strCheckFile), 4)
        shutil.rmtree(strPath1)
        shutil.rmtree(strPath2)
        self.assertFalse(os.path.isdir(strPath1))
        self.assertFalse(os.path.isdir(strPath2))
    
    def test_RemoveEmptyFolders(self):
        """
        Tests the performance of the function RemoveEmptyFolders().

        Test ID - TEST-T-520. Covers requirement REQ-FUN-520.
        """
        strRoot = os.path.join(TEST_ROOT, 'test_res')
        strPath1 = os.path.join(strRoot, 'a', 'b')
        strPath2 = os.path.join(strRoot, 'a', 'c', 'd')
        TestModule.TouchFolder(strPath1)
        TestModule.TouchFolder(strPath2)
        strFile1 = os.path.join(strPath1, 'test.txt')
        strFile2 = os.path.join(strPath2, 'test.txt')
        self.assertItemsEqual(os.listdir(os.path.join(strRoot, 'a')),['b', 'c'])
        for strFile in [strFile1, strFile2]:
            with open(strFile, 'wt') as fFile:
                fFile.write('test')
            self.assertTrue(os.path.isfile(strFile))
        os.remove(strFile2)
        self.assertFalse(os.path.isfile(strFile2))
        self.assertTrue(os.path.isdir(strPath2))
        TestModule.RemoveEmptyFolders(strRoot)
        self.assertItemsEqual(os.listdir(os.path.join(strRoot, 'a')), ['b'])
        self.assertTrue(os.path.isfile(strFile1))
        os.remove(strFile1)
        TestModule.RemoveEmptyFolders(strRoot)
        self.assertEqual(len(os.listdir(strRoot)), 0)
        TestModule.RemoveEmptyFolders(strRoot)
        self.assertEqual(len(os.listdir(strRoot)), 0)
        self.assertTrue(os.path.isdir(strRoot))
        shutil.rmtree(strRoot)
        self.assertFalse(os.path.isdir(strRoot))

    def test_RemoveDuplicateFiles(self):
        """
        Tests the performance of the function RemoveDuplicateFiles().

        Test ID - TEST-T-530. Covers requirement REQ-FUN-530.
        """
        strRoot = os.path.join(TEST_ROOT, 'test_rdf')
        TestModule.TouchFolder(strRoot)
        strTestFile = os.path.join(strRoot, 'test.txt')
        with open(strTestFile, 'wt') as fFile:
            fFile.write('test')
        for strFolder in ['a', 'b', 'c']:
            strSubFolder = os.path.join(strRoot, strFolder)
            TestModule.TouchFolder(strSubFolder)
            TestModule.SmartCopy(strTestFile, strSubFolder)
            self.assertTrue(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
        time.sleep(1) # to ensure  different date-time stamp
        with open(os.path.join(strRoot, 'c', 'test.txt'), 'wt') as fFile:
            fFile.write('test')
        #+ by date
        TestModule.RemoveDuplicateFiles(strRoot)
        strTestFile = os.path.join(strRoot, 'c', 'test.txt')
        self.assertTrue(os.path.isfile(strTestFile))
        self.assertFalse(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        for strFolder in ['a', 'b']:
            strSubFolder = os.path.join(strRoot, strFolder)
            self.assertFalse(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
            TestModule.SmartCopy(strTestFile, strSubFolder)
            self.assertTrue(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
        TestModule.SmartCopy(strTestFile, strRoot)
        self.assertTrue(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        #+ in root
        TestModule.RemoveDuplicateFiles(strRoot)
        strTestFile = os.path.join(strRoot, 'test.txt')
        self.assertTrue(os.path.isfile(strTestFile))
        for strFolder in ['a', 'b', 'c']:
            strSubFolder = os.path.join(strRoot, strFolder)
            self.assertFalse(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
            TestModule.SmartCopy(strTestFile, strSubFolder)
            self.assertTrue(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
        #+ by preferred path - first is not empty
        TestModule.RemoveDuplicateFiles(strRoot, ['a', 'b'])
        strTestFile = os.path.join(strRoot, 'a', 'test.txt')
        self.assertTrue(os.path.isfile(strTestFile))
        self.assertFalse(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        for strFolder in ['b', 'c']:
            strSubFolder = os.path.join(strRoot, strFolder)
            self.assertFalse(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
            TestModule.SmartCopy(strTestFile, strSubFolder)
            self.assertTrue(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
        TestModule.SmartCopy(strTestFile, strRoot)
        self.assertTrue(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        #+ by preferred path - first is not empty
        TestModule.RemoveDuplicateFiles(strRoot, ['b', 'a'])
        strTestFile = os.path.join(strRoot, 'b', 'test.txt')
        self.assertTrue(os.path.isfile(strTestFile))
        self.assertFalse(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        for strFolder in ['a', 'c']:
            strSubFolder = os.path.join(strRoot, strFolder)
            self.assertFalse(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
            TestModule.SmartCopy(strTestFile, strSubFolder)
            self.assertTrue(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
        TestModule.SmartCopy(strTestFile, strRoot)
        self.assertTrue(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        #+ by preferred path - first is empty
        os.remove(strTestFile)
        TestModule.RemoveDuplicateFiles(strRoot, ['b', 'a'])
        strTestFile = os.path.join(strRoot, 'a', 'test.txt')
        self.assertTrue(os.path.isfile(strTestFile))
        self.assertFalse(os.path.isfile(os.path.join(strRoot, 'test.txt')))
        for strFolder in ['b', 'c']:
            strSubFolder = os.path.join(strRoot, strFolder)
            self.assertFalse(os.path.isfile(os.path.join(strSubFolder,
                                                                'test.txt')))
        shutil.rmtree(strRoot)
        self.assertFalse(os.path.isdir(strRoot))
    
    def test_RemoveFilesCopies(self):
        """
        Tests the performance of the function RemoveFilesCopies().

        Test ID - TEST-T-540. Covers requirement REQ-FUN-540.
        """
        strRoot = os.path.join(TEST_ROOT, 'test_rfc')
        TestModule.TouchFolder(os.path.join(strRoot, 'test'))
        for strName in ['a.txt', 'b.txt', 'aa.txt']:
            strPath = os.path.join(strRoot, strName)
            with open(strPath, 'wt') as fFile:
                fFile.write('test')
            self.assertTrue(os.path.isfile(strPath))
            strPath = os.path.join(strRoot, 'test', strName)
            with open(strPath, 'wt') as fFile:
                fFile.write('test')
            self.assertTrue(os.path.isfile(strPath))
        for strName in ['c.txt', 'd.txt', 'cc.txt']:
            strPath = os.path.join(strRoot, strName)
            with open(strPath, 'wt') as fFile:
                fFile.write('test another')
            self.assertTrue(os.path.isfile(strPath))
        TestModule.RemoveFilesCopies(strRoot)
        self.assertItemsEqual(os.listdir(strRoot), ['test', 'a.txt', 'c.txt'])
        self.assertItemsEqual(os.listdir(os.path.join(strRoot, 'test')),
                                                                    ['a.txt'])
        shutil.rmtree(strRoot)
        self.assertFalse(os.path.isdir(strRoot))
    
    def test_RenameSubFolders(self):
        """
        Tests the performance of the function RenameSubFolders().

        Test ID - TEST-T-550. Covers requirement REQ-FUN-550.
        """
        strRoot = os.path.join(TEST_ROOT, 'test_rf')
        TestModule.TouchFolder(os.path.join(strRoot, 'a', 'b'))
        TestModule.TouchFolder(os.path.join(strRoot, 'a', 'c', 'd'))
        TestModule.TouchFolder(os.path.join(strRoot, 'a', 'c', 'tEst'))
        TestModule.TouchFolder(os.path.join(strRoot, 'a', 'e'))
        strPath = os.path.join(strRoot, 'a', 'b', 'test.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test')
        with open(strPath, 'rt') as fFile:
            strCheckSum1 = hashlib.md5(fFile.read()).hexdigest()
        dModTime1 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'a', 'c', 'd', 'test.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test')
        with open(strPath, 'rt') as fFile:
            strCheckSum2 = hashlib.md5(fFile.read()).hexdigest()
        dModTime2 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'a', 'c', 'tEst', 'test.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test another')
        with open(strPath, 'rt') as fFile:
            strCheckSum3 = hashlib.md5(fFile.read()).hexdigest()
        dModTime3 = os.path.getmtime(strPath)
        TestModule.RenameSubFolders(strRoot, 'test', ['b', 'd'])
        self.assertItemsEqual(os.listdir(strRoot), ['a'])
        self.assertItemsEqual(os.listdir(os.path.join(strRoot, 'a')),
                                                                ['c', 'test'])
        self.assertItemsEqual(os.listdir(os.path.join(strRoot, 'a', 'c')),
                                                                    ['test'])
        self.assertItemsEqual(os.listdir(os.path.join(strRoot, 'a', 'c',
                                            'test')),
                                             ['test.txt', 'test (copy).txt'])
        strPath = os.path.join(strRoot, 'a', 'test', 'test.txt')
        with open(strPath, 'rt') as fFile:
            strCheckSum = hashlib.md5(fFile.read()).hexdigest()
        self.assertEqual(strCheckSum, strCheckSum1)
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime1, 4)
        for strName in ['test.txt', 'test (copy).txt']:
            strPath = os.path.join(strRoot, 'a', 'c', 'test', strName)
            with open(strPath, 'rt') as fFile:
                strCheckSum = hashlib.md5(fFile.read()).hexdigest()
            if strCheckSum == strCheckSum2:
                self.assertAlmostEqual(os.path.getmtime(strPath), dModTime2, 4)
            elif strCheckSum == strCheckSum3:
                self.assertAlmostEqual(os.path.getmtime(strPath), dModTime3, 4)
            else:
                self.assertTrue(strCheckSum in [strCheckSum2, strCheckSum3])
        shutil.rmtree(strRoot)
        self.assertFalse(os.path.isdir(strRoot))
    
    def test_CopyNonPresent(self):
        """
        Tests the performance of the function CopyNonPresent().

        Test ID - TEST-T-560. Covers requirement REQ-FUN-560.
        """
        strRoot = os.path.join(TEST_ROOT, 'test_cnp')
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'b'))
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'c', 'd'))
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'c', 'e'))
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'f'))
        strPath = os.path.join(strRoot, 'source', 'b', 'a.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test')
        with open(strPath, 'rt') as fFile:
            strCheckSum1 = hashlib.md5(fFile.read()).hexdigest()
        dModTime1 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'source', 'c', 'd', 'b.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test')
        with open(strPath, 'rt') as fFile:
            strCheckSum2 = hashlib.md5(fFile.read()).hexdigest()
        dModTime2 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'source', 'c', 'e', 'a.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test another')
        with open(strPath, 'rt') as fFile:
            strCheckSum3 = hashlib.md5(fFile.read()).hexdigest()
        dModTime3 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'source', 'f', 'c.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test another')
        with open(strPath, 'rt') as fFile:
            strCheckSum4 = hashlib.md5(fFile.read()).hexdigest()
        dModTime4 = os.path.getmtime(strPath)
        strSource = os.path.join(strRoot, 'source')
        strTarget = os.path.join(strRoot, 'target')
        shutil.copytree(strSource, strTarget)
        shutil.rmtree(os.path.join(strRoot, 'source', 'b'))
        shutil.rmtree(os.path.join(strRoot, 'target', 'c'))
        TestModule.CopyNonPresent(strTarget, strSource)
        strPath = os.path.join(strTarget, 'b', 'a.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime1, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum1)
        strPath = os.path.join(strTarget, 'f', 'c.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime4, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum4)
        strPath = os.path.join(strTarget, 'a_1.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime3, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum3)
        strPath = os.path.join(strTarget, 'b.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime2, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum2)
        shutil.rmtree(strRoot)
        self.assertFalse(os.path.isdir(strRoot))
    
    def test_CopyMerge(self):
        """
        Tests the performance of the function CopyMerge().

        Test ID - TEST-T-570. Covers requirement REQ-FUN-570.
        """
        strRoot = os.path.join(TEST_ROOT, 'test_cm')
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'b'))
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'c', 'd'))
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'c', 'e'))
        TestModule.TouchFolder(os.path.join(strRoot, 'source', 'f'))
        strPath = os.path.join(strRoot, 'source', 'b', 'a.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test')
        with open(strPath, 'rt') as fFile:
            strCheckSum1 = hashlib.md5(fFile.read()).hexdigest()
        dModTime1 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'source', 'c', 'd', 'b.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test')
        with open(strPath, 'rt') as fFile:
            strCheckSum2 = hashlib.md5(fFile.read()).hexdigest()
        dModTime2 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'source', 'c', 'e', 'a.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test another')
        with open(strPath, 'rt') as fFile:
            strCheckSum3 = hashlib.md5(fFile.read()).hexdigest()
        dModTime3 = os.path.getmtime(strPath)
        strPath = os.path.join(strRoot, 'source', 'f', 'c.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test another')
        with open(strPath, 'rt') as fFile:
            strCheckSum4 = hashlib.md5(fFile.read()).hexdigest()
        dModTime4 = os.path.getmtime(strPath)
        strSource = os.path.join(strRoot, 'source')
        strTarget = os.path.join(strRoot, 'target')
        shutil.copytree(strSource, strTarget)
        shutil.rmtree(os.path.join(strRoot, 'source', 'b'))
        shutil.rmtree(os.path.join(strRoot, 'target', 'c', 'd'))
        strPath = os.path.join(strRoot, 'target', 'c', 'e', 'a.txt')
        with open(strPath, 'wt') as fFile:
            fFile.write('test yet another')
        TestModule.CopyMerge(strSource, strTarget)
        strPath = os.path.join(strTarget, 'b', 'a.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime1, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum1)
        strPath = os.path.join(strTarget, 'f', 'c.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime4, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum4)
        strPath = os.path.join(strTarget, 'c', 'e', 'a (copy).txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime3, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum3)
        strPath = os.path.join(strTarget, 'c', 'd', 'b.txt')
        self.assertAlmostEqual(os.path.getmtime(strPath), dModTime2, 4)
        with open(strPath, 'rt') as fFile:
            self.assertEqual(hashlib.md5(fFile.read()).hexdigest(),strCheckSum2)
        self.assertTrue(os.path.isfile(os.path.join(strRoot, 'target', 'c', 'e',
                                                                    'a.txt')))
        shutil.rmtree(strRoot)
        self.assertFalse(os.path.isdir(strRoot))

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_fs_maitenance)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.fs_maintenance module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)