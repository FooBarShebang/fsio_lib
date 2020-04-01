#!/usr/bin/python
"""
Module fsio_lib.Tests.ut001_structure_mapping

Implements unit testing of the module StructureMapping. See test report TE001.
"""

__version__ = "0.1.0.1"
__date__ = "15-11-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import xml.etree.ElementTree as ElementTree
import copy

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import fsio_lib.StructureMapping as TestModule

#globals - helper test values

TEST_DICT = {"a" : [{"test" : 1}, [{"b" : 2}, {"c" : 3, "value" : 4}]]}

# TEST_DICT is this structure
# {
#    "a" : [
#           {"test" : 1},
#           [
#               {"b" : 2},
#               {
#                   "c" : 3,
#                   "value" : 4
#               }
#       ]
#   ]
# }

TEST_ET_ELEMENT = ElementTree.Element('root')
TEST_ET_ELEMENT.text = "root text"
TEST_ET_ELEMENT.tail = "root tail"
objTemp = ElementTree.SubElement(TEST_ET_ELEMENT, 'a')
objTemp.text = "a text"
objTemp.tail = "a tail"
ElementTree.SubElement(objTemp, 'node', attrib = {"test" : "1"})
objTemp = ElementTree.SubElement(objTemp, 'node')
objChild = ElementTree.SubElement(objTemp, 'sub-node', attrib = {"b" : "2"})
objChild.text = "b text"
objChild.tail = "b tail"
ElementTree.SubElement(objTemp, 'sub-node', attrib = {"c" : "3", "value" : "4"})

# TEST_ET_ELEMENT should be this XML structure:
# <root>root text
#   <a>a text
#       <node test="1" />
#       <node>
#           <sub-node b="2">b text</sub-node>b tail
#           <sub-node c="3" value="4" /></node>
#   </a>a tail
# </root>root tail

# checks on existance of the output folder

strTemp = os.path.join(LIB_ROOT, 'Tests', 'Output')

if not os.path.isdir(strTemp):
    os.mkdir(strTemp)

#classes

#+ helper classes

class InnerClass(object):
    
    def __init__(self):
        self.c = 3
        self.value = 4

class OuterClass(object):
    
    def __init__(self):
        self.a = [{"test" : 1}, [{"b" : 2}, InnerClass()]]

# Instance of OuterClass has the following structure
# OuterClass(
#   a = [
#       {"test" : 1},
#       [
#           {"b" : 2},
#           InnerClass(
#                       c = 3
#                       value = 4
#                   )
#   ]
# ]
# )

#+ test cases

