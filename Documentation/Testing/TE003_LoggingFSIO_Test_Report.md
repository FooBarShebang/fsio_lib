# TE003 Test Report on Module fsio_lib.LoggingFSIO

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

Create a unit tests suite *Tests/ut006_LoggingFSIO.py*. Import class **fsio_lib.LoggingFSIO.LoggingFSIO**, which is intended to be used as a Singleton. Enable logging into the console at the ERROR level, logging into a file at DEBUG level. Set the overall severity logging level to DEBUG, and the logging file to *Tests/Output/ut006.log*. This class is to be used in all unit tests without instantiation.

Ensure that a test text file with a known md5 check-sum and modification date is created during the initialization of the unit tests, and it is deleted upon tests finalization. This check-sum and this modification date will be used for the verification of the 'copy / move / rename' functionality.

Write the unit test methods implementing the defined tests.

## Tests definition (Test)

**Test Identifier:** TEST-T-310

**Requirement ID(s)**: REQ-FUN-311, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Recursive creation of a folder

**Expected result:** The tested method - *makeDirs*() - creates a folder including all missing along the path 'parent' folders, but only if the passed path does not exist. Otherwise, it does not overwrite the content of the existing folders. In both cases it should return 0 as the success code.

**Test steps:** Execute unit test method *test_makeDirs*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to create a folder using a path with the last two elements (folders) not yet being present in the files system. Then it checks that the returned value of the call is 0 and that the path exists now. After that a file is created in the newly created end folder. The method being tested is called again with the same path argument. The returned value is checked (should be 0), and the file should still be present in that end folder. The created file, its (end) folder and the 'parent' folder are removed at the end of the test. The content of the log file *Tests/Output/ut006.log* is checked.

**Test result:** PASS

---

**Test Identifier:** TEST-T-311

**Requirement ID(s)**: REQ-FUN-310, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Exceptions treatment by makeDirs() method

**Expected result:** The tested method - *makeDirs*() - does not raise any exception. If not a string is passed as a path argument, the returned value is 1; if the folder cannot be created (permission denied) the returned value should be 3. In both cases an error message should be logged into the console and into the log file, whilst no changes should be applied to the file system.

**Test steps:** Execute unit test method *test_makeDirs_Errors*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to pass different non-string values including data types instead of types instances. The returned value is compared with 1. On a POSIX system (Linux, Mac OS X, etc.) an atempt to create a sub-folder of the root folder is taken (outside of the current user's home folder), and the returned code is compared with 3. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-320

**Requirement ID(s)**: REQ-FUN-311, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Copying file with optional renaming

**Expected result:** The tested method - *copyFile*() - can create a copy of a file with a new name in the same folder, which can be explicitely indicated or not provided at all; and it can copy a file from one folder into another folder with or without changing its base filename. In all cases it should return 0 as the success code.

**Test steps:** Execute unit test method *test_copyFile*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to create a copy of a file in the same folder with a new base filename and checks that: 1) the returned code is 0, 2) the context of the file is the same (by the md5 check-sum), and 3) the modification date-time stamps are equal up to 4 digits after the digital dot. Explicit indication of the target folder as well as its ommission are tried. The same checks are performed with copying into a different folder with the same or a different base filename. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-321

**Requirement ID(s)**: REQ-FUN-310, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Exceptions treatment by copyFile() method

**Expected result:** The tested method - *copyFile*() - does not raise any exception. If not a string is passed as a path or base filename argument, the returned value is 1; if the source file is not found the returned value is 2; if the folder or a file cannot be created (permission denied) the returned value should be 3. In both cases an error message should be logged into the console and into the log file, whilst no changes should be applied to the file system.

