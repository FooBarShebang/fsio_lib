#!/usr/bin/python
"""
Module fsio_lib.Tests.ut002_structure_mapping

Implements unit testing of the module StructureMapping. Test ID - UT002
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
import json
import collections
import copy
import xml.etree.ElementTree as ElementTree

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.StructureMapping as TestModule
from fsio_lib.LoggingFSIO import DualLogger

#globals - helper test values

TEST_FILES_FOLDER = os.path.join(LIB_ROOT, 'Tests', 'Input')

BAD_FORMAT_JSON = ['bad_1.json', #two dictionaries side by side, not enclosed
                    'bad_2.json', #two dictionaries in a list, missing brackets
                    'bad_3.json', #comma after the last element (outer)
                    'bad_4.json', #comma after the last element (inner)
                    'bad_5.json', #missing comma between elements
                    'bad_6.json', #integer key (not in parenthesis)
                    'bad_7.json', #single quotes instead of double quotes
                    'bad_8.json', #includes bad format (entirely)
                    'bad_9.json', #includes bad format (element required)
                    'bad_10.json', #includes not existing file (entirely)
                    'bad_11.json',#includes not existing file (element required)
                    ]

BAD_FORMAT_DSL = ['circular_1.json', #circular path substitution definition
                    'circular_2.json', #circular path substitution, imported
                    'undef_path_1.json', #missing path substitution definition
                    'undef_path_2.json', #missing path substitution def, import
                    'missing_path_1.json', #nested missing substitution, in list
                    'missing_path_2.json', #nested missing substitution, simple
                    'missing_path_3.json', #nested missing substitution, simple
                    'missing_path_4.json', #missing substitution, simple, top,
                                            #+ also - improper rule!
                    'missing_path_5.json', #in import missing path
                    'missing_value_1.json', #nested missing substitution, in lst
                    'missing_value_2.json', #nested missing substitution, simple
                    'missing_value_3.json', #nested missing substitution, simple
                    'missing_value_4.json', #missing substitution, simple, top
                    'missing_value_5.json', #in import missing value subst. def.
                    'empty_path_1.json', #empty path subst. definition
                    'empty_path_2.json', #empty path subst. definition, included
                    'empty_path_3.json', #empty path direct
                    'empty_path_4.json', #empty path, included in direct
                    'wrong_path_1.json', #negative index in path subst.
                    'wrong_path_2.json', #negative index in path subst., incl.
                    'wrong_path_3.json', #negative index in direct path
                    'wrong_path_4.json', #negative index in direct path, include
                    'wrong_value_name_1.json', #wrong name for val subst
                    'wrong_value_name_2.json', #wrong name for val subst, incl.
                    'wrong_path_name_1.json', #wrong name for path subst
                    'wrong_path_name_2.json', #wrong name for path subst, incl.
                    'spelling_1.json', #"PATH" instead of "PATHS"
                    'spelling_2.json', #"INCLUDE" instead of "INCLUDES"
                    'spelling_3.json', #mismatching incremental addition
                    'spelling_4.json', #mismatching incremental removal
                    'spelling_5.json', #spelling_1.json included
                    'spelling_6.json', #spelling_2.json included
                    'spelling_7.json', #spelling_3.json included
                    'spelling_8.json', #spelling_4.json included
                    'spelling_9.json', #dot name of a key (not rule name!)
                    'spelling_10.json', #dot name of a key (not rule name!)
                    'spelling_11.json', #<0 int in str = key (not rule name!)
                    'spelling_12.json', #list in str = key (not rule name!)
                    'spelling_13.json', #dict in str = key (not rule name!)
                    'spelling_14.json', #includes spelling_13.json
                    'spelling_15.json', #not nested dict incr. addition def.
                    'spelling_16.json', #dot notation of a key in inc. add. def.
                    'spelling_17.json', #negative index as key in inc. add. def.
                    'spelling_18.json', #negative index as path in inc. add. def
                    'spelling_19.json', #string as value of inc. del. def
                    'spelling_20.json', #neg. int. in path in inc. del. def
                    'spelling_21.json', #same, deeper nesting
]

GOOD_FORMAT_JSON = [('good_1.json', 'good_1.json'), #basic with all elements
                    ('good_2.json', 'good_2_check.json'), #includes 'good_1'
                    ('good_3.json', 'good_3_check.json'), #includes 'good_1' and
                                                    #+ 'good_2'['d'] + paths
                    ('good_4.json', 'good_4_check.json'), #import good_3 +
                                            #+ incremental addition and removal
                    ]
# proper format + in included - counterpart to bad formats

# checks on existance of the output folder

strTemp = os.path.join(LIB_ROOT, 'Tests', 'Output')

if not os.path.isdir(strTemp):
    os.mkdir(strTemp)

#helper functions

def ModifyKeys(dictTest):
    lstKeys = dictTest.keys()
    for gKey in lstKeys:
        gValue = dictTest[gKey]
        if isinstance(gValue, collections.Mapping):
            gValue = ModifyKeys(gValue)
        try:
            iKey = int(gKey)
            dictTest[iKey] = gValue
            del dictTest[gKey]
        except:
            dictTest[gKey] = gValue
    return dictTest

#classes

#+ helper classes

class InnerClass(object):
    
    def __init__(self, InitValue = 1):
        self.c = InitValue
        self.value = InitValue

class OuterClass(object):
    
    def __init__(self, InitValue = 1):
        self.a = [{"test" : InitValue}, 
                                [{"b" : InitValue}, InnerClass(InitValue)]]

#+ test cases

class Test_LoadDefinition(unittest.TestCase):
    """
    Test cases for the function LoadDefinition of the module StructureMapping.
    
    Implements test IDs - TEST-T-160, TEST-T-161.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.LoadDefinition)
        cls.Logger = DualLogger('Test_LoadDefinition', bLogToFile = True,
                            strFileName = os.path.join(LIB_ROOT, 'Tests',
                                                    'Output', 'ut002_1.log'))
        cls.Logger.setFileLoggingLevel(logging.INFO)
        cls.Logger.disableConsoleLogging()
    
    def test_RaisesUsualError(self):
        """
        The function raises IOError or OSError if the file cannot be found or
        opened, and ValueError if it is not a proper JSON file - i.e. the
        original exceptions are re-raised if caught.
        
        Test ID - TEST-T-160. Covers requirements REQ-AWM-120, REQ-AWM-121.
        """
        #IOError / OSError
        strFileName = os.path.join(TEST_FILES_FOLDER, 'foo_bar.baz')
        with self.assertRaises((IOError, OSError)):
            if not (self.Logger is None):
                self.Logger.info(strFileName)
            self.TestFunction(strFileName, self.Logger)
        #ValueError - bad JSON format
        for strName in BAD_FORMAT_JSON:
            strFileName = os.path.join(TEST_FILES_FOLDER, strName)
            with self.assertRaises((IOError, OSError, ValueError)):
                if not (self.Logger is None):
                    self.Logger.info(strFileName)
                self.TestFunction(strFileName, self.Logger)
    
    def test_RaisesValueError(self):
        """
        The function raises ValueError if the file being processed or at least
        one of the files it includes does not conform with the DSL
        specifications, specifically:
        
        * Circular definition of a path substitution
        * Missing dependence in a definition of a path substitution
        * Missing definition of a path or value substitution in a mapping rule
        * Incremental addition or deletion rule for non-existing mapping
            definition sub-dictionary
        * Improper path definition in any path / value substitution or mapping
            rule
        
        Test ID - TEST-T-160 - part 2. Covers requirements REQ-AWM-121.
        """
        for strName in BAD_FORMAT_DSL:
            strFileName = os.path.join(TEST_FILES_FOLDER, strName)
            with self.assertRaises(ValueError):
                if not (self.Logger is None):
                    self.Logger.info(strFileName)
                self.TestFunction(strFileName, self.Logger)
    
    def test_LoadsProper(self):
        """
        The function must parse the proper formed JSON file with all entries
        conforming the mapping DSL properly.
        
        Test ID - TEST-T-161. Covers requirements REQ-FUN-100, REQ-FUN-102,
        REQ-FUN-103.
        """
        for strCase, strResult in GOOD_FORMAT_JSON:
            strFileName = os.path.join(TEST_FILES_FOLDER, strCase)
            if not (self.Logger is None):
                self.Logger.info(strFileName)
            dictTest = self.TestFunction(strFileName, self.Logger)
            strFileName = os.path.join(TEST_FILES_FOLDER, strResult)
            with open(strFileName, 'rt') as fFile:
                dictCheck = json.load(fFile)
            if strCase != 'good_1.json':
                ModifyKeys(dictCheck)
            self.assertEqual(dictTest, dictCheck)