class Test_FlattenPath(unittest.TestCase):
    """
    Test cases for the function FlattenPath of the module StructureMapping.
    
    Implements tests ID TEST-T-100, TEST-T-101, TEST-T-102.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.FlattenPath)
        cls.TestGoodCases = [
            (1 , [1]),
            ("a" , ["a"]),
            ("$a" , ["$a"]),
            ("#a" , ["#a"]),
            ("a.b.c" , ["a", "b", "c"]),
            ("$a.b.c" , ["$a.b.c"]),
            ("#a.b.c" , ["#a.b.c"]),
            ({"test" : "check", "id" : 2, "correction" : -0.5, "pass" : True} ,
                [{"test": "check", "id": 2, "correction": -0.5, "pass": True}]),
            ([1] , [1]),
            (["a"] , ["a"]),
            (["$a"] , ["$a"]),
            (["#a"] , ["#a"]),
            (["a.b.c"] , ["a", "b", "c"]),
            (["$a.b.c"] , ["$a.b.c"]),
            (["#a.b.c"] , ["#a.b.c"]),
            ([{"test" : "check", "id" : 2, "correction" : -0.5, "pass" : True}],
                [{"test": "check", "id": 2, "correction": -0.5, "pass": True}]),
            (["a", 1, {"test" : "check", "id" : 2}],
                ["a", 1, {"test" : "check", "id" : 2}]),
            (["a.b.c", "$b.e", "#d.e", [1, {"test" : "check", "id" : 2}]],
                ["a", "b", "c", "$b.e", "#d.e", 1, {"test" :"check", "id": 2}]),
            (("a.b.c", "$b.e", "#d.e", (1, {"test" : "check", "id" : 2})),
                ["a", "b", "c", "$b.e", "#d.e", 1, {"test" : "check", "id": 2}])
        ]
        cls.TestTypeError = [1.0, True, False, int, float, bool, [1.0],
            (True, ), {1 : "name"}, {True : "name"}, [1, {1 : "name"}],
            {"name" : [1]}, {"name" : (1, 2)}
        ]
        cls.TestValueError = [-1, [-1], (2, [-1]), '', [''], '#', '$', ["#"],
                                ['$'], [], tuple(), {},
        ]
    
    def test_RaiseTypeError(self):
        """
        Tests that the function raises TypeError exception if at least one
        element of the path is of inproper type.
        
        Test ID - TEST-T-100. Covers REQ-AWM-100.
        """
        for gItem in self.TestTypeError:
            with self.assertRaises(TypeError):
                self.TestFunction(gItem)
    
    def test_RaiseValueError(self):
        """
        Tests that the function raises ValueError exception if at least one
        element of the path is of improper value.
        
        Test ID - TEST-T-101. Covers REQ-AWM-101.
        """
        for gItem in self.TestValueError:
            with self.assertRaises(ValueError):
                self.TestFunction(gItem)
    
    def test_ReturnFlattenPath(self):
        """
        Tests that the function returns the expected result with the proper
        input.
        
        Test ID - TEST-T-102. Covers REQ-FUN-100.
        """
        for gInput, gOutput in self.TestGoodCases:
            self.assertEqual(self.TestFunction(gInput), gOutput)

class Test_ResolvePathSubstitutions(unittest.TestCase):
    """
    Test cases for the function ResolvePathSubstitutions of the module
    StructureMapping.
    
    Tests ID TEST-T-110, TEST-T-111, TEST-T-112.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.ResolvePathSubstitutions)
        cls.UndefinedPatterns = [
            {"$1" : "a", "$3" : "$2"}
        ]
        cls.CircularPatterns = [
            {"$1" : "a", "$2" : "$3", "$3" : "$2"}
        ]
        cls.ProperPatterns = [
            ({"$1" : "a", "$2" : "b", "$3" : ["$1", "$2"], "$4" : ["$3", "c"]},
            {"$1" : ["a"], "$2" : ["b"], "$3" : ["a", "b"],
            "$4" : ["a", "b", "c"]})
        ]
    
    def test_RaiseValueErrorUndefined(self):
        """
        Tests that the function raises ValueError exception if at least one
        pattern definition refers an undefined (in the same dictionary) pattern.
        
        Test ID - TEST-T-110. Covers REQ-AWM-111.
        """
        for dictPattern in self.UndefinedPatterns:
            with self.assertRaises(ValueError):
                self.TestFunction(dictPattern)
    
    def test_RaiseValueErrorCircular(self):
        """
        Tests that the function raises ValueError exception if at least one pair
        of pattern definitions mutually refers each other.
        
        Test ID - TEST-T-110. Covers REQ-AWM-111.
        """
        for dictPattern in self.CircularPatterns:
            with self.assertRaises(ValueError):
                self.TestFunction(dictPattern)
    
    def test_RaiseValueErrorPath(self):
        """
        Tests that the function raises ValueError exception if at least one
        element of the path is of improper value. Uses test cases values from
        the Test_FlattenPath.TestValueError.
        
        Test ID - TEST-T-110. Covers REQ-AWM-101.
        """
        for gItem in Test_FlattenPath.TestValueError:
            dictTest = {"$1" : gItem}
            with self.assertRaises(ValueError):
                self.TestFunction(dictTest)
    
    def test_RaiseValueErrorKey(self):
        """
        Tests that the function raises ValueError exception if at least one
        key of the passed dictionary is a string, but it does not start with the
        '$' character.
        
        Test ID - TEST-T-110. Covers REQ-AWM-111.
        """
        dictTest = {"$1" : 'a', 'b' : 1}
        with self.assertRaises(ValueError):
            self.TestFunction(dictTest)
        dictTest = {"$1" : 'a', '$' : 1}
        with self.assertRaises(ValueError):
            self.TestFunction(dictTest)
    
    def test_RaiseTypeErrorPath(self):
        """
        Tests that the function raises TypeError exception if at least one
        element of the path isof improper type. Uses test cases values from
        the Test_FlattenPath.TestTypeError.
        
        Test ID - TEST-T-111. Covers REQ-AWM-100.
        """
        for gItem in Test_FlattenPath.TestTypeError:
            dictTest = {"$1" : gItem}
            with self.assertRaises(TypeError):
                self.TestFunction(dictTest)
    
    def test_RaiseTypeErrorKey(self):
        """
        Tests that the function raises TypeError exception if at least one
        key of the passed dictionary is not a string.
        
        Test ID - TEST-T-111. Covers REQ-AWM-110.
        """
        for gKey in [1, 1.0, True, (2, "2"), int, float, str]:
            dictTest = {"$1" : 'a', gKey : 1}
            with self.assertRaises(TypeError):
                self.TestFunction(dictTest)
    
    def test_RaiseTypeErrorArg(self):
        """
        Tests that the function raises TypeError exception if the passed
        argument is not a mapping type (dictionary).
        
        Test ID - TEST-T-111. Covers REQ-AWM-110.
        """
        for gType in [1, 1.0, True, (2, "2"), int, float, str, [1]]:
            with self.assertRaises(TypeError):
                self.TestFunction(gType)
    
    def test_ReturnResolvePathSubstituions(self):
        """
        Tests that the function returns the properly resolved nested path
        substituion definitions.
        
        Test ID - TEST-T-112. Covers REQ-FUN-100, REQ-FUN-102.
        """
        for dictPattern, dictResult in self.ProperPatterns:
            self.assertDictEqual(self.TestFunction(dictPattern), dictResult)