**Test steps:** Execute unit test method *test_copyFile_Errors*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to pass different non-string values including data types instead of types instances as a source path, target path and new base filename arguments. The returned value is compared with 1. On a POSIX system (Linux, Mac OS X, etc.) it atempts to copy an existing file into a not yet existing and into existing sub-folders of the root folder (outside of the current user's home folder), and the returned code is compared with 3. It also attempts to copy a non-existing file into an existing folder, and compares the returned value with 2. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-330

**Requirement ID(s)**: REQ-FUN-311, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Removal of a file

**Expected result:** The tested method - *deleteFile*() - removes an existing file and returns 0 as the success code.

**Test steps:** Execute unit test method *test_deleteFile*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It creates a file and then attempts to remove it using the method being tested. The returned value is compared with 0. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-331

**Requirement ID(s)**: REQ-FUN-310, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Exceptions treatment by deleteFile() method

**Expected result:** The tested method - *deleteFile*() - does not raise any exception. If not a string is passed as a path argument, the returned value is 1; if the file requested for removal cannot be found the returned value is 2; if the requested file cannot be deleted (permission denied) or the passed path refers to a folder the returned value should be 3. In all cases an error message should be logged into the console and into the log file, whilst no changes should be applied to the file system.

**Test steps:** Execute unit test method *test_deleteFile_Errors*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to pass different non-string values including data types instead of types instances. The returned value is compared with 1. A non-existing path is passed, and the returned value is compared with 2. Finally, a path to an existing folder is passed as the argument, and the returned value is compared with 3. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-340

**Requirement ID(s)**: REQ-FUN-311, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Moving a file

**Expected result:** The tested method - *moveFile*() - moves an existing file into another folder with or without changing its base filename and returns 0 as the success code.

**Test steps:** Execute unit test method *test_moveFile*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It creates a file, checks its modification date-time stamp and the md5 check-sum and then attempts to move it into another, not yet existing folder without changing its base filename using the method being tested. The returned value is compared with 0. The file system is checked that all the missing folders are created, the original file is removed and a file with the same base filename, md5 check-sum and modification date-time stamp is created in the new location (created end folder). The same procedure is repeated with changing the base filename; filename equality check is not performed. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-341

**Requirement ID(s)**: REQ-FUN-310, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Exceptions treatment by moveFile() method

**Expected result:** The tested method - *moveFile*() - does not raise any exception. If not a string is passed as a path or base filename argument, the returned value is 1; if the source file is not found the returned value is 2; if the target folder or a file cannot be created or source file cannot be removed (permission denied) the returned value should be 3. In both cases an error message should be logged into the console and into the log file. No changes should be applied to the file system except for the case when the source file cannot be deleted.

**Test steps:** Execute unit test method *test_moveFile_Errors*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to pass different non-string values including data types instead of types instances as a source path, target path and new base filename arguments. The returned value is compared with 1. On a POSIX system (Linux, Mac OS X, etc.) it atempts to move an existing file into a not yet existing and into existing sub-folders of the root folder (outside of the current user's home folder), and the returned code is compared with 3, and the orginal file remains. It also attempts to move a non-existing file into an existing folder, and compares the returned value with 2. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-350

**Requirement ID(s)**: REQ-FUN-311, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Renaming of a file

**Expected result:** The tested method - *renameFile*() - renames an existing file within a folder using the provided base filename and returns 0 as the success code.

**Test steps:** Execute unit test method *test_renameFile*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It creates a file, checks its modification date-time stamp and the md5 check-sum and then attempts to rename it using the method being tested. The returned value is compared with 0. The file with the new base filename is checked for presence in the same folder, its md5 check-sum and modification date-time stamps are compared with the original values. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

---

**Test Identifier:** TEST-T-351

**Requirement ID(s)**: REQ-FUN-310, REQ-AWM-310, REQ-AWM-311

**Verification method:** T

**Test goal:** Exceptions treatment by renameFile() method

**Expected result:** The tested method - *renameFile*() - does not raise any exception. If not a string is passed as a path argument or the new base filename argument, the returned value is 1; if the file requested for renaming cannot be found or the passed base filename argument is not a base name but includes a parent folder sub-path the returned value is 2; if the source file cannot be deleted or a new copy of the new file canot be created (permission denied) the returned value should be 3 (not tested). In all cases an error message should be logged into the console and into the log file. No changes should be applied to the file system except for the case when the source file cannot be deleted.

**Test steps:** Execute unit test method *test_renameFile_Errors*() of the test class **Test_LoggingFSIO** in the suite module *Tests/ut006_LoggingFSIO.py*. It attempts to pass different non-string values including data types instead of types instances as a source path or the new base filename. The returned value is compared with 1. A non-existing path is passed, and the returned value is compared with 2. Finally, a path (parent folder + base filename) is passed as the second argument, and the returned value is compared with 2. The content of the log file *Tests/Output/ut006.log* is checked as well as the file system itself.

**Test result:** PASS

## Tests definition (Demonstration)

**Test Identifier:** TEST-D-300

**Requirement ID(s)**: REQ-FUN-300, REQ-FUN-301, REQ-FUN-302

**Verification method:** D

**Test goal:** Verification of the enhanced logging functionality

**Expected result:** The implemented logger object can log into the console and / or a file (separately or simultaneously) using different and adjustable at any time severy levels. The output log file can be changed at any time.

**Test steps:** Examine the source code and make sure that the LoggingFSIO class uses DualLogger class defined in the same module to the logging. Perform the steps described in the 'Tests preparation' section: change the default logging severy and the default output file name. Run the unit tests and analyze the content of the created log file as well as the log messages in the console.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                     | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------------------------------- | :----------------------- |
| REQ-FUN-300        | TEST-D-300                                                 | YES                      |
| REQ-FUN-301        | TEST-D-300                                                 | YES                      |
| REQ-FUN-302        | TEST-D-300                                                 | YES                      |
| REQ-FUN-310        | TEST-T-311, TEST-T-321, TEST-T-331, TEST-T-341, TEST-T-351 | YES                      |
| REQ-FUN-311        | TEST-T-310, TEST-T-320, TEST-T-330, TEST-T-340, TEST-T-350 | YES                      |
| REQ-AWM-310        | TEST-T-310 to TEST-T-351 incl.                             | YES                      |
| REQ-AWM-311        | TEST-T-310 to TEST-T-351 incl.                             | YES                      |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
