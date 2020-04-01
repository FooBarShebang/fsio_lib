# TE002 Test Report on the Module fsio_lib.dynamic_import

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

Create a unit tests suite, which tests the implemented functions using Standard Library *os.path* for the import's checks. Make sure that the imported library is unloaded and the created references are de-referenced after each unit test method. In each unit test this module or only the function *basename*() from it will be imported. The function *os.path.basename*() will be used to define the base filename of the unit test suite module and compared with the same value stored in a global variable.

See unit test suite module *Tests/ut005_dynamic_import.py*.

## Tests definition (Test)

**Test Identifier:** TEST-T-200

**Requirement ID(s)**: REQ-FUN-200, REQ-FUN-220, REQ-FUN-221

**Verification method:** T

**Test goal:** Import of a module

**Expected result:** Upon import of the module *os.path* the function *basename*() it is accessible as *os.path.basename*() as well as *reference.basename*(), where *reference* is the name of the variable to which the result returned by the function's call is assigned. Both variants of the *basename*() function's call properly determine the base filename of the unit tests suit's module.

**Test steps:** Execute unit test method *test_import_module* of the test class **Test_import_module** from the module *Tests/ut005_dynamic_import.py*. It calls the function *fsio_lib.dynamic_import.import_module*() with the following arguments: 'os.path', dictGlobals = globals() - in order to import the module 'os.path' and make 'os.name' identifier visible in the scope of the test module, thus the test method itself. The returned value is assigned to the local variable *Temp*. The *os.path.basename*() function is called twice: as ```os.path.basename(__file__)``` and ```Temp.basename(__file__)```. Both returned values are compared to the actual module's base filename obtained earlier and stored in a global variable. The variable *Temp* is then de-refenced.

**Test result:** PASS

---

**Test Identifier:** TEST-T-201

**Requirement ID(s)**: REQ-FUN-201, REQ-FUN-220, REQ-FUN-221

**Verification method:** T

**Test goal:** Import of a module with aliasing

**Expected result:** Upon import of the module *os.path* the function *basename*() it is accessible as *alias.basename*() as well as *reference.basename*(), where *alias* is the requested alias for the imported module, and *reference* is the name of the variable to which the result returned by the function's call is assigned. Both variants of the *basename*() function's call properly determine the base filename of the unit tests suit's module.

**Test steps:** Execute unit test method *test_import_module_alias* of the test class **Test_import_module** from the module *Tests/ut005_dynamic_import.py*. It calls the function *fsio_lib.dynamic_import.import_module*() with the following arguments: 'os.path', 'Alias', dictGlobals = globals() - in order to import the module 'os.path' and make 'Alias' identifier visible in the scope of the test module, thus the test method itself. The returned value is assigned to the local variable *Temp*. The *os.path.basename*() function is called twice: as ```Alias.basename(__file__)``` and ```Temp.basename(__file__)```. Both returned values are compared to the actual module's base filename obtained earlier and stored in a global variable. The variable *Temp* is then de-refenced.

**Test result:** PASS

---

**Test Identifier:** TEST-T-210

**Requirement ID(s)**: REQ-FUN-210, REQ-FUN-220, REQ-FUN-221

**Verification method:** T

**Test goal:** Import of a function from a module

**Expected result:** Upon import of the function *basename*() from the module *os.path* it is accessible as *basename*() as well as *reference*(), where *reference* is the name of the variable to which the result returned by the function's call is assigned. Both variants of the *basename*() function's call properly determine the base filename of the unit tests suit's module.

**Test steps:** Execute unit test method *test_import_from_module* of the test class **Test_import_from_module** from the module *Tests/ut005_dynamic_import.py*. It calls the function *fsio_lib.dynamic_import.import_from_module*() with the following arguments: 'os.path', 'basename', dictGlobals = globals() - in order to import the function 'os.path.basename' and make 'basename' identifier visible in the scope of the test module, thus the test method itself. The returned value is assigned to the local variable *Temp*. The *os.path.basename*() function is called twice: as ```basename(__file__)``` and ```Temp(__file__)```. Both returned values are compared to the actual module's base filename obtained earlier and stored in a global variable. The variable *Temp* is then de-refenced.

**Test result:** PASS

---

**Test Identifier:** TEST-T-211

**Requirement ID(s)**: REQ-FUN-211, REQ-FUN-220, REQ-FUN-221

**Verification method:** T

**Test goal:** Import of a function from a module with aliasing

**Expected result:** Upon import of the function *basename*() from the module *os.path* it is accessible as *alias*() as well as *reference*(), where *alias* is the requested alias for the imported function, and *reference* is the name of the variable to which the result returned by the function's call is assigned. Both variants of the *basename*() function's call properly determine the base filename of the unit tests suit's module.

**Test steps:** Execute unit test method *test_import_from_module_alias* of the test class **Test_import_from_module** from the module *Tests/ut005_dynamic_import.py*. It calls the function *fsio_lib.dynamic_import.import_from_module*() with the following arguments: 'os.path', 'basename', 'Alias', dictGlobals = globals() - in order to import the function 'os.path.basename' and make 'Alias' identifier visible in the scope of the test module, thus the test method itself. The returned value is assigned to the local variable *Temp*. The *os.path.basename*() function is called twice: as ```Alias(__file__)``` and ```Temp(__file__)```. Both returned values are compared to the actual module's base filename obtained earlier and stored in a global variable. The variable *Temp* is then de-refenced.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                       | **Verified \[YES/NO\]**) |
| :----------------- | :------------------------------------------- | :----------------------- |
| REQ-FUN-200        | TEST-T-200                                   | YES                      |
| REQ-FUN-201        | TEST-T-201                                   | YES                      |
| REQ-FUN-210        | TEST-T-210                                   | YES                      |
| REQ-FUN-211        | TEST-T-211                                   | YES                      |
| REQ-FUN-220        | TEST-T-200, TEST-201, TEST-T-210, TEST-T-211 | YES                      |
| REQ-FUN-221        | TEST-T-200, TEST-201, TEST-T-210, TEST-T-211 | YES                      |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
