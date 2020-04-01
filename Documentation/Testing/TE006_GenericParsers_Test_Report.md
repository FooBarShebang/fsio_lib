# TE006 Test Report on Module fsio_lib.GenericParsers

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

Create a unit tests suite *Tests/ut004_generic_parsers.py*, which implements the unit test cases for the tests defined in this document.

Implement test templates for the JSON and XML parsing - *Templates/JSON/json_test.json* and *Templates/XML/xml_test.json* to be used in the unit testing. Reference them in the common index file *Templates/index.json* and in the specific indexes *Templates/json_seaarch_index.json* and *Templates/xml_search_index.json*. Note that the above mentioned parsing templates should properly match the structure of the JSON and XML objects stored in the files *Tests/Input/dummy.json* and *Tests/Input/dummy.xml* (created and used in TE001) respectively as the source as well as the structure of the test target object *HelperClass* defined in the module **fsio_lib.Tests.ut004_helper_class**. These template should explicitely target that class and be construted according the DSL definitions given in the DE001 and DE002 documents. 'Bad', wrong format test files used in the TE001 should be re-used to test the raising of exceptions.

Ensure that the log files created by the parsers can be located and identified, e.g. place them into the folder *Tests/Output* and use unique filenames for each of the test classes.

## Tests definition (Test)

**Test Identifier:** TEST-T-600

**Requirement ID(s)**: REQ-AWM-600

**Verification method:** T

**Test goal:** ValueError is raised if the parsing template is not provided and cannot be guessed

**Expected result:** Methods parseFile() and parseManyFiles() of the parser classes raise ValueError if no template is provided (explicit or default None value) and it cannot be guessed by the file content.

**Test steps:** Execute test unit method *test_NoDataNoTemplate*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which inherit this method in the module *Tests/ut004_generic_parsers.py*. This method calls the methods *parseFile*() and *parseManyFiles*() of the corresponding parsers, into which it passes a test file, which structure cannot be used to define a parsing template, and it does not passes a parsing template either. The unit test method checks that ValueError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-601

**Requirement ID(s)**: REQ-AWM-601

**Verification method:** T

**Test goal:** TypeError is raised if not a string value is passed as a path argument

**Expected result:** Methods parseFile() and parseManyFiles() of the parser classes raise TypeError if any data type but a string value is passed as the path argument, including the folder's path and base filenames within.

**Test steps:** Execute test unit method *test_RaisesTypeErrorFiles*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which inherit this method, as well as of the classes **Test_parseFile** and **Test_parseManyFiles** defined in the module *Tests/ut004_generic_parsers.py*. This methods call the methods *parseFile*() and *parseManyFiles*() of the corresponding parsers, into which it passes different values not being strings in as the path to a file or folder respectively, or a base filename of, at least, one file within that folder. The unit test method checks that TypeError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-602

**Requirement ID(s)**: REQ-AWM-602

**Verification method:** T

**Test goal:** ValueError is raised in the case of a non-existing path to a data file.

**Expected result:** Method parseFile() of the parser classes raises ValueError when the received path argument does not refer to an existing file. Method parseManyFiles() of the parser classes receives the folder's path argument, which does not lead to an existing folder, or any of the passed base filenames is not found in that folder.

**Test steps:** Execute test unit method *test_RaisesValueErrorNotFile*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which inherit this method, as well as of the classes **Test_parseFile** and **Test_parseManyFiles** defined in the module *Tests/ut004_generic_parsers.py*. This methods call the methods *parseFile*() and *parseManyFiles*() of the corresponding parsers, into which it passes different values of string types, which are not proper paths to an existing file or folder. Specifically for the *parseManyFiles*() a combination of a proper path to a folder with a non-existing base filename is checked as well. The unit test method checks that ValueError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-603

**Requirement ID(s)**: REQ-AWM-603

**Verification method:** T

**Test goal:** TypeError is raised if neither **None** value nor a dictionary is passed a parsing template

**Expected result:** Methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() raise **TypeError** if the template argument is not a template (but not None), i.e. any other data type but a mapping type.

**Test steps:** Execute test unit method *test_RaisesTypeErrorTemplateNotDict*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which inherit this method in the module *Tests/ut004_generic_parsers.py*. This method calls the methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() of the corresponding parsers, into which it passes different values of different data types, which are not a dictionary or other mapping type. The unit test method checks that TypeError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-604

**Requirement ID(s)**: REQ-AWM-604