class Test_GetElement(unittest.TestCase):
    """
    Test cases for the function GetElement of the module StructureMapping.
    
    Implements tests ID TEST-T-120, TEST-T-121, TEST-T-122, TEST-T-123.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.GetElement)
        cls.TestObjects = [TEST_DICT, TEST_ET_ELEMENT, OuterClass()]
        cls.TestGoodCases = [
            (["a", 0, "test"], 1),
            (["a", 1, 0, "b"], 2),
            (["a", 1, 1, "c"], 3),
            (["a", 1, 1, "value"], 4),
            (["a", {"test" : 1}, "test"], 1),
            (["a", 1, {"b" : 2}, "b"], 2),
            (["a", 1, {"c" : 3}, "c"], 3),
            (["a", 1, {"c" : 3}, "value"], 4),
            (["a", 1, {"value" : 4}, "c"], 3),
            (["a", 1, {"value" : 4}, "value"], 4),
            (["a", 1, {"c" : 3, "value" : 4}, "c"], 3),
            (["a", 1, {"c" : 3, "value" : 4}, "value"], 4)
        ]
        cls.TestBadCases = [ "b", "a.b", ["a", 0, "b"], ["a", 0, "test", "b"],
                            ["a", 1, "b"], ["a", 1, 0, "c"], ["a", 1, 1, "b"]]
    
    def test_RaiseTypeErrorPath(self):
        """
        Tests that the function raises TypeError exception if at least one
        element of the path is of improper type. Uses test cases values from
        the Test_FlattenPath.TestTypeError.
        
        Test ID - TEST-T-120. Covers requirement REQ-AWM-100.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestTypeError:
                with self.assertRaises(TypeError):
                    self.TestFunction(gTestObject, gPath)
    
    def test_RaiseValueErrorPath(self):
        """
        Tests that the function raises ValueError exception if at least one
        element of the path is of improper value. Uses test cases values from
        the Test_FlattenPath.TestValueError.
        
        Test ID - TEST-T-121. Covers requirement REQ-AWM-101.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestValueError:
                with self.assertRaises(ValueError):
                    self.TestFunction(gTestObject, gPath)
    
    def test_RaiseAttributeError(self):
        """
        Tests that the function raises AttributeError exception if at least one
        element of the path is not found.
        
        Test ID - TEST-T-122. Covers requirement REQ-AWM-102.
        """
        for gTestObject in self.TestObjects:
            for gPath in self.TestBadCases:
                with self.assertRaises(AttributeError):
                    self.TestFunction(gTestObject, gPath)
    
    def test_ReturnGetElement(self):
        """
        Tests that the function finds the required nested attribute and returns
        its value, with the numbers (floating point or integer) stored in a
        string being converted into float and int respectively.
        
        Test ID - TEST-T-123. Covers requirement REQ-FUN-101.
        """
        for gTestObject in self.TestObjects:
            for glstPath, gResult in self.TestGoodCases:
                gTest = self.TestFunction(gTestObject, glstPath)
                self.assertEqual(gTest, gResult)
        gTestObject = TEST_ET_ELEMENT
        for glstPath, gResult in self.TestGoodCases:
            _glstPath = list(glstPath)
            _glstPath[0] = {"tag" : glstPath[0]}
            gTest = self.TestFunction(gTestObject, _glstPath)
            self.assertEqual(gTest, gResult)
        self.assertEqual(self.TestFunction(gTestObject, 'text'), 'root text')
        self.assertEqual(self.TestFunction(gTestObject, 'tail'), 'root tail')
        self.assertEqual(self.TestFunction(gTestObject, ['a', 'text']),'a text')
        self.assertEqual(self.TestFunction(gTestObject, ['a', 'tail']),'a tail')
        self.assertEqual(self.TestFunction(gTestObject, ['a', 1, {"b" : 2},
                                                            'text']),'b text')
        self.assertEqual(self.TestFunction(gTestObject, ['a', 1, {"b" : 2},
                                                            'tail']),'b tail')

class Test_SetElement(unittest.TestCase):
    """
    Test cases for the function SetElement of the module StructureMapping.
    
    Implements tests ID TEST-T-130, TEST-T-131, TEST-T-132, TEST-T-133.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.SetElement)
        cls.TestObjects = Test_GetElement.TestObjects
        cls.TestMissingPaths = Test_GetElement.TestBadCases
        cls.TestGoodCases = [
            (["a", 0, "test"], 1),
            (["a", 1, 0, "b"], 2),
            (["a", 1, 1, "c"], 3),
            (["a", 1, 1, "value"], 4),
            (["a", 1, {"c" : 3}, "value"], 4),
            (["a", 1, {"value" : 4}, "c"], 3)
        ]
    
    def test_RaiseTypeErrorPath(self):
        """
        Tests that the function raises TypeError exception if at least one
        element of the path is of improper type. Uses test cases values from
        the Test_FlattenPath.TestTypeError.
        
        Test ID - TEST-T-130. Covers requirement REQ-AWM-100.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestTypeError:
                with self.assertRaises(TypeError):
                    self.TestFunction(gTestObject, gPath, 1)
    
    def test_RaiseValueErrorPath(self):
        """
        Tests that the function raises ValueError exception if at least one
        element of the path is of improper value. Uses test cases values from
        the Test_FlattenPath.TestValueError.
        
        Test ID - TEST-T-131. Covers requirement REQ-AWM-101.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestValueError:
                with self.assertRaises(ValueError):
                    self.TestFunction(gTestObject, gPath, 1)
    
    def test_RaiseAttributeError(self):
        """
        Tests that the function raises AttributeError exception if at least one
        element of the path is not found.
        
        Test ID - TEST-T-132. Covers requirement REQ-AWM-102.
        """
        for gTestObject in self.TestObjects:
            for gPath in self.TestMissingPaths:
                with self.assertRaises(AttributeError):
                    self.TestFunction(gTestObject, gPath, 1)
    
    def test_RaiseTypeErrorValuePath(self):
        """
        The function must raise the TypeError exception if an XML node object is
        attempted to be assigned as an attribute of another XML node object (not
        as a sub-element), or a non XML node is attempted to be assigned to a
        sub-element of an XML node, or an immutable sequence as the last element
        is attempted to be modified. The path is proper.
        
        Test ID - TEST-T-130 - part 2. Covers requirement REQ-AWM-100.
        """
        gTestObject = TEST_ET_ELEMENT
        gPath = 'a' #assigning not a node to a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, 1)
        gPath = ['a', 0] #assigning not a node to a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, 1)
        gPath = ['a', 1, {'b' : 2}] #assigning not a node to a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, 1)
        objNew = ElementTree.Element('new')
        gPath = ['a', 'text'] #assigning a node to not a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, objNew)
        gPath = ['a', 'tail'] #assigning a node to not a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, objNew)
        gPath = ['a', 'tag'] #assigning a node to not a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, objNew)
        gPath = ['a', 0, 'test'] #assigning a node to not a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, objNew)
        gPath = ['a', 1, 0, 'b'] #assigning a node to not a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, objNew)
        gPath = ['a', 1, {'b' : 2}, 'b'] #assigning a node to not a node
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, objNew)
        gTestObject = (1, 2) #immutable
        gPath = 1
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, 1)
        gTestObject = {"a" : (1, 2)} #immutable
        gPath = ["a", 1]
        with self.assertRaises(TypeError):
            self.TestFunction(gTestObject, gPath, 1)
    
    def test_ProperSetElement(self):
        """
        The function must perform proper values assignment to the end and
        intermediate nested attributes, as long as the path is proper and the
        conditions of the test UT0001.4.4 are not applicable (no type conflict).
        
        Test ID - TEST-T-133. Covers requirement REQ-FUN-101.
        """
        TestValue = 42
        #end nodes
        for gTestObject in self.TestObjects:
            for glstPath, gResult in self.TestGoodCases:
                self.TestFunction(gTestObject, glstPath, TestValue)
                gTest = TestModule.GetElement(gTestObject, glstPath)
                self.assertEqual(gTest, TestValue)
                self.TestFunction(gTestObject, glstPath, gResult)
                gTest = TestModule.GetElement(gTestObject, glstPath)
                self.assertEqual(gTest, gResult)
        gTestObject = TEST_ET_ELEMENT
        for glstPath, gResult in self.TestGoodCases:
            _glstPath = list(glstPath)
            _glstPath[0] = {"tag" : glstPath[0]}
            self.TestFunction(gTestObject, _glstPath, TestValue)
            gTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertEqual(gTest, TestValue)
            self.TestFunction(gTestObject, _glstPath, gResult)
            gTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertEqual(gTest, gResult)
        for glstPath in ['text', 'tail', ['a', 'text'], ['a', 'tail'],
                            ['a', 1, {"b" : 2}, 'text'],
                            ['a', 1, {"b" : 2}, 'tail']]:
            gResult = TestModule.GetElement(gTestObject, glstPath)
            self.TestFunction(gTestObject, glstPath, TestValue)
            gTest = TestModule.GetElement(gTestObject, glstPath)
            self.assertEqual(gTest, TestValue)
            self.TestFunction(gTestObject, glstPath, gResult)
            gTest = TestModule.GetElement(gTestObject, glstPath)
            self.assertEqual(gTest, gResult)
        #intermediate modes
        objNewItem = ElementTree.Element("new", attrib = {'attr' : "42"})
        for glstPath, gResult in self.TestGoodCases[:-2]:
            _glstPath = glstPath[:-1]
            objOldItem = TestModule.GetElement(gTestObject, _glstPath)
            self.TestFunction(gTestObject, _glstPath, objNewItem)
            objTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertIs(objTest, objNewItem)
            self.TestFunction(gTestObject, _glstPath, objOldItem)
            objTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertIs(objTest, objOldItem)
        for glstPath, gResult in self.TestGoodCases:
            gTest = TestModule.GetElement(gTestObject, glstPath)
            self.assertEqual(gTest, gResult) #fully restored!
        for gTestObject in [TEST_DICT, OuterClass()]:
            for glstPath, gResult in self.TestGoodCases[:-2]:
                _glstPath = glstPath[:-1]
                objOldItem = TestModule.GetElement(gTestObject, _glstPath)
                self.TestFunction(gTestObject, _glstPath, TestValue)
                objTest = TestModule.GetElement(gTestObject, _glstPath)
                self.assertEqual(objTest, TestValue)
                self.TestFunction(gTestObject, _glstPath, objOldItem)
                objTest = TestModule.GetElement(gTestObject, _glstPath)
                self.assertEqual(objTest, objOldItem)
            for glstPath, gResult in self.TestGoodCases:
                gTest = TestModule.GetElement(gTestObject, glstPath)
                self.assertEqual(gTest, gResult) #fully restored!

