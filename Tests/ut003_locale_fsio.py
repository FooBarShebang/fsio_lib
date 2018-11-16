#!/usr/bin/python
"""
Module Tests.ut003_locale_fsio

Implements unit testing of the module locale_fsio. Test ID - UT003
"""

__version__ = "0.1.0.1"
__date__ = "15-11-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import random

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.locale_fsio as TestModule

# checks on existance of the output folder

strTemp = os.path.join(LIB_ROOT, 'Tests', 'Output')

if not os.path.isdir(strTemp):
    os.mkdir(strTemp)

#helper functions

def GenerateString():
    """
    Returns a random ASCII string.
    
    Signature:
        None -> str
    """
    iLength = random.randint(1, 11)
    strResult = ''.join([chr(random.randint(32, 127)) for _ in range(iLength)])
    return strResult

def GenerateStringsList():
    """
    Returns a rnadom length list of random ASCII strings.
    
    Signature:
        None -> list(str)
    """
    iLength = random.randint(20, 30)
    strlstResult = [GenerateString() for _ in range(iLength)]
    return strlstResult

#classes

#+ test cases

class Test_LineEndings(unittest.TestCase):
    """
    Test cases for the function LineEndings of the module locale_fsio.
    
    Test ID - UT003.1.1
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunc = staticmethod(TestModule.SaveForcedNewLine)
        cls.TestData = GenerateStringsList()
        cls.FileBase = 'ut003_1'
        cls.FileExtension = 'txt'
        cls.OutFolder = os.path.join(LIB_ROOT, 'Tests', 'Output')
    
    def test_LF(self):
        """
        Forced LF ending.
        
        Test ID - UT003.1.1
        """
        strFileName = '{}-{}.{}'.format(self.FileBase, 'LF', self.FileExtension)
        strFileName = os.path.join(self.OutFolder, strFileName)
        strExpected = '{}{}'.format('\n'.join(self.TestData), '\n')
        self.TestFunc(strFileName, self.TestData, '\n')
        with open(strFileName, 'rb') as fFile:
            strResult = fFile.read()
        self.assertEqual(strExpected, strResult)
    
    def test_CR(self):
        """
        Forced CR ending.
        
        Test ID - UT003.1.1
        """
        strFileName = '{}-{}.{}'.format(self.FileBase, 'CR', self.FileExtension)
        strFileName = os.path.join(self.OutFolder, strFileName)
        strExpected = '{}{}'.format('\r'.join(self.TestData), '\r')
        self.TestFunc(strFileName, self.TestData, '\r')
        with open(strFileName, 'rb') as fFile:
            strResult = fFile.read()
        self.assertEqual(strExpected, strResult)
    
    def test_CRLF(self):
        """
        Forced CRLF ending.
        
        Test ID - UT003.1.1
        """
        strFileName='{}-{}.{}'.format(self.FileBase, 'CRLF', self.FileExtension)
        strFileName = os.path.join(self.OutFolder, strFileName)
        strExpected = '{}{}'.format('\r\n'.join(self.TestData), '\r\n')
        self.TestFunc(strFileName, self.TestData, '\r\n')
        with open(strFileName, 'rb') as fFile:
            strResult = fFile.read()
        self.assertEqual(strExpected, strResult)
    
    def test_DEF(self):
        """
        Default line ending - should be 'CRLF'
        
        Test ID - UT003.1.1
        """
        strFileName='{}-{}.{}'.format(self.FileBase, 'DEF', self.FileExtension)
        strFileName = os.path.join(self.OutFolder, strFileName)
        strExpected = '{}{}'.format('\r\n'.join(self.TestData), '\r\n')
        self.TestFunc(strFileName, self.TestData)
        with open(strFileName, 'rb') as fFile:
            strResult = fFile.read()
        self.assertEqual(strExpected, strResult)

class Test_DetectNotation(unittest.TestCase):
    """
    Test cases for the function DetectNotation of the module locale_fsio.
    
    Test ID - UT003.2.1
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunc = staticmethod(TestModule.DetectNotation)
        cls.Notations = [
            [['a', '1', '12.03E3', '100,000'], 0], #RE_INT1
            [['a', '1', '12,03E3', '100.000'], 1], #RE_NL1
            [['a', '1', '12,100,100', '100,000'], 0], #RE_INT2
            [['a', '1', '12.100.100', '100.000'], 1], #RE_NL2
            [['a', '1', '12,100.10', '100,000'], 0], #RE_INT3
            [['a', '1', '12.100,10', '100.000'], 1], #RE_NL3
            [['a', '1', '12.10', '100,000'], 0], #RE_INT4
            [['a', '1', '12,10', '100.000'], 1], #RE_NL4
            [['a', '1', '12.1000', '100,000'], 0], #RE_INT4
            [['a', '1', '12,1000', '100.000'], 1], #RE_NL4
            [['a', '1', '12,', '100.000'], 1], #RE_NL5
            [['a', '1', '1203,000', '100.000'], 1], #RE_NL5
            [['a', '1', '1203', '100000'], 0], #default
            [['a', '1', '120.3', '1000.00'], 0], #default
        ]
    
    def test_Notation(self):
        """
        Test concerning the detection of the numbers notation INT / NL.
        
        Test ID - UT003.2.1
        """
        for strlstTest, bExpResult in self.Notations:
            bResult = self.TestFunc(strlstTest)
            self.assertEqual(bResult, bExpResult)