class Test_MapValues(unittest.TestCase):
    """
    Test cases for the function MapValues of the module StructureMapping.
    
    Implements test IDs - TEST-T-170, TEST-T-171, TEST-T-172
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.MapValues)
        cls.Logger = DualLogger('Test_MapValues', bLogToFile = True,
                            strFileName = os.path.join(LIB_ROOT, 'Tests',
                                                    'Output', 'ut002_2.log'))
        cls.Logger.setFileLoggingLevel(logging.INFO)
        cls.Logger.disableConsoleLogging()
    
    def test_RaiseTypeError(self):
        """
        The function raises TypeError if any type but mapping (e.g. dict) is
        passed as the third argument - the mapping rules dictionary. Regardless
        of the bStrictSource and bStrictTarget flags.
        """
        for gTestObject in [list, tuple, int, float, str, [], tuple(), 1, 2.0,
                                                                        "test"]:
            for TargetFlag in [True, False]:
                for SourceFlag in [True, False]:
                    if not (self.Logger is None):
                        strMessage = "{} {} {}".format(gTestObject, TargetFlag,
                                                                    SourceFlag)
                        self.Logger.info(strMessage)
                    with self.assertRaises(TypeError):
                        self.TestFunction(dict(), dict(), gTestObject,
                                        self.Logger, bStrictTarget = TargetFlag,
                                                    bStrictSource = SourceFlag)
    
    def test_RaiseTypeValueErrorMappingObject(self):
        """
        The function raises TypeError or ValueError if the mapping dictionary is
        not of the proper format (DE001 DSL specifications). Regardless of the
        bStrictSource and bStrictTarget flags.
        
        Test ID - TEST-T-170. Covers requirements REQ-AWM-110, REQ-AWM-111.
        """
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
            for TargetFlag in [True, False]:
                for SourceFlag in [True, False]:
                    if not (self.Logger is None):
                        strMessage = "{} {} {}".format(gTestObject, TargetFlag,
                                                                    SourceFlag)
                        self.Logger.info(strMessage)
                    with self.assertRaises((TypeError, ValueError)):
                        
                        self.TestFunction(dict(), dict(), gTestObject,
                                        self.Logger, bStrictTarget = TargetFlag,
                                                    bStrictSource = SourceFlag)
    
    def test_RaisesAttributeErrorSource(self):
        """
        The function must raise AttributeError if the required element is not
        found in the source object and the bStrictSource flag is True.
        
        Test ID - TEST-T-171. Covers requirement REQ-AWM-122.
        """
        Target = {"a" : { "b" : 0, "c" : 0}}
        MapDict = { "a" : { "b" : "a.b", "c" : "a.c"}}
        lstSources = [[1, 2], {"a" : { "b" : 1}, "c" : 2},
                                                    {"a" : { "c" : 2}, "b" : 1}]
        for Source in lstSources:
            if not (self.Logger is None):
                strMessage = "{}".format(Source)
                self.Logger.info(strMessage)
            with self.assertRaises(AttributeError):
                self.TestFunction(Target, Source, MapDict, self.Logger,
                                    bStrictTarget = True, bStrictSource = True)
    
    def test_SkipsAttributeErrorSource(self):
        """
        The function must not raise AttributeError if the required element is
        not found in the source object and the bStrictSource flag is False. The
        data is, however, not copied for this specific mapping rule.
        
        Test ID - TEST-T-171 - part 2. Covers requirements REQ-AWM-122,
        REQ-FUN-100.
        """
        Target = {"a" : { "b" : 0, "c" : 0}}
        MapDict = { "a" : { "b" : "a.b", "c" : "a.c"}}
        tuplstSources = [([1, 2], (0,0)),
                        ({"a" : { "b" : 1}, "c" : 2}, (1, 0)),
                        ({"a" : { "c" : 2}, "b" : 1}, (0, 2)),
                        ({"a" : {"b" : 1, "c" : 2}}, (1, 2))]
        for Source, tupResults in tuplstSources:
            if not (self.Logger is None):
                strMessage = "{}".format(Source)
                self.Logger.info(strMessage)
            Temp = copy.deepcopy(Target)
            self.TestFunction(Temp, Source, MapDict, self.Logger,
                                    bStrictTarget = True, bStrictSource = False)
            self.assertEqual(Temp["a"]["b"], tupResults[0])
            self.assertEqual(Temp["a"]["c"], tupResults[1])
    
    def test_RaisesAttributeErrorTargetForced(self):
        """
        The function must raise AttributeError if the required element is not
        found in the target object and the bStrictTarget flag is False, whilst
        bForceTarget is True and there is an immutable or incopatible object in
        the path.
        
        Test ID - TEST-T-171 - part 3. Covers requirement REQ-AWM-122.
        """
        Source = {"a" : { "b" : 1, "c" : 2}}
        MapDict = { "a" : { "b" : "a.b", "c" : "a.c"}}
        lstTargets = [(0, 0), {"a" : ({ "b" : 0}, {"c" : 0})}, {"a" : 1},
                {"a" : "b"}, ElementTree.Element('root', attrib = {"a" : "1"})]
        for Target in lstTargets:
            if not (self.Logger is None):
                strMessage = "{}".format(Target)
                self.Logger.info(strMessage)
            with self.assertRaises(AttributeError):
                self.TestFunction(Target, Source, MapDict, self.Logger,
                                    bStrictTarget = False, bForceTarget = True)
    
    def test_SkipsAttributeErrorTargetForced(self):
        """
        The function must raise AttributeError if the required element is not
        found in the target object and the bStrictTarget flag is False, whilst
        bForceTarget is True and there are no immutable or incopatible objects
        in the path.
        
        Test ID - TEST-T-171 - part 4. Covers requirements REQ-AWM-122,
        REQ-FUN-100.
        """
        Source = {"a" : { "b" : 1, "c" : 2}}
        MapDict = { "a" : { "b" : "a.b", "c" : "a.c"}}
        lstTargets = [([0, 0],
                        [0, 0, {"a" : { "b" : 1}}, {"a" : { "c" : 2}}]),
                        ({"a" : { "b" : 0}, "c" : 0},
                                        {"a" : { "b" : 1, "c" : 2}, "c" : 0}),
                        ({"a" : { "c" : 0}, "b" : 0},
                                        {"a" : { "c" : 2, "b" : 1}, "b" : 0}),
                        ({ "b" : 0, "c" : 0},
                                { "b" : 0, "c" : 0, "a" : { "b" : 1, "c" : 2}})]
        for Target, Result in lstTargets:
            strMessage = "{} ->".format(Target)
            self.TestFunction(Target, Source, MapDict, self.Logger,
                                    bStrictTarget = False, bForceTarget = True)
            if not (self.Logger is None):
                strMessage = "{} {} ?= {}".format(strMessage, Target, Result)
                self.Logger.info(strMessage)
            if isinstance(Target, collections.Sequence):
                self.assertItemsEqual(Target, Result)
            else:
                self.assertEqual(Target, Result)
        #special cases - XML element
        objTest = ElementTree.Element("root") #no sub-elements!
        if not (self.Logger is None):
            strMessage ="Adding sub-element with attributes to the root XML"
            self.Logger.info(strMessage)
        self.TestFunction(objTest, Source, MapDict, self.Logger,
                                    bStrictTarget = False, bForceTarget = True)
        objChild = objTest.find("a")
        self.assertEqual(objChild.attrib["b"], "1")
        self.assertEqual(objChild.attrib["c"], "2")
        objTest = ElementTree.Element("root")
        ElementTree.SubElement(objTest, "a") #no attributes!
        if not (self.Logger is None):
            strMessage ="Adding attributes to the XML sub-element"
            self.Logger.info(strMessage)
        self.TestFunction(objTest, Source, MapDict, self.Logger,
                                    bStrictTarget = False, bForceTarget = True)
        objChild = objTest.find("a")
        self.assertEqual(objChild.attrib["b"], "1")
        self.assertEqual(objChild.attrib["c"], "2")
    
    def test_SetsProperly(self):
        """
        The function performs the mapping properly in the default mode (both
        source and target are strict) in the case of the mapping rules properly
        reflecting the structure of both objects. The test cases must include
        complex / mixed types of the source and target objects, and the source
        path notation using strings, integers and 'choice' dictionaries:
        
        * Class including nested sequence, dictionary and another struct-like
            class - > to the same type object
        * Class including nested sequence, dictionary and another struct-like
            class - > to nested XML object
        * Class including nested sequence, dictionary and another struct-like
            class - > to flat dictionary
        * flat sequence -> class including nested sequence, dictionary and
            another struct-like class
        * nested XML object -> class including nested sequence, dictionary and
            another struct-like class
        
        Test ID - TEST-T-172. Covers requirements REQ-FUN-100, REQ-FUN-103 and
        REQ-FUN-104.
        """
        TestValue = 42
        # OuterClass -> OuterClass
        MapDict = {"a" : {
                    0 : {"test" : ["a", 0, "test"]},
                    1 : {
                        0 : {"b" : ["a", 1, 0, "b"]},
                        1 : {
                            "c" : ["a", 1, {"c" : TestValue}, "c"],
                            "value" : ["a", 1, 1, "value"],
                        }
                    }}}
        Target = OuterClass(0)
        Source = OuterClass(TestValue)
        if not (self.Logger is None):
            strMessage ="OuterClass to OuterClass"
            self.Logger.info(strMessage)
        self.TestFunction(Target, Source, MapDict, self.Logger)
        self.assertEqual(Target.a[0]["test"], TestValue)
        self.assertEqual(Target.a[1][0]["b"], TestValue)
        self.assertEqual(Target.a[1][1].c, TestValue)
        self.assertEqual(Target.a[1][1].value, TestValue)
        # flat sequence -> OuterClass
        MapDict = {"a" : {
                    0 : {"test" : 0},
                    1 : {
                        0 : {"b" : 1},
                        1 : {
                            "c" : 2,
                            "value" : 3,
                        }
                    }}}
        Target = OuterClass(0)
        Source = [TestValue, TestValue + 1, TestValue + 2, TestValue + 3]
        if not (self.Logger is None):
            strMessage ="flat sequence to OuterClass"
            self.Logger.info(strMessage)
        self.TestFunction(Target, Source, MapDict, self.Logger)
        self.assertEqual(Target.a[0]["test"], TestValue)
        self.assertEqual(Target.a[1][0]["b"], TestValue + 1)
        self.assertEqual(Target.a[1][1].c, TestValue + 2)
        self.assertEqual(Target.a[1][1].value, TestValue + 3)
        # OuterClass -> flat sequence
        MapDict = {0 : ["a", 0, "test"],
                    1 : ["a", 1, 0, "b"],
                    2 : ["a", 1, {"c" : TestValue}, "c"],
                    3 : ["a", 1, 1, "value"]
                    }
        Target = [0, 0, 0, 0]
        Source = OuterClass(TestValue)
        if not (self.Logger is None):
            strMessage ="OuterClass to flat sequence"
            self.Logger.info(strMessage)
        self.TestFunction(Target, Source, MapDict, self.Logger)
        self.assertEqual(Target[0], TestValue)
        self.assertEqual(Target[1], TestValue)
        self.assertEqual(Target[2], TestValue)
        self.assertEqual(Target[3], TestValue)
        # OuterClass -> XML ElementTree.Element
        MapDict = { "a" : {
                    0 :  {"test" : ["a", 0, "test"]},
                    1 : {
                        0 : {"b" : ["a", 1, 0, "b"]},
                        1 : { "c" : ["a", 1, {"c" : TestValue}, "c"],
                                "value" : ["a", 1, 1, "value"]}
                    }
                }
        }
                    
        Target = ElementTree.Element("root")
        objNodeA = ElementTree.SubElement(Target, "a")
        objNodeA0 = ElementTree.SubElement(objNodeA, "node",
                                                    attrib = {"test" : "None"})
        objNodeA1 = ElementTree.SubElement(objNodeA, "node")
        objNodeA10 = ElementTree.SubElement(objNodeA1, "node",
                                                    attrib = {"b" : "None"})
        objNodeA11 = ElementTree.SubElement(objNodeA1, "node",
                                    attrib = {"c" : "None", "value" : "None"})
        Source = OuterClass(TestValue)
        if not (self.Logger is None):
            strMessage ="OuterClass to XML ElementTree.Element"
            self.Logger.info(strMessage)
        self.TestFunction(Target, Source, MapDict, self.Logger)
        self.assertEqual(Target[0][0].attrib["test"], str(TestValue))
        self.assertEqual(objNodeA0.attrib["test"], str(TestValue)) #same!
        self.assertEqual(Target[0][1][0].attrib["b"], str(TestValue))
        self.assertEqual(objNodeA10.attrib["b"], str(TestValue)) #same!
        self.assertEqual(Target[0][1][1].attrib["c"], str(TestValue))
        self.assertEqual(objNodeA11.attrib["c"], str(TestValue)) #same!
        self.assertEqual(Target[0][1][1].attrib["value"], str(TestValue))
        self.assertEqual(objNodeA11.attrib["value"], str(TestValue)) #same!
        # XML ElementTree.Element -> OuterClass
        MapDict = { "a" : {
                    0 :  {"test" : ["a", 0, "test"]},
                    1 : {
                        0 : {"b" : ["a", 1, 0, "b"]},
                        1 : { "c" : ["a", 1, {"c" : TestValue}, "c"],
                                "value" : ["a", 1, 1, "value"]}
                    }
                }
        }
        strVal = str(TestValue)
        Source = ElementTree.Element("root")
        objNodeA = ElementTree.SubElement(Source, "a")
        objNodeA0 = ElementTree.SubElement(objNodeA, "node",
                                                    attrib = {"test" : strVal})
        objNodeA1 = ElementTree.SubElement(objNodeA, "node")
        objNodeA10 = ElementTree.SubElement(objNodeA1, "node",
                                                    attrib = {"b" : strVal})
        objNodeA11 = ElementTree.SubElement(objNodeA1, "node",
                                    attrib = {"c" : strVal, "value" : strVal})
        Target = OuterClass(0)
        if not (self.Logger is None):
            strMessage ="XML ElementTree.Element to OuterClass"
            self.Logger.info(strMessage)
        self.TestFunction(Target, Source, MapDict, self.Logger)
        self.assertEqual(Target.a[0]["test"], TestValue)
        self.assertEqual(Target.a[1][0]["b"], TestValue)
        self.assertEqual(Target.a[1][1].c, TestValue)
        self.assertEqual(Target.a[1][1].value, TestValue)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_LoadDefinition)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_MapValues)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.StructureMapping module tests 2...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)