class Test_DeleteElement(unittest.TestCase):
    """
    Test cases for the function DeleteElement of the module StructureMapping.
    
    Implements tests ID TEST-T-140, TEST-T-141, TEST-T-142, TEST-T-143.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.DeleteElement)
        cls.TestObjects = Test_GetElement.TestObjects
        cls.TestMissingPaths = Test_GetElement.TestBadCases
        cls.TestGoodCases = [["a"], ["a", 1], ["a", 1, 1], ["a", 1, 1, "c"],
                            ["a", 1, 1, "value"], ["a", 1, {"c" : 3}, "value"],
                            ["a", 1, {"value" : 4}, "c"]]
    
    def test_RaiseTypeErrorPath(self):
        """
        Tests that the function raises TypeError exception if at least one
        element of the path is of improper type. Uses test cases values from
        the Test_FlattenPath.TestTypeError.
        
        Test ID - TEST-T-140. Covers requirement REQ-AWN-100.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestTypeError:
                with self.assertRaises(TypeError):
                    self.TestFunction(gTestObject, gPath)
    
    def test_RaiseValueErrorPath(self):
        """
        Tests that the function raises ValueError exception if at least one
        element of the path is of improper value. Uses test cases values from
        the Test_FlattenPath.TestValueError.
        
        Test ID - TEST-T-141. Covers requirement REQ-AWN-101.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestValueError:
                with self.assertRaises(ValueError):
                    self.TestFunction(gTestObject, gPath)
    
    def test_RaiseAttributeError(self):
        """
        Tests that the function raises AttributeError exception if at least one
        element of the path is not found.
        
        Test ID - TEST-T-142. Covers requirement REQ-AWN-102.
        """
        for gTestObject in self.TestObjects:
            for gPath in self.TestMissingPaths:
                with self.assertRaises(AttributeError):
                    self.TestFunction(gTestObject, gPath)
    
    def test_ProperDeleteElement(self):
        """
        The function must perform proper deletion of the end and intermediate
        nested attributes.
        
        Test ID - TEST-T-143. Covers requirement REQ-FUN-101.
        """
        for gTestObject in self.TestObjects:
            for glstPath in self.TestGoodCases:
                iIndex = len(glstPath)
                while iIndex > 0:
                    _glstPath = glstPath[:iIndex]
                    objTest = copy.deepcopy(gTestObject)
                    self.TestFunction(objTest, _glstPath)
                    for iTemp in range(1, len(_glstPath)):
                        TestModule.GetElement(objTest, glstPath[:iTemp])
                        #should be ok - elements before deleted
                    for iTemp in range(len(_glstPath), len(glstPath) + 1):
                        with self.assertRaises(AttributeError):
                            TestModule.GetElement(objTest, glstPath[:iTemp])
                            #elements from and after the deleted
                    iIndex -= 1
        #special cases - text, tail and tag of an XML node
        objTest = copy.deepcopy(TEST_ET_ELEMENT)
        self.assertIsNotNone(TestModule.GetElement(objTest, ["a", "text"]))
        self.assertIsNotNone(TestModule.GetElement(objTest, ["a", "tail"]))
        self.assertEqual(TestModule.GetElement(objTest, ["a", "tag"]), "a")
        self.TestFunction(objTest, ["a", "text"])
        self.assertIsNone(TestModule.GetElement(objTest, ["a", "text"]))
        self.TestFunction(objTest, ["a", "tail"])
        self.assertIsNone(TestModule.GetElement(objTest, ["a", "tail"]))
        #deletion of the tag of a node => renaming to 'def_node'!
        self.TestFunction(objTest, ["a", "tag"])
        with self.assertRaises(AttributeError):
            TestModule.GetElement(objTest, "a")
        TestModule.GetElement(objTest, "def_node")
        self.assertEqual(TestModule.GetElement(objTest, ["def_node", "tag"]),
                                                                    "def_node")
        #direct deletion of a node
        objTest = copy.deepcopy(TEST_ET_ELEMENT)
        self.TestFunction(objTest, "a")
        with self.assertRaises(AttributeError):
            TestModule.GetElement(objTest, "a")
        with self.assertRaises(AttributeError):
            TestModule.GetElement(objTest, "def_node")

class Test_AddElement(unittest.TestCase):
    """
    Test cases for the function DeleteElement of the module StructureMapping.
    
    Implements tests ID TEST-T-150, TEST-T-151, TEST-T-152, TEST-T-153.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.AddElement)
        cls.TestObjects = Test_GetElement.TestObjects
        cls.TestGoodCases = [
            (["a", 0, "test"], 1),
            (["a", 1, 0, "b"], 2),
            (["a", 1, 1, "c"], 3),
            (["a", 1, 1, "value"], 4),
            (["a", 1, {"c" : 3}, "value"], 4),
            (["a", 1, {"value" : 4}, "c"], 3)
        ] # for testing overwriting!
        cls.TestValueError = [-1, [-1], (2, [-1]), [''], '#', '$', ["#"],
                                ['$'], {} ]
        cls.TestBadMissingPaths = [
            ["a", 1, "b"], ["a", 0, "b", 1], [1, "a"], ["a", 1], [1],
            ["a", {"b" : 1}], ["a", {"b" : 1}, "c"], ["a", {"b" : 1}, 0],
            [{"b" : 1}, "c"], [{"b" : 1}, 1], [1, {"b" : 1}]
        ]
    
    def test_RaiseTypeErrorPath(self):
        """
        Tests that the function raises TypeError exception if at least one
        element of the path is of improper type. Uses test cases values from
        the Test_FlattenPath.TestTypeError.
        
        Test ID - TEST-T-150. Covers requirement REQ-AWN-100.
        """
        for gTestObject in self.TestObjects:
            for gPath in Test_FlattenPath.TestTypeError:
                with self.assertRaises(TypeError):
                    self.TestFunction(gTestObject, gPath, 1)
    
    def test_RaiseValueErrorPath(self):
        """
        Tests that the function raises ValueError exception if at least one
        element of the path is of improper value.
        
        Test ID - TEST-T-151. Covers requirement REQ-AWN-101.
        """
        for gTestObject in self.TestObjects:
            for gPath in self.TestValueError:
                with self.assertRaises(ValueError):
                    self.TestFunction(gTestObject, gPath, 1)
            if not (gTestObject is TEST_ET_ELEMENT):
                for gPath in ['', [], tuple(), None]:
                    with self.assertRaises(ValueError):
                        self.TestFunction(gTestObject, gPath, 1)
    
    def test_ProperSetElement(self):
        """
        The function must perform proper values assignment to the end and
        intermediate nested attributes, as long as the path is proper and the
        conditions of the test UT0001.4.4 are not applicable (no type conflict),
        and the target attribute exists in the target object.
        
        Test ID - TEST-T-153. Covers requirement REQ-FUN-101.
        """
        TestValue = 42
        #end nodes
        for gTestObject in self.TestObjects:
            for glstPath, gResult in self.TestGoodCases:
                self.TestFunction(gTestObject, glstPath, TestValue)
                gTest = TestModule.GetElement(gTestObject, glstPath)
                self.assertEqual(gTest, TestValue)
                self.TestFunction(gTestObject, glstPath, gResult)
                gTest = TestModule.GetElement(gTestObject, glstPath)
                self.assertEqual(gTest, gResult)
        gTestObject = TEST_ET_ELEMENT
        for glstPath, gResult in self.TestGoodCases:
            _glstPath = list(glstPath)
            _glstPath[0] = {"tag" : glstPath[0]}
            self.TestFunction(gTestObject, _glstPath, TestValue)
            gTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertEqual(gTest, TestValue)
            self.TestFunction(gTestObject, _glstPath, gResult)
            gTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertEqual(gTest, gResult)
        for glstPath in ['text', 'tail', ['a', 'text'], ['a', 'tail'],
                            ['a', 1, {"b" : 2}, 'text'],
                            ['a', 1, {"b" : 2}, 'tail']]:
            gResult = TestModule.GetElement(gTestObject, glstPath)
            self.TestFunction(gTestObject, glstPath, TestValue)
            gTest = TestModule.GetElement(gTestObject, glstPath)
            self.assertEqual(gTest, TestValue)
            self.TestFunction(gTestObject, glstPath, gResult)
            gTest = TestModule.GetElement(gTestObject, glstPath)
            self.assertEqual(gTest, gResult)
        #intermediate modes
        objNewItem = ElementTree.Element("new", attrib = {'attr' : "42"})
        for glstPath, gResult in self.TestGoodCases[:-2]:
            _glstPath = glstPath[:-1]
            objOldItem = TestModule.GetElement(gTestObject, _glstPath)
            self.TestFunction(gTestObject, _glstPath, objNewItem)
            objTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertIs(objTest, objNewItem)
            self.TestFunction(gTestObject, _glstPath, objOldItem)
            objTest = TestModule.GetElement(gTestObject, _glstPath)
            self.assertIs(objTest, objOldItem)
        for glstPath, gResult in self.TestGoodCases:
            gTest = TestModule.GetElement(gTestObject, glstPath)
            self.assertEqual(gTest, gResult) #fully restored!
        for gTestObject in [TEST_DICT, OuterClass()]:
            for glstPath, gResult in self.TestGoodCases[:-2]:
                _glstPath = glstPath[:-1]
                objOldItem = TestModule.GetElement(gTestObject, _glstPath)
                self.TestFunction(gTestObject, _glstPath, TestValue)
                objTest = TestModule.GetElement(gTestObject, _glstPath)
                self.assertEqual(objTest, TestValue)
                self.TestFunction(gTestObject, _glstPath, objOldItem)
                objTest = TestModule.GetElement(gTestObject, _glstPath)
                self.assertEqual(objTest, objOldItem)
            for glstPath, gResult in self.TestGoodCases:
                gTest = TestModule.GetElement(gTestObject, glstPath)
                self.assertEqual(gTest, gResult) #fully restored!
    
    def test_RaiseAttributeErrorNotNames(self):
        """
        The function must raise AttributeError if either a numeric index or a
        'choice' dictionary element is encountered in the 'missing' part of the
        path after the 'branching' point.
        
        Test ID - TEST-T-152. Covers requirement REQ-AWN-102.
        """
        TestValue = 42
        for gTestObject in self.TestObjects:
            for glstPath, gResult in self.TestGoodCases:
                for gsltBadPath in self.TestBadMissingPaths:
                    glstTestPath = glstPath[:-1] + gsltBadPath
                    with self.assertRaises(AttributeError):
                        self.TestFunction(gTestObject, glstTestPath, TestValue)
    
    def test_RaiseAttributeErrorNotNode(self):
        """
        The function must raise AttributeError if the 'branching' point (last
        existing element along the path) is either not an XML node or an
        immutable object.
        
        Test ID - TEST-T-152 - part 2. Covers requirement REQ-AWN-102.
        """
        TestValue = 42
        #not XML node / end node (int) to append a branch
        for gTestObject in self.TestObjects:
            for glstPath, _ in self.TestGoodCases:
                glstTestPath = list(glstPath)
                glstTestPath.append("a")
                with self.assertRaises(AttributeError):
                    self.TestFunction(gTestObject, glstTestPath, TestValue)
        #immutable object (tuple) to append a branch into
        TestDict = {"a" : (1, 2)}
        glstTestPath = "a.b"
        with self.assertRaises(AttributeError):
            self.TestFunction(TestDict, glstTestPath, TestValue)
    
    def test_ProperAddsNewBranch(self):
        """
        The function must properly add new branch from the deepest existing
        element. For the non XML tree target object - intermediate levels as
        dictionaries, the last element - as key : value pair with the key is the
        last element in the path and the value - as passed. For an XML tree
        target object - all but last elements as nested nodes, the last element
        as a node as well if the passed values is a node itself, otherwise - the
        last element as the attribute name, and the passed value as its value.
        
        Test ID - TEST-T-153 - part 2. Covers requirement REQ-FUN-101.
        """
        glstMissingPath = "a.b.c"
        iValue = 42
        for gPatternObject in self.TestObjects:
            for glstPath, _ in self.TestGoodCases:
                gTestPath = glstPath[:-1]
                gTestPath.append(glstMissingPath)
                gTestObject = copy.deepcopy(gPatternObject)
                self.TestFunction(gTestObject, gTestPath, iValue)
                if not isinstance(gTestObject, ElementTree.Element):
                    tCheckType = dict
                else:
                    tCheckType = ElementTree.Element
                gCheckPath = glstPath[:-1]
                gCheckPath.append("a")
                self.assertIsInstance(TestModule.GetElement(gTestObject,
                                                        gCheckPath), tCheckType)
                gCheckPath.append("b")
                self.assertIsInstance(TestModule.GetElement(gTestObject,
                                                        gCheckPath), tCheckType)
                gCheckPath.append("c")
                self.assertEqual(TestModule.GetElement(gTestObject, gCheckPath),
                                                                        iValue)
                if isinstance(gTestObject, ElementTree.Element):
                    #extra check - addition of a new node, not an attribute
                    gTestObject = copy.deepcopy(gPatternObject)
                    etNewNode = ElementTree.Element('new_node')
                    self.TestFunction(gTestObject, gTestPath, etNewNode)
                    gCheckPath = glstPath[:-1]
                    for strName in ["a", "b", "c", "new_node"]:
                        gCheckPath.append(strName)
                        gCheckObject = TestModule.GetElement(gTestObject,
                                                                    gCheckPath)
                        self.assertIsInstance(gCheckObject, tCheckType)
                        self.assertEqual(gCheckObject.tag, strName)
        #add to the top
        for strName in ["a", "a.b", "a.b.c"]:
            objTest = [] #sequence
            self.TestFunction(objTest, strName, iValue)
            self.assertEqual(TestModule.GetElement(objTest, [0, strName]),
                                                                        iValue)
            objTest = {} #dictionary
            self.TestFunction(objTest, strName, iValue)
            self.assertEqual(TestModule.GetElement(objTest, strName), iValue)
            objTest = InnerClass() #struct object
            self.TestFunction(objTest, strName, iValue)
            self.assertEqual(TestModule.GetElement(objTest, strName), iValue)
            objTest = ElementTree.Element('test') #XML tree of one node
            self.TestFunction(objTest, strName, iValue)
            self.assertEqual(TestModule.GetElement(objTest, strName), iValue)
        #special case - node to the top node without path
        for gPath in ['', [], tuple(), None]:
            objTest = ElementTree.Element('test')
            objNewNode = ElementTree.Element('node')
            self.TestFunction(objTest, gPath, objNewNode)
            self.assertEqual(TestModule.GetElement(objTest, 'node').tag, 'node')

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_FlattenPath)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(
                                                Test_ResolvePathSubstitutions)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetElement)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_SetElement)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_DeleteElement)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_AddElement)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6])

if __name__ == "__main__":
    sys.stdout.write("Conducting fsio_lib.StuctureMapping module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)