**Verification method:** T

**Test goal:** ValueError is raised if a dictionary of a wrong format is passed as a parsing template

**Expected result:** Methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() raise **ValueError** if the template argument is a dictionary, but it does not have the key 'DataMapping', or the value bound to this key is not a dictionary.

**Test steps:** Execute test unit method *test_RaisesValueErrorTemplateDataMapping*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which inherit this method in the module *Tests/ut004_generic_parsers.py*. This method calls the methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() of the corresponding parsers, into which it passes different dictionaries as the parsing template argument, which either do not have 'DataMapping' entry, or with a non-dictionary value bound to that key. The unit test method checks that ValueError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-605

**Requirement ID(s)**: REQ-AWM-605

**Verification method:** T

**Test goal:** TypeError or ValueError is raised in the case of a non-conforming mapping template

**Expected result:** The methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() raise **TypeError** or **ValueError** if the mapping dictionary is not of the proper format (DE001 DSL specifications) regardless of the *bStrictSource* and *bStrictTarget* flags.

**Test steps:** Execute test unit method *test_RaisesValueErrorTemplateDataMapping*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which inherit this method in the module *Tests/ut004_generic_parsers.py*. This method calls the methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() of the corresponding parsers, into which it passes different improperly formed mapping rules templates either directly (in the case of*parseSingleObject*() method) or by defining them using the parsing templates. The unit test method checks that ValueError or TypeError exception is raised.

**Test result:** PASS

---

**Test Identifier:** TEST-T-606

**Requirement ID(s)**: REQ-AWM-606, REQ-FUN-604

**Verification method:** T

**Test goal:** Strict and relaxed source mapping mode implementation

**Expected result:** The methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() raise **AttributeError** if the source object does not have the required element and the flag *bStrictSource* is **True**. If the flag *bStrictSource* is **False**, the exception is not raised, but the corresponding element of the target object is not changed and remains at its initial value.

**Test steps:** Execute test unit method *test_RaisesAttributeErrorSource*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which re-define this method in the module *Tests/ut004_generic_parsers.py*. It passes different properly defined mapping templates, which do not match the internal structure of the source data object, i.e. pointing to a non-existing element (path) of the source object. This test checks that **AttributeError** is raised with the *bStrictSource* flag being **True**; otherwise the exception is not raised and the value of the corresponding element of the target object is not changed.

**Test result:** PASS

---

**Test Identifier:** TEST-T-607

**Requirement ID(s)**: REQ-AWM-606, REQ-FUN-604

**Verification method:** T

**Test goal:** Strict and relaxed target mapping mode implementation

**Expected result:** The methods *parseSingleObject*(), *parseFile*() and *parseManyFiles*() raise **AttributeError** if the source object does not have the required element and the flag *bStrictTarget* is **True**. If the flag *bStrictTarget* is **False** and *bForceTarget* is **False** - the exception is not raised, but the missing element is not created; if the *bForceTarget* is **True** - the missing element is created and the proper value is assigned to it. This test does not cover the case when *bStrictTarget* flag is at **None** value (see REQ-FUN-604).

**Test steps:** Execute test unit method *test_RaisesAttributeErrorTarget*() of the test class **Test_GenericParser** and of classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser**, which re-define this method in the module *Tests/ut004_generic_parsers.py*. It passes different properly defined mapping templates, which do not match the internal structure of the target data object, i.e. pointing to a non-existing element (path) of the target object. This test checks that **AttributeError** is raised with the *bStrictTarget* flag being **True**; otherwise the exception is not raised and a) the corresponding element of the target object is created and the respective value from the source is copied if *bForceTarget* flag is **True** or b) the corresponding element of the target object is not created if *bForceTarget* flag is **False**.

**Test result:** PASS

---

**Test Identifier:** TEST-T-608

**Requirement ID(s)**: REQ-FUN-600

**Verification method:** T

**Test goal:** Files parsing with explicitely provided parsing template and the target data type

**Expected result:** The methods *parseFile*() and *parseManyFiles*() of the parser objects create the expected number of the target objects (defined by passed argument) packed into a list and fill them properly when both the target class (type) and the template are provided explicitly, and the mapping matches the structure of the both source and target objects.

