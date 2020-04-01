# TE001 Test Report on the Module fsio_lib.StructureMapping

## Conventions

Each test is defined following the same format. Each test receives a unique test identifier and a reference to the ID(s) of the requirements it covers (if applicable). The goal of the test is described to clarify what is to be tested. The test steps are described in brief but clear instructions. For each test it is defined what the expected results are for the test to pass. Finally, the test result is given, this can be only pass or fail.

The test format is as follows:

**Test Identifier:** TEST-\[I/A/D/T\]-XYZ

**Requirement ID(s)**: REQ-uvw-xyz

**Verification method:** I/A/D/T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

The test ID starts with the fixed prefix 'TEST'. The prefix is followed by a single letter, which defines the test type / verification method. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the test ordering number for this object. E.g. 'TEST-T-112'. Each test type has its own counter, thus 'TEST-T-112' and 'TEST-A-112' tests are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Tests preparations

Write the unit tests cases (classes and methods) implementing the defined tests - modules *Tests/ut001_structure_mapping.py* and *Tests/ut002_structure_mapping.py*. Define a number of correct and incorrect path definitions to test the basic functionality. Define a class simulating a nested C-stuct, a dictionary repesenting the same nested structure, and an XML ElementTree object reprenting the same structure using the following conventions:

Dictionary:

```python
{
   "a" : [
          {"test" : 1},
          [
              {"b" : 2},
              {
                  "c" : 3,
                  "value" : 4
              }
      ]
  ]
}
```

Nested struct object:

```python
OuterClass(
  a = [
      {"test" : 1},
      [
          {"b" : 2},
          InnerClass(
                      c = 3
                      value = 4
                  )
      ]
    ]
)
```

XML ElementTree:

```xml
<root>root text
  <a>a text
      <node test="1" />
      <node>
          <sub-node b="2">b text</sub-node>b tail
          <sub-node c="3" value="4" /></node>
  </a>a tail
</root>root tail
```

Create a number of templates describing the data mapping rules for the structure of such and object using incremental changes (later templates including previously defined). Create a number of templates with various *faults*: spelling, wrong type or values of the path elements, missing and circular definitions for the path substitutions.

## Tests definition (Test)

**Test Identifier:** TEST-T-100

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Function FlattenPath() raises TypeError if the received argument is not of any of the types allowed by DSL definition

**Expected result:** The expected exception is raised when the function receives an argument of a type not in:

* integer number, but not boolean type
* string
* dictionary (mapping type in general) of string keys and values of any of the numeric types (including boolean and floating point) or strings
* flat sequence (list, tuple, etc. - generic sequence) of any of the three types above
* nested sequence of any of the 4 types above

**Test steps:** Execute unit test method *test_RaiseTypeError*() of test class **Test_FlattenPath** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* arguments: floating point number, boolean values, integer data types (instead of data type instances), sequences with floating point, boolean and dictionary elements as well as dicitonaries with non-string keys or values not being strings or numeric types.

**Test result:** PASS

---

**Test Identifier:** TEST-T-101

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Function FlattenPath() raises ValueError if the received argument is a negative integer or an empty string, or an empty name for the path or value substitution, or an empty sequence or dictionary.

**Expected result:** The expected exception is raised when the function receives an argument of a a wrong value.

**Test steps:** Execute unit test method *test_RaiseValueError*() of test class **Test_FlattenPath** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* arguments: negative integers, empty string, '$' and '#' one character strings as well as empty sequences and sequences including the previously described wrong values.

**Test result:** PASS

---

**Test Identifier:** TEST-T-102

**Requirement ID(s)**: REQ-FUN-100

**Verification method:** T

**Test goal:** Function FlattenPath() unifies the passed path according to the DSL specifications: it can accept an integer, a string (including dot(s)), a dictionary of string keys and numeric, boolean or string values, a flat or nested sequence of such elements - the result should be a flat list of integers, strings without commas and dictionaries of string keys and numeric, boolean or string values.

**Expected result:** The function processes the input as expected (returns the same lists as the control values), exceptions are not raised.

**Test steps:** Execute unit test method *test_ReturnFlattenPath*() of test class **Test_FlattenPath** in module *Tests/ut001_structure_mapping.py*, which passes *right* arguments and compare the returned values with the expected and manually constructed results.

**Test result:** PASS

---

**Test Identifier:** TEST-T-110

**Requirement ID(s)**: REQ-AWM-101, REQ-AWM-111

**Verification method:** T