class Test_ConvertFromString(unittest.TestCase):
    """
    Test cases for the function ConvertFromString of the module locale_fsio.
    
    Test ID - UT003.3.1
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunc = staticmethod(TestModule.ConvertFromString)
        cls.TestDutch = ['a', '', '1', '12,03E3', '12.100.100', '12.100,10',
                            '12,10', '12,1000', '1203,000']
        cls.DutchResult = ['a', '', 1, 12.03E3, 12100100, 12100.10,
                            12.10, 12.1000, 1203.000]
        cls.TestInt = ['a', '', '1', '12.03E3', '12,100,100', '12,100.10',
                            '12.10', '12.1000', '1203.000']
        cls.IntResult = ['a', '', 1, 12.03E3, 12100100, 12100.10,
                            12.10, 12.1000, 1203.000]
    
    def test_Conversion(self):
        """
        Test concerning the proper string -> integer / float conversion of the
        quoted numbers (in strings) stored in INT / NL notation with possible
        inclusion of the decimal delimiters.
        
        See REQ-FUN5
        """
        for iIdx, strTest in enumerate(self.TestDutch):
            gExpResult = self.DutchResult[iIdx]
            gResult = self.TestFunc(strTest, 1)
            self.assertEqual(gExpResult, gResult)
        for iIdx, strTest in enumerate(self.TestInt):
            gExpResult = self.IntResult[iIdx]
            gResult = self.TestFunc(strTest, 0)
            self.assertEqual(gExpResult, gResult)

class Test_LoadLines(unittest.TestCase):
    """
    Test cases for the function LoadLines of the module locale_fsio.
    
    Test ID - UT003.4
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunc = staticmethod(TestModule.LoadLines)
        cls.SaveFunc = staticmethod(TestModule.SaveForcedNewLine)
        cls.TempFile = os.path.join(LIB_ROOT, 'Tests', 'Output', 'temp.txt')
        cls.TestData = ['as', '1', '1.3', '1,3E-2', '1 ', '2  2.5   ', '3\t',
                        '4\t\t4.5\t', '5\t   \t  ', '', '6  \t   \t']
    
    def test_LoadLines(self):
        """
        The function properly splits a text file into lines regardless of the
        used new line convention: LF, CR or CRLF. Proper treatment of the line
        endings, their proper removal and preservation of the tailing TABs and
        spaces.
        
        Test ID - UT003.4.1
        """
        #default ending
        self.SaveFunc(self.TempFile, self.TestData)
        strlstResult = self.TestFunc(self.TempFile)
        self.assertEqual(self.TestData, strlstResult)
        for strEnding in ['\r', '\n', '\r\n']:
            self.SaveFunc(self.TempFile, self.TestData, strEnding)
            strlstResult = self.TestFunc(self.TempFile)
            self.assertEqual(self.TestData, strlstResult)
        os.remove(self.TempFile)
    
    def test_LoadSkipLines(self):
        """
        Proper treatment of the line endings, their proper removal and
        preservation of the tailing TABs and spaces and skipping of the lines.
        
        Test ID - UT003.4.2
        """
        #default ending
        self.SaveFunc(self.TempFile, self.TestData)
        strlstResult = self.TestFunc(self.TempFile, 3)
        self.assertEqual(self.TestData[3:], strlstResult)
        for iIndex in range(0,4):
            for strEnding in ['\r', '\n', '\r\n']:
                self.SaveFunc(self.TempFile, self.TestData, strEnding)
                strlstResult = self.TestFunc(self.TempFile, iIndex)
                self.assertEqual(self.TestData[iIndex:], strlstResult)
        os.remove(self.TempFile)

class Test_SplitLine(unittest.TestCase):
    """
    Test cases for the function SplitLine of the module locale_fsio.
    
    Test ID - UT003.5.1
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunc = staticmethod(TestModule.SplitLine)
        cls.TestData = ['as', '1', '1.3', '1,3E-2', '1 ', '2  2.5   ', '3\t',
                        '4\t\t4.5\t', '5\t   \t  ', '', '6  \t   \t',
                        '\t6', ' 6']
        cls.ExpectedData = [['as'], ['1'], ['1.3'], ['1,3E-2'], ['1', ''],
                            ['2', '2.5', ''], ['3', ''], ['4', '', '4.5', ''],
                            ['5', '', '', '', ''], [''], ['6', '', '', '', ''],
                            ['', '6'], ['', '6']]
    
    def test_SplitLine(self):
        """
        Proper splitting of a line into columns by TABs or usual spaces,
        including the leading / tailing TAB / spaces.
        
        Test ID - UT003.5.1
        """
        for iIdx, strLine in enumerate(self.TestData):
            strlstResult = self.TestFunc(strLine)
            self.assertEqual(strlstResult, self.ExpectedData[iIdx])

class Test_LoadTable(unittest.TestCase):
    """
    Test cases for the function LoadTable of the module locale_fsio -
    integration test.
    
    Test ID - UT003.6.1
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunc = staticmethod(TestModule.LoadTable)
        strOutFolder = os.path.join(LIB_ROOT, 'Tests', 'Input')
        cls.TestFBR = os.path.join(strOutFolder, 'test.fbr')
        cls.TestLIN = os.path.join(strOutFolder, 'test.lin')
        cls.TestLMP = os.path.join(strOutFolder, 'test.lmp')
        cls.TestSP = os.path.join(strOutFolder, 'test_sp.txt')
    
    def test_LoadFBR(self):
        """
        Single column. CRLF line end. Mixed data - str + int + float in dutch
        scientific notation.
        
        Test ID - UT003.6.1
        """
        Result = self.TestFunc(self.TestFBR)
        self.assertEqual(len(Result), 2053)
        for lstItem in Result:
            self.assertEqual(len(lstItem), 1)
        self.assertTrue(isinstance(Result[0][0], str))
        self.assertTrue(isinstance(Result[2][0], int))
        self.assertEqual(Result[2][0], 18)
        self.assertTrue(isinstance(Result[4][0], float))
        self.assertAlmostEqual(Result[4][0], 1.0E10)
        self.assertTrue(isinstance(Result[175][0], float))
        self.assertAlmostEqual(Result[175][0], 234.1808)
    
    def test_LoadLMP(self):
        """
        Two columns, spaces. CRLF line end. Floats in international notation.
        
        Test ID - UT003.6.1
        """
        Result = self.TestFunc(self.TestLMP)
        self.assertEqual(len(Result), 701)
        for lstItem in Result:
            self.assertEqual(len(lstItem), 2)
        self.assertTrue(isinstance(Result[25][0], float))
        self.assertTrue(isinstance(Result[25][1], float))
        self.assertAlmostEqual(Result[25][0], 325.0)
        self.assertAlmostEqual(Result[25][1], 0.01090)
    
    def test_LoadLIN(self):
        """
        Three columns, tabs and spaces (variable length). LF line end. Mixed
        data: ints, floats in international notation and strings.
        
        Test ID - UT003.6.1
        """
        Result = self.TestFunc(self.TestLIN)
        self.assertEqual(len(Result), 3)
        for lstItem in Result:
            self.assertEqual(len(lstItem), 3)
            self.assertTrue(isinstance(lstItem[0], int))
            self.assertTrue(isinstance(lstItem[1], float))
            self.assertTrue(isinstance(lstItem[2], str))
        self.assertEqual(Result[1][0], 2)
        self.assertAlmostEqual(Result[1][1], 2.0)
        self.assertEqual(Result[1][2], 'a')
    
    def test_LoadSP_TXT(self):
        """
        Three columns, tabsspaces (variable length). CRLF line end. Mixed
        data: ints and floats in dutch notation with delimiters.
        
        Test ID - UT003.6.1
        """
        Result = self.TestFunc(self.TestSP, 2)
        self.assertEqual(len(Result), 2048)
        for lstItem in Result:
            self.assertEqual(len(lstItem), 3)
            self.assertTrue(isinstance(lstItem[0], int))
            self.assertTrue(isinstance(lstItem[1], float))
            self.assertTrue(isinstance(lstItem[2], float))
        self.assertEqual(Result[577][0], 577)
        self.assertAlmostEqual(Result[577][1], 435.196)
        self.assertAlmostEqual(Result[577][2], 1144.86)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_LineEndings)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_DetectNotation)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_ConvertFromString)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_LoadLines)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_SplitLine)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_LoadTable)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4,
                    TestSuite5, TestSuite6])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.locale_fsio module tests...")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