**Test steps:** Execute test unit method *test_CopiesProperlyWithTargetAndTemplate*() of the test classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser** defined in the module *Tests/ut004_generic_parsers.py*. It calls the methods *parseFile*() and *parseManyFiles*() of the corresponding parser class and passes a path to a proper data source file / folder containing the proper data source files, a parsing template matching the structure of the source file(s) and a data type (class) with the internal structure compatible with the mapping rules defined by the template. The test method checks that no exceptions are raised, sequence of instances of the specified data type is returned and the data mapping is performed as expected (only the first element in the sequence is checked).

**Test result:** PASS

---

**Test Identifier:** TEST-T-609

**Requirement ID(s)**: REQ-FUN-600, REQ-FUN-602

**Verification method:** T

**Test goal:** Files parsing with explicitely provided parsing template without the target data type being provided

**Expected result:** The methods *parseFile*() and *parseManyFiles*() of the parser objects create the expected number of the target objects packed into a list and fill them properly when the template are provided explicitly and the target data type is not provided but defined by the template, and the mapping matches the structure of the both source and target objects.

**Test steps:** Execute test unit method *test_CopiesProperlyWithTemplateOnly*() of the test classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser** defined in the module *Tests/ut004_generic_parsers.py*. It calls the methods *parseFile*() and *parseManyFiles*() of the corresponding parser class and passes a path to a proper data source file / folder containing the proper data source files and a parsing template matching the structure of the source file(s). The test method checks that no exceptions are raised, sequence of instances of the propert data type is returned as defined by the template and the data mapping is performed as expected (only the first element in the sequence is checked).

**Test result:** PASS

---

**Test Identifier:** TEST-T-60A

**Requirement ID(s)**: REQ-FUN-604

**Verification method:** T

**Test goal:** Proper selection of the strict or relaxed target mapping mode when not set explicitely

**Expected result:** The default (absent) or explicit **None** value of the *bStrictTarget* flag should be treated as **True** if the explicit target class is not given but can be derived from the template, or it is the same as the suggested by the template. If the explicitly given target class is not the same as suggested by the template, the **None** value of the *bStrictTarget* flag should be treated as **False**. The explicitly specified **True** or **False** values of this flag should not be modified in any of the cases.

**Test steps:** Execute test unit method *test_StrictTargetModeTargetByTemplate*() of the test classes **Test_TSV_Parser**, **Test_JSON_Parser** and **Test_XML_Parser** defined in the module *Tests/ut004_generic_parsers.py*. This unit test calls the methods *parseFile*() and *parseManyFiles*() of the corresponding parser class passing a proper parsing template matching the structure of the provided source data file(s) and different combinations of the **True**, **False** and **None** values of the *bStrictTarget* flag with the value of the target data type argument: as **None** (not provided), same as suggested by the template and a different from the template suggested data type. The unit test method checks that the strict / relaxed mode is selected properly and the **AttirbuteError** is raised only in the strict mode and when the target object misses, at least, one of the expected paths / elements.

**Test result:** PASS

---

**Test Identifier:** TEST-T-60B

**Requirement ID(s)**: REQ-FUN-603

**Verification method:** T

**Test goal:** Proper automatic selection of the parsing template by the file's content

**Expected result:** The methods **parseFile**() and **parseManyFiles**() return the target objects of the expected types (class instances) properly filled with the data from the source file(s) and packed into lists - when neither the template nor the target class are explicitly provided, but the required template can be selected on the basis of the source file content using the search indexes.

**Test steps:** Execute test unit method *test_DeterminesTargetAndTemplateByFile*() of the test classes **Test_JSON_Parser** and **Test_XML_Parser** defined in the module *Tests/ut004_generic_parsers.py*. This unit test calls the methods *parseFile*() and *parseManyFiles*() of the corresponding parser class passing a proper parsing template matching the structure of the provided source data file(s) and different combinations of the **True**, **False** and **None** values of the *bStrictTarget* flag with the value of the target data type argument: as **None** (not provided), same as suggested by the template and a different from the template suggested data type. The unit test method checks that the strict / relaxed mode is selected properly and the **AttirbuteError** is raised only in the strict mode and when the target object misses, at least, one of the expected paths / elements.

**Test result:** PASS

---

**Test Identifier:** TEST-T-610

**Requirement ID(s)**: REQ-AWM-610

**Verification method:** T

**Test goal:** Improper format of input JSON data file results in ValueError exception

**Expected result:** The methods *parseFile*() and *parseManyFiles*() of the class **JSON_Parser** raise **ValueError** if the source data file is not a proper format JSON, excluding the 'special' cases of '{} {}' or '{}, {}' instead of '[{}, {}]'.