**Test goal:** Function ResolvePathSubstitutions() raises ValueError when the paths substitution dictionary contains entires of the proper data types but with at least one key or value of a wrong value.

**Expected result:** ValueError is raised if:

* all path definitions are contructed from the elements of the proper types, but, at least, one definition contains, at least, one element with a *wrong* value, see TEST-T-101
* at least, one path substitution includes a circular reference (two patterns are defined mutually via each other)
* at least, one path sybstutution includes a not defined macros
* at least, one macros name is a string not starting with '$' or containing only the '$' character 

**Test steps:** Execute unit test methods *test_RaiseValueErrorUndefined*, *test_RaiseValueErrorCircular*, *test_RaiseValueErrorPath* and *test_RaiseValueErrorKey* of test class **Test_ResolvePathSubstitutions** in module *Tests/ut001_structure_mapping.py*, which pass the *wrong* dictionaries as the argument to the ResolvePathSubstitutions() function and check that the ValueError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-111

**Requirement ID(s)**: REQ-AWM-100, REQ-AWM-110

**Verification method:** T

**Test goal:** Function ResolvePathSubstitutions() raises TypeError when the path substitution rules are defined using the *wrong* data types.

**Expected result:** TypeError is raised if:

* Not a dictionary argument is passed into this function
* Any if of the keys in the passed dictionary is not a string
* Any of the values (macros' path substitution definition) is not a string, as in TEST-T-100

**Test steps:** Execute unit test methods *test_RaiseTypeErrorPath*, *test_RaiseTypeErrorKey* and *test_RaiseTypeErrorArg* of test class **Test_ResolvePathSubstitutions** in module *Tests/ut001_structure_mapping.py*, which pass the *wrong* arguments and check that the TypeError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-112

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-102

**Verification method:** T

**Test goal:** Function ResolvePathSubstitutions() properly converts the path substitution definitions into flattened paths, including the recursive definitions.

**Expected result:** The function should accept a dicitonary with the string keys (starting with '$' - macros names) and bound values, which are proper path definitions, which may be not yet flattened, and which can include other macroses defined in the same dictionary (recursive definition), but not unresolvable (missing definitions) macroses. This function must return a dictionary with the string keys (starting with '$' - macros names) and bound flat list values, which are flattened fully resolved paths without any macroses inside. All defined macroses should be resolved and returned.

**Test steps:** Execute unit test method *test_ReturnResolvePathSubstituions* of test class **Test_ResolvePathSubstitutions** in module *Tests/ut001_structure_mapping.py*, which passes a proper path substitution definitions' dictionary in to the function being tested and compares the returned value with the expected result.

**Test result:** PASS

---

**Test Identifier:** TEST-T-120

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Function GetElement() raises TypeError when the passed argument if of the wrong type.

**Expected result:** TypeError is raised if the passed argument is of any value / data type defined in the TEST-T-100.

**Test steps:** Execute unit test method *test_RaiseTypeErrorPath* of test class **Test_GetElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* values defined in TEST-T-100 and checks that the TypeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-121

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Function GetElement() raises ValueError when the passed argument if of the proper type but of the unacceptable value.

**Expected result:** ValueError is raised if the passed argument is of any value defined in the TEST-T-101.

**Test steps:** Execute unit test method *test_RaiseValueErrorPath* of test class **Test_GetElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* values defined in TEST-T-101 and checks that the ValueError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-122

**Requirement ID(s)**: REQ-AWM-102

**Verification method:** T

**Test goal:** Function GetElement() raises AttributeError when the passed argument is a proper path complying with the DSL specifications, but it points to an element, attribute or key, which is not present in the target object.

**Expected result:** The AttributeError is raised in the following situations:

* Access by integer index applied to a dictionary or a structured object (class or class instance), which is not a sequence
* Access by integer index applied to an XML ElementTree node, which doesn't have sub-nodes
* Access by name applied to a sequence - named tuple is an exception and is not considered
* Access by integer index applied to a sequence with the index being greater than or equal to the length of the sequence
* Access by integer index applied to an XML ElementTree node with the index being greater than or equal to the number of the sub-nodes
* Access by name to an attribute of a structured object or an entry of a dictionary, which is not present in the target
* Access by name to an attribute of an XML ElementTree node, which is not present - exept for the 'special' default attributes 'text' and 'tail'

**Test steps:** Execute unit test method *test_RaiseAttributeError* of test class **Test_GetElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* values defined in this test and checks that the AttributeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-123

**Requirement ID(s)**: REQ-FUN-101

**Verification method:** T

**Test goal:** The function GetElement() can access and returns the value of a (nested) sequence's element, attribute of a struct-like object or an XML ElementTree node, entry of a dictionary - provided that the path is properly defined and exists.

**Expected result:** The functions does not raise any exception and returns the value of the corresponding element / entry / attribute, which was assigned during the creation of the target object.

**Test steps:** Execute unit test method *test_ReturnGetElement* of test class **Test_GetElement** in module *Tests/ut001_structure_mapping.py*, which passes the proper and existing paths and checks that the returned values correspond to those that are supposed to be held by the corresponding element / entry / attribute. It also checks the access to the special attributes 'text' and 'tail' of XML ElementTree nodes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-130

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Function SetElement() raises TypeError when the passed 'path' argument if of the wrong type.

**Expected result:** TypeError is raised if the passed 'path' argument is of any value / data type defined in the TEST-T-100. The TypeError should also be raised when any value except for an instance of the XML ElementTree class is assigned to a node of another XML ElementTree instance; or if an instance of ElementTree is assigned to an atribute of another ElementTree instance. The TypeError exception should also be raised upon attempted assignment to an immutable object, e.g. an element of a tuple.

**Test steps:** Execute unit test method *test_RaiseTypeErrorPath* of test class **Test_SetElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* 'path' values defined in TEST-T-100 and checks that the TypeError is raised. It also checks that an XML node object can be assigned only to an XML node, and an existing XML node accepts only XML node instance as its new value, as well as to an element of a tuple.

**Test result:** PASS

---

**Test Identifier:** TEST-T-131

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Function SetElement() raises ValueError when the passed 'path' argument if of the proper type but of the unacceptable value.

**Expected result:** ValueError is raised if the passed argument is of any value defined in the TEST-T-101.

**Test steps:** Execute unit test method *test_RaiseValueErrorPath* of test class **Test_SetElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* 'path' values defined in TEST-T-101 and checks that the ValueError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-132

**Requirement ID(s)**: REQ-AWM-102

**Verification method:** T

**Test goal:** Function SetElement() raises AttributeError when the passed argument is a proper path complying with the DSL specifications, but it points to an element, attribute or key, which is not present in the target object.

**Expected result:** The AttributeError is raised in the following situations:

* Access by integer index applied to a dictionary or a structured object (class or class instance), which is not a sequence
* Access by integer index applied to an XML ElementTree node, which doesn't have sub-nodes
* Access by name applied to a sequence - named tuple is an exception and is not considered
* Access by integer index applied to a sequence with the index being greater than or equal to the length of the sequence
* Access by integer index applied to an XML ElementTree node with the index being greater than or equal to the number of the sub-nodes
* Access by name to an attribute of a structured object or an entry of a dictionary, which is not present in the target
* Access by name to an attribute of an XML ElementTree node, which is not present - exept for the 'special' default attributes 'text' and 'tail'

**Test steps:** Execute unit test method *test_RaiseAttributeError* of test class **Test_SetElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* 'path' values defined in this test and checks that the AttributeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-133

**Requirement ID(s)**: REQ-FUN-101

**Verification method:** T

**Test goal:** The function SetElement() can access and properly changes the value of a (nested) sequence's element, attribute of a struct-like object or an XML ElementTree node, entry of a dictionary - provided that the path is properly defined and exists.

**Expected result:** The functions does not raise any exception. The value of the corresponding element / entry / attribute is indeed changed, and it holds the passed as the second argument value.

**Test steps:** Execute unit test method *test_ProperSetElement* of test class **Test_SetElement** in module *Tests/ut001_structure_mapping.py*, which passes the proper and existing paths as the first argument and a proper value as the second argument,; then it and checks that the modified element / entry / attribute holds the expected value. It also checks the access to the special attributes 'text' and 'tail' of XML ElementTree nodes as well as assignment of an XML ElementTree instance to a (sub-) node of another XML ElementTree instance.

**Test result:** PASS

---

**Test Identifier:** TEST-T-140

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Function DeleteElement() raises TypeError when the passed argument if of the wrong type.

**Expected result:** TypeError is raised if the passed argument is of any value / data type defined in the TEST-T-100.

**Test steps:** Execute unit test method *test_RaiseTypeErrorPath* of test class **Test_DeleteElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* values defined in TEST-T-100 and checks that the TypeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-141

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Function DeleteElement() raises ValueError when the passed argument if of the proper type but of the unacceptable value.

**Expected result:** ValueError is raised if the passed argument is of any value defined in the TEST-T-101.

**Test steps:** Execute unit test method *test_RaiseValueErrorPath* of test class **Test_DeleteElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* values defined in TEST-T-101 and checks that the ValueError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-142

**Requirement ID(s)**: REQ-AWM-102

**Verification method:** T

**Test goal:** Function DeleteElement() raises AttributeError when the passed argument is a proper path complying with the DSL specifications, but it points to an element, attribute or key, which is not present in the target object.

**Expected result:** The AttributeError is raised in the following situations:

* Reference by integer index applied to a dictionary or a structured object (class or class instance), which is not a sequence
* Reference by integer index applied to an XML ElementTree node, which doesn't have sub-nodes
* Reference by name applied to a sequence - named tuple is an exception and is not considered
* Reference by integer index applied to a sequence with the index being greater than or equal to the length of the sequence
* Reference by integer index applied to an XML ElementTree node with the index being greater than or equal to the number of the sub-nodes
* Reference by name to an attribute of a structured object or an entry of a dictionary, which is not present in the target
* Reference by name to an attribute of an XML ElementTree node, which is not present - exept for the 'special' default attributes 'text' and 'tail'

**Test steps:** Execute unit test method *test_RaiseAttributeError* of test class **Test_DeleteElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* values defined in this test and checks that the AttributeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-143

**Requirement ID(s)**: REQ-FUN-101

**Verification method:** T

**Test goal:** The function DeleteElement() can delete a (nested) sequence's element, attribute of a struct-like object or an XML ElementTree node, entry of a dictionary - provided that the path is properly defined and exists.

**Expected result:** The functions does not raise any exception, and the corresponding element / entry / attribute is no longer present afterwards.

**Test steps:** Execute unit test method *test_ProperDeleteElement* of test class **Test_DeleteElement** in module *Tests/ut001_structure_mapping.py*, which passes the proper and existing paths and checks that the returned values correspond to those that are supposed to be held by the corresponding element / entry / attribute. It also checks the access to the special attributes 'text' and 'tail' of XML ElementTree nodes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-150

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Function AddElement() raises TypeError when the passed 'path' argument if of the wrong type.

**Expected result:** TypeError is raised if the passed 'path' argument is of any value / data type defined in the TEST-T-100.

**Test steps:** Execute unit test method *test_RaiseTypeErrorPath* of test class **Test_AddElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* 'path' values defined in TEST-T-100 and checks that the TypeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-151

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Function AddElement() raises ValueError when the passed 'path' argument if of the proper type but of the unacceptable value.

**Expected result:** ValueError is raised if the passed argument is of any value defined in the TEST-T-101. The ValueError should not be raised when the passed path is an empty string, empty list or tuples, or None value and the targte object is an instance of XML ElementTree, when such a path refers to the 'root' of the tree.

**Test steps:** Execute unit test method *test_RaiseValueErrorPath* of test class **Test_AddElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* 'path' values defined in TEST-T-101 and checks that the ValueError is raised. It also checks that an exception is not raised when an empty path is used for an instance of XML ElementTree.

**Test result:** PASS

---

**Test Identifier:** TEST-T-152

**Requirement ID(s)**: REQ-AWM-102

**Verification method:** T

**Test goal:** Function AddElement() raises AttributeError when a new end node (leaf) cannot be created or a missing intermediate node (branch) along the path to a new end node to cannot be created.

**Expected result:** The AttributeError is raised in the following situations:

* The next element in the path is an integer number (element index) or a 'choice dictionary', whereas the current position along the path is neither a sequence nor an XML ElementTree node
* The next element in the path is an integer number (element index), whereas the current position along the path is a sequence or an XML ElementTree node with the amount of elements / sub-nodes less or equal to this number
* The next element in the path is a 'choice dictionary', whereas the current position along the path is a sequence or an XML ElementTree node but an element / sub-node with the required value of the required key / attribute is not found
* The new leaf (end node) must be added to an immutable object, e.g. to a tuple

**Test steps:** Execute unit test methods *test_RaiseAttributeErrorNotNames* and *test_RaiseAttributeErrorNotNode* of test class **Test_AddElement** in module *Tests/ut001_structure_mapping.py*, which passes *wrong* 'path' values defined in this test and checks that the AttributeError is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-153

**Requirement ID(s)**: REQ-FUN-101

**Verification method:** T

**Test goal:** The function AddElement() can access and properly changes the value of an existing (nested) sequence's element, attribute of a struct-like object or an XML ElementTree node, entry of a dictionary - provided that the path is properly defined and exists. If the provided path is properly defined but doesn't exist a new end node (leaf) is created with the expected value as well as all missing branches along the path, unless this operation requies creation of a new element of a sequence or sub-node of an XML ElementTree not in the next to the end position, or modification of an immutable branch.

**Expected result:** The functions does not raise any exception. The value of the corresponding existing element / entry / attribute is indeed changed, and it holds the passed as the second argument value. The new end nodes and missing branches are created, and the proper value is assigned to the new end node.

**Test steps:** Execute unit test methods *test_ProperSetElement* and *test_ProperAddsNewBranch* of test class **Test_AddElement** in module *Tests/ut001_structure_mapping.py*, which assigns proper values to the existing elements / entries / attributes, etc. and checks that an exception is not raised; also creates new branches and end nodes and checks that an exception is not raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-160

**Requirement ID(s)**: REQ-AWM-120, REQ-AWM-121

**Verification method:** T

**Test goal:** IOError or OSError is raised if a template file cannot be found or opened, ValueError is raised in case of a bad format JSON file or the mapping rules do not comply with the DSL specifications.

**Expected result:**

* IOError or OSError is raised if a template file cannot be found or openned (e.g. due access rights)
* ValueError is raised if the openned file does not contain a proper format JSON data
* Any of the defined mapping rules does not comply the specifications, i.e.:
  * Circular definition of a path substitution
  * Missing dependence in a definition of a path substitution
  * Missing definition of a path or value substitution in a mapping rule
  * Incremental addition or deletion rule for non-existing mapping definition sub-dictionary
  * Improper path definition in any path / value substitution or mapping rule
  * Misspelled special names 'PATHS' and 'INCLUDES'

**Test steps:** Execute unit test methods *test_RaisesUsualError* and *test_RaisesValueError* of the test class **Test_LoadDefinition** in the module *Tests/ut002_structure_mapping.py*, which attempts to load a non-existing file as well as a number of existing files with various faults from imporper JSON format to missing files to include to various errors in the mapping rules definitions.

**Test result:** PASS

---

**Test Identifier:** TEST-T-161

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-102, REQ-FUN-103.

**Verification method:** T

**Test goal:** Function LoadDefinition() properly parses a JSON format mapping rules definitions including path substitutions, recursive definitions (inclusion of sub-modules), etc.

**Expected result:** A template file (mapping definitions) is loaded and parsed without an exception raised. All required imports are performed, all substituions are resolved, the mapping rules are fully resolved and converted into cannonical form, i.e. - flattenned.

**Test steps:** Execute unit test method *test_LoadsProper* of the test class **Test_LoadDefinition** in the module *Tests/ut002_structure_mapping.py*, which loads a number of properly defined templates with the various amount of the mapping rules, including sub-modules import, path substitutions and incremental changes. The generated dictionaries of the mapping rules are compared to the manually constructed expected results.

**Test result:** PASS

---

**Test Identifier:** TEST-T-170

**Requirement ID(s)**: REQ-AWM-110, REQ-AWM-111

**Verification method:** T

**Test goal:** Function MapValues() raises TypeError when a path definition contains an element if of the wrong type, and ValueError - an element of a proper type but inacceptable value.

**Expected result:** TypeError is raised when a path definition contains an element if of the wrong type as defined in TEST-T-100, and ValueError - an element of a proper type but inacceptable value as defined in TEST-T-101.

**Test steps:** Execute unit test method *test_RaiseTypeValueErrorMappingObject* of test class **Test_MapValues** in module *Tests/ut002_structure_mapping.py*, which try to map the data between two objects using 'wrong' templates, and check that the expected exceptions are raised. 

**Test result:** PASS

---

**Test Identifier:** TEST-T-171

**Requirement ID(s)**: REQ-FUN-100, REQ-AWM-122

**Verification method:** T

**Test goal:** Function MapValues() raises AttributeError if a path in the source or target objects is missing unless the mapping occurs in a 'soft' mode.

**Expected result:**

The AttributeError is raised if:

* The required element / entry / attribute is not found in the source object and the corresponding *ignore source faults* flag is not set
* The required element / entry / attribute is not found in the target object, the corresponding *ignore target faults* flag is not set
* The required element / entry / attribute is not found in the target object, the corresponding *ignore target faults* flag is set, the creation of the missing elements in the target object is forced and there is immutable or incompatible object along the path
* There is an incompatible or immitable object in the path in the target object

The AttributeError is not raised if:

* The required element / entry / attribute is not found in the source object and the corresponding *ignore source faults* flag is set
* The required element / entry / attribute is not found in the target object, the corresponding *ignore target faults* flag is set and:
  * the creation of the missing elements in the target object is not forced
  * the creation of the missing elements in the target object is forced and there are no immutable or incompatible objects along the path

**Test steps:** Execute unit test methods *test_RaisesAttributeErrorSource*, *test_SkipsAttributeErrorSource*, *test_RaisesAttributeErrorTargetForced* and *test_SkipsAttributeErrorTargetForced* of test class **Test_MapValues** in module *Tests/ut002_structure_mapping.py*, which try to map the data between two objects using properly constructed templates, which do not match the structure of either a source or a target objects, and check that the expected exceptions are raised, unless the missing paths's errors are forced to be ignored. They also check that that the modification of an immutable path element in the target object results in the AttributeError regardless of the *ignore target faults* flag.

**Test result:** PASS

---

**Test Identifier:** TEST-T-172

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-103, REQ-FUN-104.

**Verification method:** T

**Test goal:** Function MapValues() properly maps the data from one object onto another object if a proper mapping rules set is provided.

**Expected result:**

The function performs the mapping properly in the default mode (both source and target are strict) in the case of the mapping rules properly reflecting the structure of both objects. The test cases must include complex / mixed types of the source and target objects, and the source path notation using strings, integers and 'choice' dictionaries:

* Class including nested sequence, dictionary and another struct-like class - > to the same type object
* Class including nested sequence, dictionary and another struct-like class - > to nested XML object
* Class including nested sequence, dictionary and another struct-like class - > to flat dictionary
* Flat sequence -> class including nested sequence, dictionary and another struct-like class
* Nested XML object -> class including nested sequence, dictionary and another struct-like class

**Test steps:** Execute unit test method *test_SetsProperly* of test class **Test_MapValues** in module *Tests/ut002_structure_mapping.py*, which creates a proper mapping rules set reflecting the internal structure of the objects descibed in the preparation steps and applies it for the data mapping between objects of the same or different types compatible in their structure with the mapping rules. The results of the data copying are verified to be as expected.

**Test result:** PASS

## Tests definition (Test)

**Test Identifier:** TEST-D-100

**Requirement ID(s)**: REQ-AWM-123

**Verification method:** D

**Test goal:** Functions LoadDefinition() and MapValues() log the raised exceptions into the console or / and a file using the passed logger object.

**Expected result:**

The functions properly log the intercepted and (re-) raised exceptions using the passed object (an instance of DualLogger class) before raising the exception themselves. THe original type and message of the re-raised exception is referenced. The log messages are clear and informative enough to trace the source of the problem.

The logging does not occur if a logger object is not passed explicitely as the optional (keyword) argument.

**Test steps:** Pass or do not pass an instance of DualLogger class as an optional keyword argument of the functions being tested within the ut002 test suite. When an instance of DualLogger class is passed, it is set to create the log files in *Tests/Output* folder - 'ut002_1.log' and 'ut002_2.log'.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                                 | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------------------------------------------- | :----------------------- |
| REQ-FUN-100        | TEST-T-102, TEST-T-112, TEST-T-161, TEST-T-171, TEST-T-172             | YES                      |
| REQ-FUN-101        | TEST-T-123, TEST-T-133, TEST-T-143, TEST-T-153                         | YES                      |
| REQ-FUN-102        | TEST-T-112, TEST-T161                                                  | YES                      |
| REQ-FUN-103        | TEST-T-161, TEST-T-172                                                 | YES                      |
| REQ-FUN-104        | TEST-T-172                                                             | YES                      |
| REQ-AWM-100        | TEST-T-100, TEST-T-111, TEST-T-120, TEST-T-130, TEST-T-140, TEST-T-150 | YES                      |
| REQ-AWM-101        | TEST-T-101, TEST-T-110, TEST-T-121, TEST-T-131, TEST-T-141, TEST-T-151 | YES                      |
| REQ-AWM-102        | TEST-T-122, TEST-T-132, TEST-T-142, TEST-T-152                         | YES                      |
| REQ-AWM-110        | TEST-T-111                                                             | YES                      |
| REQ-AWM-111        | TEST-T-110                                                             | YES                      |
| REQ-AWM-120        | TEST-T-160                                                             | YES                      |
| REQ-AWM-121        | TEST-T-160                                                             | YES                      |
| REQ-AWM-122        | TEST-T-171                                                             | YES                      |
| REQ-AWM-123        | TEST-D-100                                                             | YES                      |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
