# TE005 Test Report on Module fsio_lib.fs_maintenance

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

Create a unit tests suite *Tests/ut005_fs_maintenance.py*, which implements the unit test cases for the tests defined in this document.

## Tests definition (Test)

**Test Identifier:** TEST-T-500

**Requirement ID(s)**: REQ-FUN-500

**Verification method:** T

**Test goal:** Check that 'touch folder' functionality is implemented and performs as expected

**Expected result:** The function *TouchFolder*() creates a folder with all missing 'parent' folders when the passed path does not exist. The function does not modify or remove the files nor creates it new files or folders when the passed path to a folder already exists.

**Test steps:** Execute unit test method *test_TouchFolder*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*. It touches the sub-folder *Tests/a/b* using function *TouchFolder*() with the last two sub-folder not yet existing. Then it checks that the path is created. After that it creates a file within *Tests/a* and another file within *Tests/a/b*, and touches *Tests/a/b* again. Then it checks that the content of these folder has not changed. Finally, it removes the entire directory tree *Tests/a*.

**Test result:** PASS

---

**Test Identifier:** TEST-T-510

**Requirement ID(s)**: REQ-FUN-510

**Verification method:** T

**Test goal:** Function *SmartCopy*() performs according the requirements

**Expected result:** Function does not copy a file if there is a file with the same base filename and md5 check-sum in the target folder - i.e. a 'duplicate' file; function copies the original file preserving its base filename and attributes if there is no 'duplicate' in the target folder; function copies the original file changing the base filename but preserving the attributes if there is a name conflict but the files have different content (by md5 check-sum).

**Test steps:** Execute unit test method *test_TouchFolder*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. It creates two test sub-folders and a file in the 'source' test sub-folder, which is copied into the 'target' sub-folder.
2. The identity of the copy is verified.
3. An attempt is made to copy the original file again - and the 'target' sub-folder is checked, that no changes have occured.
4. The content of the original file in the 'source' sub-folder is modified, then an attempt to copy it into the 'target' sub-folder is taken.
5. The 'target' sub-folder is checked - a new file with md5 check-sum and modification date-time stamp being equal to the current values for the 'source' file, whereas its base filename should have the required suffix.
6. An attempt is made to copy the 'source' file again - and the 'target' sub-folder is checked, that no changes have occured.
7. Steps 4 to 6 are repeated 2 more times

**Test result:** PASS

---

**Test Identifier:** TEST-T-520

**Requirement ID(s)**: REQ-FUN-520

**Verification method:** T

**Test goal:** Function *RemoveEmptySubfolders*() performs according the requirements

**Expected result:** The function *RemoveEmptySubfolders*() deletes all 'dead branches' within a folder, i.e. all (nested) sub-folders, which do not contain any files and all their (nested) sub-sub-folders do not contain files either. The specified folder itself should remain, even if its empty itself.

**Test steps:** Execute unit test method *test_RemoveEmptyFolders*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. Create two files deeply (2 to 4 levels deep) nested within otherwise empty folders structure, such that these 'leaves' belong to two different branches
2. Remove one 'leaf', than call function *RemoveEmptySubfolders*() on the 'root' folder of the created struture
3. Check that only the branches along the path leading to the second 'leaf' remain
4. Remove the second 'leaf', than call function *RemoveEmptySubfolders*() on the 'root' folder
5. Check that the 'root' folder still exists, but it is empty
6. Call function *RemoveEmptySubfolders*() on the 'root' folder and check that it still exists and is empty

**Test result:** PASS

---

**Test Identifier:** TEST-T-530

**Requirement ID(s)**: REQ-FUN-530

**Verification method:** T

**Test goal:** Function *RemoveDuplicateFiles*() performs according the requirements

**Expected result:** The tested function locates 'identical' files - with the same base filename and md5 check-sums - and removes all instances but one using the following rules:

* The first found sub-path amongst the provided list of preferred locations
* If not provided or not found - the file with the latest date-time stamp
* If several copies with the latest date-time stamp exist - the shortest sub-path is chosen

**Test steps:** Execute unit test method *test_RemoveDuplicateFiles*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. Create a 'root' of the folders' structure with 3 sub-folders: 'a', 'b' and 'c'
2. Create a file in the 'root' folder and copy it preserving the base filename and attributes into each of the subfolders
3. Modify the copy in the sub-folder 'c' - write exactly the same content into the file as it was originally
4. Call the tested function *RemoveDuplicateFiles*() without the second argument; check that the only copy of the file remaining is in the 'c' sub-folder.
5. Copy this file into the 'root' and other sub-folders preserving the base filename and attributes
6. Call the tested function *RemoveDuplicateFiles*() without the second argument; check that the only copy remains in the 'root' folder
7. Copy that file into each of the subfolders preserving the base filename and attributes
8. Call the function *RemoveDuplicateFiles*() with the list ['a', 'b'] as the second argument; check that the only copy of the file remaining is in the 'a' sub-folder.
9. Copy this file into the 'root' and other sub-folders preserving the base filename and attributes
10. Call the function *RemoveDuplicateFiles*() with the list ['b', 'a'] as the second argument; check that the only copy of the file remaining is in the 'b' sub-folder.
11. Copy this file into the 'root' and other sub-folders preserving the base filename and attributes; remove that file from the 'b' subfolder
12. Call the function *RemoveDuplicateFiles*() with the list ['b', 'a'] as the second argument; check that the only copy of the file remaining is in the 'b' sub-folder.

**Test result:** PASS

---

**Test Identifier:** TEST-T-540

**Requirement ID(s)**: REQ-FUN-540

**Verification method:** T

**Test goal:** Function *RemoveFilesCopies*() performs according the requirements

**Expected result:** The function *RemoveFilesCopies*() finds and groups files within the specified folder with the same md5 check-sums, and deletes all such 'copies' except one in each group with the shortest (or smallest being sorted alphabetically) base filename. This process is recursively applied to all sub-folders, but each sub-folder is treated independently of the others.

**Test steps:** Execute unit test method *test_RemoveFilesCopies*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. Create a 'root' test folder and a sub-folder within
2. Create a number of files within the 'root' folder with the same content but different base filenames: 'a.txt', 'b.txt', 'aa.txt' - and also in the sub-folder of the root
3. Create a number of files within the 'root' folder with the same content (different from the previous point) but different base filenames: 'c.txt', 'd.txt', 'cc.txt'
4. Call function *RemoveFilesCopies*() to process the 'root' folder; check it content - only two files should remain in the 'root': 'a.txt' and 'c.txt', whereas only the file 'a.txt' should remain in the sub-folder

**Test result:** PASS

---

**Test Identifier:** TEST-T-550

**Requirement ID(s)**: REQ-FUN-550

**Verification method:** T

**Test goal:** Function *RenameSubFolders*() performs according the requirements

**Expected result:** The function recursively renames (sub-) sub-folders within a folder with the names matching case-insensitively any of the provided strings, or with their names being equal case-insensitively but being of a differnt case (lower, upper, etc.) to the 'new', requested name. If there are two or more sub-folders meeting these criteria in a folder - their content is merged. All remaining 'dead branches' are removed.

**Test steps:** Execute unit test method *test_RenameSubFolders*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. Create a 'root' test folder and the following sub-folders within: 'a/b', 'a/c/d', 'a/c/tEst' and 'a/e'
2. Create two copies of a file 'test.txt' (with the same content) within the subfolders 'a/b' and 'a/c/d' respectively.
3. Create another file in 'a/c/tEst' sub-folder with a differnt content.
4. Execute function *RenameSubFolders*() on the 'root' test folder.
5. Check that the sub-folder 'a/e' does not exist any longer
6. Check that the subfolder 'a/b' is renamed into 'a/test', whereas the file 'test.txt' is still present within with the same md5 check-sum and attributes
7. Check that the subfolder 'a/c' contains only a single sub-sub-folder 'test' with two files therein - 'test.txt' and 'test (copy).txt'. And each of these two files has the same combination of the md5 check-sum and modification date as the 'original' files in the sub-folders 'a/c/d' or 'a/c/tEst'.

**Test result:** PASS

---

**Test Identifier:** TEST-T-560

**Requirement ID(s)**: REQ-FUN-560

**Verification method:** T

**Test goal:** Function *CopyNonPresent*() performs according the requirements

**Expected result:** The function *CopyNonPresent*() copies such files from all sub-folders of the 'source' folder directly into the 'root' of the 'target' folder, for which there are no duplicates (same base filename and md5 check-sum) in any sub-folder of the 'target'. If the 'target' does contain a file with the same base filename but a different md5 check-sum than a file in the 'source', a suffix is added before the extension to the base filename during copy process, which is constructed from an underscore and a positive integer number. Attributes of the files being copied such as modification date, etc. are preserved.

**Test steps:** Execute unit test method *test_CopyNonPresent*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. Create a nested sub-folders structure.
2. Create a number of files in the end sub-folders and make sure that: a) there is a pair of files with the same base filename but different content and, b) there is a pair of files with the same md5 check-sum (content) but different base filenames
3. Copy the entire folders tree structure ('source') into another location ('target')
4. Remove one of the files with the same base filename from the 'source'
5. Remove one of the files with the same md5 check-sum from the 'target'
6. Make sure that the 'source' and 'target' both contain files with the same paths relative to the respective 'root' (and same md5 check-sum and base filename)
7. Execute the function *CopyNonPresent*() and pass the respective 'target' and 'source' as the arguments.
8. Check the 'target' that: a) for the same files with the same relative paths in 'target' and 'source' no changes are applied in the 'target', b) for files + path combinations present in the 'target' but not in the 'source' no changes are applied in the 'target', and c) files from any subfolder present in the 'source' but not in the 'target' are copied directly into the 'root' of the 'target' with or without the added suffix but preserving the attributes such as modification date.

**Test result:** PASS

---

**Test Identifier:** TEST-T-570

**Requirement ID(s)**: REQ-FUN-570

**Verification method:** T

**Test goal:** Function *CopyMerge*() performs according the requirements

**Expected result:** The module function *CopyMerge*() merges a content of one ('source') folder into another ('target') folder, i.e. after 'merging' the 'target' folder contains all branches (nested sub-folders structure) and all unique leaves (files with the unique for this sub-folder base filename and md5 check-sum) initially present in either of the 'source' or 'target' folders. The name conflict (same base filename but different md5 check-sums) whithin each sub-folder should be resolved by adding a suffix ' (copy)', ' (copy 1)', ' (copy 2)', etc. before the extension. Attributes of the files being copied such as modification date, etc. are preserved.

**Test steps:** Execute unit test method *test_CopyMerge*() of the test class **Test_fs_maintenance** in the module *Tests/ut007_fs_maintenance.py*.

1. Create a nested sub-folders structure.
2. Create a number of files in the end sub-folders and make sure that: a) there is a pair of files with the same base filename but different content and, b) there is a pair of files with the same md5 check-sum (content) but different base filenames
3. Copy the entire folders tree structure ('source') into another location ('target')
4. Remove some leaves or / and branches in the 'source' and some other branches and / or leaves in the 'target'
5. Remove one of the files in the 'target' such that its base filename is not modified but the content is different, and there is a file with the same relative path and base filename in the 'source'
6. Make sure that the 'source' and 'target' both contain files with the same paths relative to the respective 'root' (and same md5 check-sum and base filename)
7. Execute the function *CopyMerge*() and pass the respective 'source' and 'target' as the arguments.
8. Check the 'target' that its entire files and folders tree structure is the same as it was intially created for the 'source' except one sub-folder, where the content of a file was modified. In this folder the original modified in 'target' file should remained unchained, whilst the file with the same base filename from 'source' should be copied with a suffix ' (copy)' being added but preserving the attributes. All other files - present in the 'target' before merging and copied from the 'source' must retain their base filenames and attributes such as modification date.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-500        | TEST-T-500             | YES                      |
| REQ-FUN-510        | TEST-T-510             | YES                      |
| REQ-FUN-520        | TEST-T-520             | YES                      |
| REQ-FUN-530        | TEST-T-530             | YES                      |
| REQ-FUN-540        | TEST-T-540             | YES                      |
| REQ-FUN-550        | TEST-T-550             | YES                      |
| REQ-FUN-560        | TEST-T-560             | YES                      |
| REQ-FUN-570        | TEST-T-570             | YES                      |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