**Test steps:** Execute test unit method *test_RaisesExceptionBadFile*() of the test class **Test_JSON_Parser** defined in the module *Tests/ut004_generic_parsers.py*, which checks that the methods *parseFile*() and *parseManyFiles*() raise **ValueError** when they attempt to parse a text file, which is not a proper format JSON, but they can properly parse a file and do not raise **ValueError** exception when it contains a number of JSON dictionaries simply dumpt into a file with or without commas between but not packed into a list.

**Test result:** PASS

---

**Test Identifier:** TEST-T-620

**Requirement ID(s)**: REQ-AWM-620

**Verification method:** T

**Test goal:** Improper format of input XML data file results in specific exception

**Expected result:** The methods *parseFile*() and *parseManyFiles*() of the class  **XML_Parser** raise **xml.etree.ElementTree.ParserError** if the source data file is not a proper format XML.

**Test steps:** Execute test unit method *test_RaisesExceptionBadFile*() of the test class **Test_XML_Parser** defined in the module *Tests/ut004_generic_parsers.py*, which checks that the methods *parseFile*() and *parseManyFiles*() raise the expected exception when they attempt to parse a text file, which is not a proper format XML.

**Test result:** PASS

---

**Test Identifier:** TEST-T-60C

**Requirement ID(s)**: REQ-FUN-601, REQ-FUN-602, REQ-FUN-603

**Verification method:** T

**Test goal:** Proper automatic selection of the parser class, template and target type

**Expected result:** The (aggregation) functions *parseFile*() and *parseManyFiles*() defined in the module *fsio_lib.GenericParsers* properly determine the parser class based on the file extension and internal format, the suitable parsing template using the search indexes and analyzing the content of the files, whereas the required target data type is defined by the parsing template.

**Test steps:** Execute the unit test method *test_ParsesAutomatically* of the test classes **Test_parseFile** and **Test_parseManyFiles** in the module *Tests/ut004_generic_parsers.py*, which calls the functions *parseFile*() and *parseManyFiles*() respectively and passes only the path to a file / path to a folder and the file's base filename as a single element of a list. The arguments for the template and target data types are not provided. The test files are *Templates/JSON/json_test.json* and *Templates/XML/xml_test.json*, for which the records in the search indexes are created. The unit test method checks that the files are properly parsed and the data is mapped onto instances of the expected data type / class, whilst no exceptions are raised.

**Test result:** PASS

## Tests definition (Demonstration)

**Test Identifier:** TEST-D-600

**Requirement ID(s)**: REQ-FUN-605

**Verification method:** D

**Test goal:** The implemented parsers can parse a file, a group of files in a single folder and map one or more data objects in a single call

**Expected result:** All implemented parser classes have methods to map a single source data object into a instance of the target data type and to parse one file or a group of files and return a sequence of instances of target data type. If a folder contains data files of different internal structure or file format a sequence of instances of different data types can be returned.

**Test steps:** This test is an integration of the results of the tests TEST-608. TEST-T-609, TEST-T-60A, TEST-T-60B

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**             | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------- | :----------------------- |
| REQ-FUN-600        | TEST-T-608, TEST-T-609             | YES                      |
| REQ-FUN-601        | TEST-T-60C                         | YES                      |
| REQ-FUN-602        | TEST-T-609, TEST-T-60C             | YES                      |
| REQ-FUN-603        | TEST-T-60B, TEST-T-60C             | YES                      |
| REQ-FUN-604        | TEST-T-606, TEST-T-607, TEST-T-60A | YES                      |
| REQ-FUN-605        | TEST-D-600                         | YES                      |
| REQ-AWM-600        | TEST-T-600                         | YES                      |
| REQ-AWM-601        | TEST-T-601                         | YES                      |
| REQ-AWM-602        | TEST-T-602                         | YES                      |
| REQ-AWM-603        | TEST-T-603                         | YES                      |
| REQ-AWM-604        | TEST-T-604                         | YES                      |
| REQ-AWM-605        | TEST-T-605                         | YES                      |
| REQ-AWM-606        | TEST-T-606                         | YES                      |
| REQ-AWM-607        | TEST-T-607                         | YES                      |
| REQ-AWM-610        | TEST-T-610                         | YES                      |
| REQ-AWM-620        | TEST-T-620                         | YES                      |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |