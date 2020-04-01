#!/usr/bin/python
"""
Module Tests.ut004_generic_parsers

Implements unit testing of the module GenericParsers. See test report TE006.
"""

__version__ = "0.1.0.1"
__date__ = "15-11-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import logging
import copy
import collections
from xml.etree.ElementTree import ParseError

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.GenericParsers as TestModule
from fsio_lib.LoggingFSIO import DualLogger
from fsio_lib.Tests.ut004_helper_class import HelperClass as HelperClass1

#globals - helper test values

TEST_FILES_FOLDER = os.path.join(LIB_ROOT, 'Tests', 'Input')

# checks on existance of the output folder

strTemp = os.path.join(LIB_ROOT, 'Tests', 'Output')

if not os.path.isdir(strTemp):
    os.mkdir(strTemp)

#classes

#+ helper class

class HelperClass(object):
    def __init__(self):
        self.report = {"id" : None, "type" : None}
        self.result = None

#+ test cases

class Test_GenericParser(unittest.TestCase):
    """
    Test cases for the class GenericParser of the module GenericParsers.
    
    Test IDs - TEST-T-600, TEST-T-601, TEST-T-602, TEST-T-603, TEST-T-604,
    TEST-T-605, TEST-T-606 and TEST-T-607.
    """
    
    TestID = "ut004_1"
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = TestModule.GenericParser
        cls.Logger = DualLogger(cls.__name__, bLogToFile = True,
                            strFileName = os.path.join(LIB_ROOT, 'Tests',
                                        'Output', '{}.log'.format(cls.TestID)))
        cls.Logger.setFileLoggingLevel(logging.INFO)
        cls.Logger.disableConsoleLogging()
        cls.InFolder = os.path.join(LIB_ROOT, 'Tests', 'Input')
        cls.DummyFile = 'good_1.json'
        cls.DummyFileZero = 'good_1.json'
        cls.NotStringNames = [1, 1.0, {"a" : "b"}, True, int, float, str, dict]
    
    def test_NoDataNoTemplate(self):
        """
        Methods parseFile() and parseManyFiles() raise ValueError if no template
        is provided (explicit or default None value) and it cannot be guessed by
        the file content.
        
        Test ID - TEST-T-600. Covers requirements REQ-AWM-600.
        """
        strFile = os.path.join(self.InFolder, self.DummyFileZero)
        with self.assertRaises(ValueError):
            self.TestClass.parseFile(strFile, dictTemplate = None,
                                                        objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFileZero],
                                dictTemplate = None, objLogger = self.Logger)
    
    def test_RaisesTypeErrorFiles(self):
        """
        Method parseFile() must raise TypeError if the file name is not a string
        and method parseManyFiles() must raise TypeError if either the folder
        name or any of the file names are not a string.
        
        Test ID - TEST-T-601. Covers requirements REQ-AWM-601.
        """
        for Name in self.NotStringNames:
            with self.assertRaises(TypeError):
                self.TestClass.parseFile(Name, objLogger = self.Logger)
            with self.assertRaises(TypeError):
                self.TestClass.parseManyFiles(Name, ["a"],
                                                    objLogger = self.Logger)
            with self.assertRaises(TypeError):
                self.TestClass.parseManyFiles("a", Name,
                                                    objLogger = self.Logger)
    
    def test_RaisesValueErrorNotFile(self):
        """
        Methods parseFile() and parseManyFiles() raise ValueError if, at least,
        one file path does not point to an existing file. Method
        parseManyFiles() also raises ValueError if the folder path argument does
        not point to an existing folder.
        
        Test ID - TEST-T-602. Covers requirements REQ-AWM-602.
        """
        strFile = os.path.join(self.InFolder, 'foo_bar.baz')
        with self.assertRaises(ValueError):
            self.TestClass.parseFile(strFile, objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestClass.parseManyFiles(self.InFolder, ['foo_bar.baz'],
                                                        objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestClass.parseManyFiles('foo', ['foo_bar.baz'],
                                                        objLogger = self.Logger)
    
    def test_RaisesTypeErrorTemplateNotDict(self):
        """
        Methods parseSingleObject(), parseFile() and parseManyFiles() raise
        TypeError if the template agrument is not a template (but not None).
        
        Test ID - TEST-T-603. Covers requirements REQ-AWM-603.
        """
        lstTests = [1, 1.0, True, "a", ["a"], int, float, bool, list, tuple]
        strFile = os.path.join(self.InFolder, self.DummyFile)
        for gTest in lstTests:
            with self.assertRaises(TypeError):
                self.TestClass.parseSingleObject({}, dict, gTest,
                                                        objLogger = self.Logger)
            with self.assertRaises(TypeError):
                self.TestClass.parseFile(strFile, dictTemplate = gTest,
                                                        objLogger = self.Logger)
            with self.assertRaises(TypeError):
                self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                                dictTemplate = gTest, objLogger = self.Logger)
    
    def test_RaisesValueErrorTemplateDataMapping(self):
        """
        Methods parseSingleObject(), parseFile() and parseManyFiles() raise
        ValueError if the template does not have the key 'DataMapping' or the
        value bound to this key is not a dictionary.
        
        Test ID - TEST-T-604. Covers requirements REQ-AWM-604.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        with self.assertRaises(ValueError):
            self.TestClass.parseSingleObject({}, dict, {},
                                                        objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestClass.parseFile(strFile, dictTemplate = {},
                                                        objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                                    dictTemplate = {}, objLogger = self.Logger)
        lstTests = [1, 1.0, True, "a", ["a"], int, float, bool, list, tuple]
        for gTest in lstTests:
            dictMapping = {'DataMapping' : gTest}
            with self.assertRaises(ValueError):
                self.TestClass.parseSingleObject({}, dict, dictMapping,
                                                        objLogger = self.Logger)
            with self.assertRaises(ValueError):
                self.TestClass.parseFile(strFile, dictTemplate = dictMapping,
                                                        objLogger = self.Logger)
            with self.assertRaises(ValueError):
                self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                            dictTemplate = dictMapping, objLogger = self.Logger)
    
    def test_RaiseTypeValueErrorMappingObject(self):
        """
        The methods parseSingleObject(), parseFile() and parseManyFiles() raise
        TypeError or ValueError if the mapping dictionary is not of the proper
        format (DE001 DSL specifications). Regardless of the bStrictSource and
        bStrictTarget flags. Note, the parseFile() and parseManyFiles() methods
        are checked only with the derived test clases, not this one.
        
        Test ID - TEST-T-605. Covers requirements REQ-AWM-605.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        #bad target path elements
        lstBadElements = ["a.b", -1, 1.0, "-1", "1.0", "_", "#a", "$b", "+a",
                            "-a", (1,)]
                            
        BadMappingTestCases = [{Item : 'a'} for Item in lstBadElements] #top
        BadMappingTestCases.extend([{"a":{Item : 'a'}}
                                            for Item in lstBadElements]) #nested
        #bad source path elements
        lstBadElements = [1.0, True, False, int, float, bool, [1.0],
                (True, ), [{1 : "name"}], [{True : "name"}], [1, {1 : "name"}],
                [{"name" : [1]}], [{"name" : (1, 2)}], -1, [-1], (2, [-1]), '',
                [''], '#', '$', ["#"], ['$'], [], tuple()]
        BadMappingTestCases.extend([{"a" : Item}
                                            for Item in lstBadElements]) #top
        BadMappingTestCases.extend([{"a" : {"b" : Item}}
                                            for Item in lstBadElements]) #nested
        for gTestObject in BadMappingTestCases:
            dictMapping = {'DataMapping' : gTestObject}
            for TargetFlag in [True, False]:
                for SourceFlag in [True, False]:
                    with self.assertRaises((TypeError, ValueError)):
                        self.TestClass.parseSingleObject({}, dict, dictMapping,
                            objLogger = self.Logger, bStrictTarget = TargetFlag,
                                                    bStrictSource = SourceFlag)
                    if not (self.__class__.__name__ == 'Test_GenericParser'):
                        with self.assertRaises((TypeError, ValueError)):
                            self.TestClass.parseFile(strFile, clsTarget = dict,
                                dictTemplate = dictMapping,
                                    objLogger = self.Logger,
                                            bStrictTarget = TargetFlag,
                                                    bStrictSource = SourceFlag)
                        with self.assertRaises((TypeError, ValueError)):
                            self.TestClass.parseManyFiles(self.InFolder,
                                [self.DummyFile], clsTarget = dict,
                                    dictTemplate = dictMapping,
                                        objLogger = self.Logger,
                                            bStrictTarget = TargetFlag,
                                                    bStrictSource = SourceFlag)
    
    def test_RaisesAttributeErrorSource(self):
        """
        The method parseSingleObject() raises Attribute error if the source
        object does not have the required element and the flag bStrictSource is
        True. If the flag bStrictSource is False, the exception is not raised,
        but the corresponding element of the target object is not changed but
        remains at its initial value.
        
        Test ID - TEST-T-606. Covers requirements REQ-AWM-606 and REQ-FUN-604.
        """
        clsTarget = HelperClass
        objSource = dict()
        dictTemplate = {"DataMapping" : {"result" : "a"}}
        with self.assertRaises(AttributeError):
            objResult = self.TestClass.parseSingleObject(objSource, clsTarget,
                    dictTemplate, objLogger = self.Logger, bStrictSource = True)
        objResult = self.TestClass.parseSingleObject(objSource, clsTarget,
                dictTemplate, objLogger = self.Logger, bStrictSource = False)
        self.assertIsInstance(objResult, clsTarget)
        self.assertIsNone(objResult.result)
    
    def test_RaisesAttributeErrorTarget(self):
        """
        The method parseSingleObject() raises Attribute error if the target
        object does not have the required element and the flag bStrictTarget is
        True. If the flag bStrictTarget is False and bForceTarget is False - the
        exception is not raised, but the missing element is not created; if the
        bForceTarget is True - the missing element is created and the proper
        value is assigned to it.
        
        Test ID - TEST-T-607. Covers requirements REQ-AWM-607 and REQ-FUN-604.
        """
        clsTarget = HelperClass
        objSource = {"a" : 1}
        dictTemplate = {"DataMapping" : {"result1" : "a"}}
        with self.assertRaises(AttributeError):
            objResult = self.TestClass.parseSingleObject(objSource, clsTarget,
                    dictTemplate, objLogger = self.Logger, bStrictTarget = True,
                        bForceTarget = True)
        objResult = self.TestClass.parseSingleObject(objSource, clsTarget,
                dictTemplate, objLogger = self.Logger, bStrictTarget = False,
                                                        bForceTarget = False)
        self.assertIsInstance(objResult, clsTarget)
        self.assertFalse(hasattr(objResult, "result1"))
        objResult = self.TestClass.parseSingleObject(objSource, clsTarget,
                dictTemplate, objLogger = self.Logger, bStrictTarget = False,
                                                        bForceTarget = True)
        self.assertIsInstance(objResult, clsTarget)
        self.assertEqual(objResult.result1, 1)

class Test_TSV_Parser(Test_GenericParser):
    """
    Test cases for the class TSV_Parser of the module GenericParsers.
    
    Test IDs - TEST-T-600, TEST-T-601, TEST-T-602, TEST-T-603, TEST-T-604,
    TEST-T-605, TEST-T-606, TEST-T-607, TEST-T-608, TEST-T-609 and TEST-T-60A.
    """
    
    TestID = "ut004_2"
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_TSV_Parser, cls).setUpClass()
        cls.TestClass = TestModule.TSV_Parser
        cls.DummyFile = "dummy.txt"
        cls.DummyFileZero = "dummy.txt"
        cls.Template = {
            "HeaderOffset" : 1,
            "DataMapping" : {
                "report" : {
                    "id" : 0,
                    "type" : 1
                },
                "result" : 2
            }
        }
        cls.TargetClass = HelperClass
    
    def test_RaisesAttributeErrorSourceFiles(self):
        """
        Extension of the test UT004.2.7 onto the methods parseFile() and
        parseManyFiles(). In the case of not raising the exception, only the
        first object returned is tested in terms of its content. The target
        class and the mapping dictionary are provided explicitly.
        
        Test ID - TEST-T-606 part 2. Covers requirements REQ-AWM-606 and
        REQ-FUN-604.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        clsTarget = HelperClass
        dictTestTemplate = copy.deepcopy(self.Template)
        dictTestTemplate["DataMapping"]["result"] = "b"
        with self.assertRaises(AttributeError):
            Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictSource = True)
        with self.assertRaises(AttributeError):
            Result=self.TestClass.parseManyFiles(self.InFolder,[self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictSource = True)
        Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictSource = False)
        objTest = Result[0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertIsNone(objTest.result)
        Result = self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictSource = False)
        objTest = Result[self.DummyFile][0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertIsNone(objTest.result)
        
    def test_RaisesAttributeErrorTargetFiles(self):
        """
        Extension of the test UT004.2.8 onto the methods parseFile() and
        parseManyFiles(). In the case of not raising the exception, only the
        first object returned is tested in terms of its content. The target
        class and the mapping dictionary are provided explicitly. The None
        (explicit or default) value of the flag bStrictTarget in this case is
        treated as True.
        
        Test ID - TEST-T-607 part 2. Covers requirements REQ-AWM-607 and
        REQ-FUN-604.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        clsTarget = HelperClass
        dictTestTemplate = copy.deepcopy(self.Template)
        dictTestTemplate["DataMapping"]["result1"] = (
                                        self.Template["DataMapping"]["result"])
        with self.assertRaises(AttributeError):
            Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = True,
                        bForceTarget = True)
        with self.assertRaises(AttributeError):
            Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = None,
                        bForceTarget = True)
        with self.assertRaises(AttributeError):
            Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bForceTarget = True)
        with self.assertRaises(AttributeError):
            Result=self.TestClass.parseManyFiles(self.InFolder,[self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = True,
                        bForceTarget = True)
        with self.assertRaises(AttributeError):
            Result=self.TestClass.parseManyFiles(self.InFolder,[self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = None,
                        bForceTarget = True)
        with self.assertRaises(AttributeError):
            Result=self.TestClass.parseManyFiles(self.InFolder,[self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bForceTarget = True)
        Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = False,
                        bForceTarget = False)
        objTest = Result[0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertFalse(hasattr(objTest, "result1"))
        Result = self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = False,
                        bForceTarget = False)
        objTest = Result[self.DummyFile][0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertFalse(hasattr(objTest, "result1"))
        Result = self.TestClass.parseFile(strFile,
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = False,
                        bForceTarget = True)
        objTest = Result[0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertEqual(objTest.result1, 1)
        Result = self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                clsTarget = self.TargetClass, dictTemplate = dictTestTemplate,
                    objLogger = self.Logger, bStrictTarget = False,
                        bForceTarget = True)
        objTest = Result[self.DummyFile][0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertEqual(objTest.result1, 1)
    
    def test_CopiesProperlyWithTargetAndTemplate(self):
        """
        The methods parseFile() and parseManyFiles() create the expected number
        of the target objects packed into the expected container types and fill
        them properly when both the target class (type) and the template are
        provided explicitely, and the mapping matches the structure of the both
        source and target objects.
        
        Test ID - TEST-T-608. Covers requirements REQ-FUN-600.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile,
            clsTarget = self.TargetClass, dictTemplate = self.Template,
                objLogger = self.Logger)
        self.assertTrue(isinstance(lstResult, collections.Sequence))
        self.assertFalse(isinstance(lstResult, basestring))
        self.assertEqual(len(lstResult), 2)
        for iIndex, objTest in enumerate(lstResult):
            self.assertIsInstance(objTest, self.TargetClass)
            self.assertEqual(objTest.report["id"], 1)
            self.assertEqual(objTest.report["type"], "dummy")
            self.assertEqual(objTest.result, 1 - iIndex)
        strlstFiles = [self.DummyFile, 'dummy1.txt']
        odResult = self.TestClass.parseManyFiles(self.InFolder, strlstFiles,
            clsTarget = self.TargetClass, dictTemplate = self.Template,
                objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 2)
        for strFile in strlstFiles:
            objlstTest = odResult[strFile]
            for iIndex, objTest in enumerate(objlstTest):
                self.assertIsInstance(objTest, self.TargetClass)
                self.assertEqual(objTest.report["id"], 1)
                self.assertEqual(objTest.report["type"], "dummy")
                self.assertEqual(objTest.result, 1 - iIndex)
    
    def test_CopiesProperlyWithTemplateOnly(self):
        """
        The methods parseFile() and parseManyFiles() create the expected number
        of the target objects packed into the expected container types and fill
        them properly when only the template is provided explicitely, and the
        mapping matches the structure of the both source and target objects. The
        target class (type) is not provided, but taken from the template. All
        flags are left at their default values.
        
        Test ID - TEST-T-609. Covers requirements REQ-FUN-600 and REQ-FUN-602.
        """
        dictTemplate = copy.deepcopy(self.Template)
        dictTemplate["TargetClassModule"] = 'fsio_lib.Tests.ut004_helper_class'
        dictTemplate["TargetClass"] = 'HelperClass'
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile,
            dictTemplate = dictTemplate, objLogger = self.Logger)
        self.assertTrue(isinstance(lstResult, collections.Sequence))
        self.assertFalse(isinstance(lstResult, basestring))
        self.assertEqual(len(lstResult), 2)
        for iIndex, objTest in enumerate(lstResult):
            self.assertIsInstance(objTest, HelperClass1)
            self.assertEqual(objTest.report["id"], 1)
            self.assertEqual(objTest.report["type"], "dummy")
            self.assertEqual(objTest.result, 1 - iIndex)
        strlstFiles = [self.DummyFile, 'dummy1.txt']
        odResult = self.TestClass.parseManyFiles(self.InFolder, strlstFiles,
            dictTemplate = dictTemplate, objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 2)
        for strFile in strlstFiles:
            objlstTest = odResult[strFile]
            for iIndex, objTest in enumerate(objlstTest):
                self.assertIsInstance(objTest, HelperClass1)
                self.assertEqual(objTest.report["id"], 1)
                self.assertEqual(objTest.report["type"], "dummy")
                self.assertEqual(objTest.result, 1 - iIndex)
    
    def test_StrictTargetModeTargetByTemplate(self):
        """
        The default (absent) or explicit **None** value of the *bStrictTarget*
        flag should be treated as **True** if the explicit target class is not
        given but can be derved from the template, or it is the same as the
        suggested by the template. If the explicitly given target class is not
        the same as suggested by the template, the **None** value of the
        *bStrictTarget* flag should be treated as **False**. The explicitly
        specified **True** or **False** values of this flag should not be
        modified in any of the cases.
        
        Test ID - TEST-T-60A. Covers requirements REQ-FUN-604.
        """
        dictTemplate = copy.deepcopy(self.Template)
        dictTemplate["TargetClassModule"] = 'fsio_lib.Tests.ut004_helper_class'
        dictTemplate["TargetClass"] = 'HelperClass'
        dictTemplate["DataMapping"]["result1"] = (
                                        self.Template["DataMapping"]["result"])
        strFile = os.path.join(self.InFolder, self.DummyFile)
        #no explicit target
        #+ default value (None)
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                                                        objLogger = self.Logger)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, objLogger = self.Logger)
        #+ explicit None
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        objLogger = self.Logger, bStrictTarget = None)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, objLogger = self.Logger,
                    bStrictTarget = None)
        #+ explicit True
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        objLogger = self.Logger, bStrictTarget = True)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, objLogger = self.Logger,
                    bStrictTarget = True)
        #+ explicit False
        self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        objLogger = self.Logger, bStrictTarget = False)
        self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, objLogger = self.Logger,
                    bStrictTarget = False)
        #explicit target == suggested
        #+ default value (None)
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                    clsTarget = HelperClass1, objLogger = self.Logger)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass1,
                    objLogger = self.Logger)
        #+ explicit None
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        clsTarget = HelperClass1, objLogger = self.Logger,
                            bStrictTarget = None)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass1,
                    objLogger = self.Logger, bStrictTarget = None)
        #+ explicit True
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        clsTarget = HelperClass1, objLogger = self.Logger,
                            bStrictTarget = True)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass1,
                    objLogger = self.Logger, bStrictTarget = True)
        #+ explicit False
        self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        clsTarget = HelperClass1, objLogger = self.Logger,
                            bStrictTarget = False)
        self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass1,
                    objLogger = self.Logger, bStrictTarget = False)
        #explicit target != suggested
        #+ default value (None)
        self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                    clsTarget = HelperClass, objLogger = self.Logger)
        self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass,
                    objLogger = self.Logger)
        #+ explicit None
        self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        clsTarget = HelperClass, objLogger = self.Logger,
                            bStrictTarget = None)
        self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass,
                    objLogger = self.Logger, bStrictTarget = None)
        #+ explicit True
        with self.assertRaises(AttributeError):
            self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        clsTarget = HelperClass, objLogger = self.Logger,
                            bStrictTarget = True)
        with self.assertRaises(AttributeError):
            self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass,
                    objLogger = self.Logger, bStrictTarget = True)
        #+ explicit False
        self.TestClass.parseFile(strFile, dictTemplate = dictTemplate,
                        clsTarget = HelperClass, objLogger = self.Logger,
                            bStrictTarget = False)
        self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                dictTemplate = dictTemplate, clsTarget = HelperClass,
                    objLogger = self.Logger, bStrictTarget = False)

class Test_JSON_Parser(Test_TSV_Parser):
    """
    Test cases for the class JSON_Parser of the module GenericParsers.
    
    Test IDs - TEST-T-600, TEST-T-601, TEST-T-602, TEST-T-603, TEST-T-604,
    TEST-T-605, TEST-T-606, TEST-T-607, TEST-T-608, TEST-T-609, TEST-T-60A,
    TEST-T-60B and TEST-T-610.
    """
    
    TestID = "ut004_3"
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_JSON_Parser, cls).setUpClass()
        cls.TestClass = TestModule.JSON_Parser
        cls.DummyFile = "dummy.json"
        cls.DummyFileZero = "dummy0.json"
        cls.Template = {
            "DataMapping" : {
                "report" : {
                    "id" : "dummy.id",
                    "type" : "dummy.type"
                },
                "result" : ["dummy.tests", {"result" : "PASS"}, "value"]
            }
        }
        cls.BadFile = "bad_4.json"
    
    def test_CopiesProperlyWithTargetAndTemplate(self):
        """
        The methods parseFile() and parseManyFiles() create the expected number
        of the target objects packed into the expected container types and fill
        them properly when both the target class (type) and the template are
        provided explicitely, and the mapping matches the structure of the both
        source and target objects. Also checks that the 'special' cases of the
        improper formed JSON as '{} {}' or '{}, {}' instead of '[{}, {}]' are
        treated as lists of dictionaries as well.
        
        Test ID - TEST-T-608. Covers requirements REQ-FUN-600.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile,
            clsTarget = self.TargetClass, dictTemplate = self.Template,
                objLogger = self.Logger)
        self.assertTrue(isinstance(lstResult, collections.Sequence))
        self.assertFalse(isinstance(lstResult, basestring))
        self.assertEqual(len(lstResult), 1)
        objTest = lstResult[0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertEqual(objTest.report["id"], 1)
        self.assertEqual(objTest.report["type"], "dummy")
        self.assertEqual(objTest.result, 1)
        strlstFiles = ['dummy1.json', 'dummy2.json', 'dummy3.json']
        odResult = self.TestClass.parseManyFiles(self.InFolder, strlstFiles,
            clsTarget = self.TargetClass, dictTemplate = self.Template,
                objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 3)
        for strFile in strlstFiles:
            objlstTest = odResult[strFile]
            for objTest in objlstTest:
                self.assertIsInstance(objTest, self.TargetClass)
                self.assertEqual(objTest.report["id"], 1)
                self.assertEqual(objTest.report["type"], "dummy")
                self.assertEqual(objTest.result, 1)
    
    def test_CopiesProperlyWithTemplateOnly(self):
        """
        The methods parseFile() and parseManyFiles() create the expected number
        of the target objects packed into the expected container types and fill
        them properly when only the template is provided explicitely, and the
        mapping matches the structure of the both source and target objects. The
        target class (type) is not provided, but taken from the template. All
        flags are left at their default values.Also checks that the 'special'
        cases of the improper formed JSON as '{} {}' or '{}, {}' instead of
        '[{}, {}]' are treated as lists of dictionaries as well.
        
        Test ID - TEST-T-609. Covers requirements REQ-FUN-600 and REQ-FUN-602.
        """
        dictTemplate = copy.deepcopy(self.Template)
        dictTemplate["TargetClassModule"] = 'fsio_lib.Tests.ut004_helper_class'
        dictTemplate["TargetClass"] = 'HelperClass'
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile,
            dictTemplate = dictTemplate, objLogger = self.Logger)
        self.assertTrue(isinstance(lstResult, collections.Sequence))
        self.assertFalse(isinstance(lstResult, basestring))
        self.assertEqual(len(lstResult), 1)
        objTest = lstResult[0]
        self.assertIsInstance(objTest, HelperClass1)
        self.assertEqual(objTest.report["id"], 1)
        self.assertEqual(objTest.report["type"], "dummy")
        self.assertEqual(objTest.result, 1)
        strlstFiles = ['dummy1.json', 'dummy2.json', 'dummy3.json']
        odResult = self.TestClass.parseManyFiles(self.InFolder, strlstFiles,
            dictTemplate = dictTemplate, objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 3)
        for strFile in strlstFiles:
            objlstTest = odResult[strFile]
            for objTest in objlstTest:
                self.assertIsInstance(objTest, HelperClass1)
                self.assertEqual(objTest.report["id"], 1)
                self.assertEqual(objTest.report["type"], "dummy")
                self.assertEqual(objTest.result, 1)
    
    def test_RaisesExceptionBadFile(self):
        """
        The methods parseFile() and parseManyFiles() raise ValueError if the
        source data file is not a proper format JSON, excluding the cases of
        '{} {}' or '{}, {}' instead of '[{}, {}]'.
        
        Test ID - TEST-T-610. Covers requirements REQ-AWM-610.
        """
        strFile = os.path.join(self.InFolder, self.BadFile)
        with self.assertRaises(ValueError):
            self.TestClass.parseFile(strFile, clsTarget = self.TargetClass,
                dictTemplate = self.Template, objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestClass.parseManyFiles(self.InFolder, [self.BadFile],
                clsTarget = self.TargetClass, dictTemplate = self.Template,
                    objLogger = self.Logger)
    
    def test_DeterminesTargetAndTemplateByFile(self):
        """
        The methods parseFile() and parseManyFiles() must return the target
        objects of the expected types (class instances) properly filled with the
        data from the source file(s) and packed into the proper container
        objects - when neither the template nor the target class are explicitely
        provided, but the required template can be selected on the basis of the
        source file content.
        
        Test ID - TEST-T-60B. Covers requirements REQ-FUN-603.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile, objLogger = self.Logger)
        self.assertIsInstance(lstResult, collections.Sequence)
        self.assertNotIsInstance(lstResult, basestring)
        self.assertEqual(len(lstResult), 1)
        objTest = lstResult[0]
        self.assertIsInstance(objTest, HelperClass1)
        self.assertEqual(objTest.report["id"], 1)
        self.assertEqual(objTest.report["type"], "dummy")
        self.assertEqual(objTest.result, 1)
        odResult =self.TestClass.parseManyFiles(self.InFolder, [self.DummyFile],
                objLogger = self.Logger)
        self.assertIsInstance(odResult, collections.OrderedDict)
        lstResult = odResult[self.DummyFile]
        self.assertIsInstance(lstResult, collections.Sequence)
        self.assertNotIsInstance(lstResult, basestring)
        self.assertEqual(len(lstResult), 1)
        objTest = lstResult[0]
        self.assertIsInstance(objTest, HelperClass1)
        self.assertEqual(objTest.report["id"], 1)
        self.assertEqual(objTest.report["type"], "dummy")
        self.assertEqual(objTest.result, 1)
        

class Test_XML_Parser(Test_JSON_Parser):
    """
    Test cases for the class XML_Parser of the module GenericParsers.
    
    Test IDs - TEST-T-600, TEST-T-601, TEST-T-602, TEST-T-603, TEST-T-604,
    TEST-T-605, TEST-T-606, TEST-T-607, TEST-T-608, TEST-T-609, TEST-T-60A,
    TEST-T-60B and TEST-T-620.
    """
    
    TestID = "ut004_4"
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_XML_Parser, cls).setUpClass()
        cls.TestClass = TestModule.XML_Parser
        cls.DummyFile = "dummy.xml"
        cls.DummyFileZero = "dummy0.xml"
        cls.Template = {
            "DataMapping" : {
                "report" : {
                    "id" : "node.id",
                    "type" : "node.type"
                },
                "result" : ["node", {"result" : "PASS"}, "value"]
            }
        }
    
    def test_CopiesProperlyWithTargetAndTemplate(self):
        """
        The methods parseFile() and parseManyFiles() create the expected number
        of the target objects packed into the expected container types and fill
        them properly when both the target class (type) and the template are
        provided explicitely, and the mapping matches the structure of the both
        source and target objects.
        
        Test ID - TEST-T-608. Covers requirements REQ-FUN-600.
        """
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile,
            clsTarget = self.TargetClass, dictTemplate = self.Template,
                objLogger = self.Logger)
        self.assertTrue(isinstance(lstResult, collections.Sequence))
        self.assertFalse(isinstance(lstResult, basestring))
        self.assertEqual(len(lstResult), 1)
        objTest = lstResult[0]
        self.assertIsInstance(objTest, self.TargetClass)
        self.assertEqual(objTest.report["id"], 1)
        self.assertEqual(objTest.report["type"], "dummy")
        self.assertEqual(objTest.result, 1)
        strlstFiles = [self.DummyFile, 'dummy1.xml']
        odResult = self.TestClass.parseManyFiles(self.InFolder, strlstFiles,
            clsTarget = self.TargetClass, dictTemplate = self.Template,
                objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 2)
        for strFile in strlstFiles:
            objlstTest = odResult[strFile]
            for objTest in objlstTest:
                self.assertIsInstance(objTest, self.TargetClass)
                self.assertEqual(objTest.report["id"], 1)
                self.assertEqual(objTest.report["type"], "dummy")
                self.assertEqual(objTest.result, 1)
    
    def test_CopiesProperlyWithTemplateOnly(self):
        """
        The methods parseFile() and parseManyFiles() create the expected number
        of the target objects packed into the expected container types and fill
        them properly when only the template is provided explicitely, and the
        mapping matches the structure of the both source and target objects. The
        target class (type) is not provided, but taken from the template. All
        flags are left at their default values.
        
        Test ID - TEST-T-609. Covers requirements REQ-FUN-600 and REQ-FUN-602.
        """
        dictTemplate = copy.deepcopy(self.Template)
        dictTemplate["TargetClassModule"] = 'fsio_lib.Tests.ut004_helper_class'
        dictTemplate["TargetClass"] = 'HelperClass'
        strFile = os.path.join(self.InFolder, self.DummyFile)
        lstResult = self.TestClass.parseFile(strFile,
            dictTemplate = dictTemplate, objLogger = self.Logger)
        self.assertTrue(isinstance(lstResult, collections.Sequence))
        self.assertFalse(isinstance(lstResult, basestring))
        self.assertEqual(len(lstResult), 1)
        objTest = lstResult[0]
        self.assertIsInstance(objTest, HelperClass1)
        self.assertEqual(objTest.report["id"], 1)
        self.assertEqual(objTest.report["type"], "dummy")
        self.assertEqual(objTest.result, 1)
        strlstFiles = [self.DummyFile, 'dummy1.xml']
        odResult = self.TestClass.parseManyFiles(self.InFolder, strlstFiles,
            dictTemplate = dictTemplate, objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 2)
        for strFile in strlstFiles:
            objlstTest = odResult[strFile]
            for objTest in objlstTest:
                self.assertIsInstance(objTest, HelperClass1)
                self.assertEqual(objTest.report["id"], 1)
                self.assertEqual(objTest.report["type"], "dummy")
                self.assertEqual(objTest.result, 1)
    
    def test_RaisesExceptionBadFile(self):
        """
        The methods parseFile() and parseManyFiles() raise exception
        xml.etree.ElementTree.ParseError if the source data file is not a proper
        format XML.
        
        Test ID - TEST-T-620. Covers requirements REQ-AWM-620.
        """
        strFile = os.path.join(self.InFolder, self.BadFile)
        with self.assertRaises(ParseError):
            self.TestClass.parseFile(strFile, clsTarget = self.TargetClass,
                dictTemplate = self.Template, objLogger = self.Logger)
        with self.assertRaises(ParseError):
            self.TestClass.parseManyFiles(self.InFolder, [self.BadFile],
                clsTarget = self.TargetClass, dictTemplate = self.Template,
                    objLogger = self.Logger)

class Test_parseFile(unittest.TestCase):
    """
    Test cases for the function parseFile() of the module GenericParsers.
    
    Test ID - TEST-T-601, TEST-T-602, TEST-T-60C.
    """
    
    TestID = "ut004_5"
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.parseFile)
        cls.Logger = DualLogger(cls.__name__, bLogToFile = True,
                            strFileName = os.path.join(LIB_ROOT, 'Tests',
                                        'Output', '{}.log'.format(cls.TestID)))
        cls.Logger.setFileLoggingLevel(logging.INFO)
        cls.Logger.disableConsoleLogging()
        cls.InFolder = os.path.join(LIB_ROOT, 'Tests', 'Input')
        cls.Files = ['dummy.json', 'dummy.xml']
        cls.NotStringNames = [1, 1.0, {"a" : "b"}, True, int, float, str, dict]
    
    def test_RaisesTypeErrorFiles(self):
        """
        Function parseFile() raises TypeError if the file name is not a string.
        
        Test ID - TEST-T-601. Covers requirements REQ-AWM-601.
        """
        for Name in self.NotStringNames:
            with self.assertRaises(TypeError):
                self.TestFunction(Name, objLogger = self.Logger)
    
    def test_RaisesValueErrorNotFile(self):
        """
        Function parseFile() raises ValueError if the file path does not point
        to an existing file.
        
        Test ID - TEST-T-602. Covers requirements REQ-AWM-602.
        """
        strFile = os.path.join(self.InFolder, 'foo_bar.baz')
        with self.assertRaises(ValueError):
            self.TestFunction(strFile, objLogger = self.Logger)
    
    def test_ParsesAutomatically(self):
        """
        Function parseFile() must automatically detect the required parsing
        template and the target class by the content of the file, when possible,
        and return the proper container object with the proper type elements,
        filled with the data from the source file as expected.
        
        Test ID - TEST-T-60C. Covers the requirements REQ-FUN-601, REQ-FUN-602
        and REQ-FUN-603.
        """
        for strFileName in self.Files:
            strFile = os.path.join(self.InFolder, strFileName)
            lstResult = self.TestFunction(strFile, objLogger = self.Logger)
            self.assertTrue(isinstance(lstResult, collections.Sequence))
            self.assertFalse(isinstance(lstResult, basestring))
            self.assertEqual(len(lstResult), 1)
            objTest = lstResult[0]
            self.assertIsInstance(objTest, HelperClass1)
            self.assertEqual(objTest.report["id"], 1)
            self.assertEqual(objTest.report["type"], "dummy")
            self.assertEqual(objTest.result, 1)

class Test_parseManyFiles(unittest.TestCase):
    """
    Test cases for the function parseManyFiles() of the module GenericParsers.
    
    Test ID - TEST-T-601, TEST-T-602, TEST-T-60C.
    """
    
    TestID = "ut004_6"
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.parseManyFiles)
        cls.Logger = DualLogger(cls.__name__, bLogToFile = True,
                            strFileName = os.path.join(LIB_ROOT, 'Tests',
                                        'Output', '{}.log'.format(cls.TestID)))
        cls.Logger.setFileLoggingLevel(logging.INFO)
        cls.Logger.disableConsoleLogging()
        cls.InFolder = os.path.join(LIB_ROOT, 'Tests', 'Input')
        cls.Files = ['dummy.json', 'dummy.xml']
        cls.NotStringNames = [1, 1.0, {"a" : "b"}, True, int, float, str, dict]
    
    def test_RaisesTypeErrorFiles(self):
        """
        Function parseManyFiles() raises TypeError if the folder name is not a
        string or, at least, one base file name is not a string.
        
        Test ID - TEST-T-601. Covers requirements REQ-AWM-601.
        """
        for Name in self.NotStringNames:
            with self.assertRaises(TypeError):
                self.TestFunction(Name, self.Files, objLogger = self.Logger)
            with self.assertRaises(TypeError):
                self.TestFunction(self.InFolder, [Name], objLogger =self.Logger)
    
    def test_RaisesValueErrorNotFile(self):
        """
        Function parseManyFiles() raises ValueError if the file path does not
        point to an existing file, for any of the base names, which includes the
        path to their folder not pointing to an existing folder.
        
        Test ID - TEST-T-602. Covers requirements REQ-AWM-602.
        """
        strFile = os.path.join(self.InFolder, 'foo_bar.baz')
        with self.assertRaises(ValueError):
            self.TestFunction(strFile, self.Files, objLogger = self.Logger)
        with self.assertRaises(ValueError):
            self.TestFunction(self.InFolder, ['foo_bar.baz'],
                                                    objLogger = self.Logger)
    
    def test_ParsesAutomatically(self):
        """
        Function parseManyFiles() must automatically detect the required parsing
        template and the target class by the content of the file - individually
        per file, when possible, and return the proper container object with
        the proper type elements, filled with the data from the source file as
        expected.
        
        Test ID - TEST-T-60C. Covers the requirements REQ-FUN-601, REQ-FUN-602
        and REQ-FUN-603.
        """
        odResult = self.TestFunction(self.InFolder, self.Files,
                                                        objLogger = self.Logger)
        self.assertTrue(isinstance(odResult, collections.OrderedDict))
        self.assertEqual(len(odResult), 2)
        for strFile in self.Files:
            lstResult = odResult[strFile]
            self.assertTrue(isinstance(lstResult, collections.Sequence))
            self.assertFalse(isinstance(lstResult, basestring))
            self.assertEqual(len(lstResult), 1)
            objTest = lstResult[0]
            self.assertIsInstance(objTest, HelperClass1)
            self.assertEqual(objTest.report["id"], 1)
            self.assertEqual(objTest.report["type"], "dummy")
            self.assertEqual(objTest.result, 1)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GenericParser)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_TSV_Parser)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_JSON_Parser)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_XML_Parser)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_parseFile)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_parseManyFiles)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
    TestSuite6])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.GenericParsers module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)