# RE005 Requirements for the Module fs_maintenance

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Description / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requirement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-500

**Title:** 'Touch folder' functionality

**Description:** The module should provide functionality to check if a specific folder exists, and to create such folder with all missing 'parent' folders in the path if it is not found. If the folder already exists no changes should be applied to the file system.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-510

**Title:** 'Smart copy' functionality

**Description:** The module should providue a funciton or a method to copy a file from one folder into anoter using the following rules:

* if a file with the same base filename and md5 check sum exists in the target folder - no action is taken
* if a file with the same base filename does not exist in the target folder, it is simply copied preserving the base filename and attributes, such as modification time, etc.
* if there is a file with the same base filename but a different md5 check-sum, the file is copied with a suffix ' (copy)', ' (copy 1)', ' (copy 2)', etc., added before the file's extension, whilst the file's attributes such as modification time are preserved

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-520

**Title:** 'Remove dead branches' functionality

**Description:** The module should provide a function or a method to delete all 'dead branches' within a folder, i.e. all (nested) sub-folders, which do not contain any files and all their (nested) sub-sub-folders do not contain files either. The specified folder itself should remain, even if its empty itself.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-530

**Title:** Removal of duplicated files along the folder's tree

**Description:** The module should provide a function or a method to locate 'identical' files - with the same base filename and md5 check-sums - and to remove all instances but one using the following rules:

* The first found sub-path amongst the provided list of preferred locations
* If not provided or not found - the file with the latest date-time stamp
* If several copies with the latest date-time stamp exist - the shortest sub-path is chosen

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-540

**Title:** Removal of the copies of a file within a single folder

**Description:** The module should provide a function or a method to remove all unwanted copies of the same file - different base filenames but the same md5 check-sum - from a folder. The only copy for each md5 check-sum value is with the shortest or smallest (sorted alphabetically) base filename. This process is recursively applied to all sub-folders, but each sub-folder is treated independently of the others.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-550

**Title:** Renaming and merging of sub-folders

**Description:** The module should provide a function or a method to recursively rename (sub-) sub-folders within a folder with the names matching case-insensitively any of the provided strings, or with their names being equal case-insensitively but being of a differnt case (lower, upper, etc.) to the 'new', requested name. If there are two or more sub-folders meeting these criteria in a folder - their content is merged. The 'dead branches' created in the process as well as previously existed should be removed.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-560

**Title:** Copying of files from one folder, which are not found in the second folder

**Description:** The module should provide a function of a method to compare the content of two folders including their (nested) sub-folders and to copy such files from all sub-folders of the 'source' folder directly into the 'root' of the 'target' folder, for which there are no duplicates (same base filename and md5 check-sum) in any sub-folder of the 'target'. If the 'target' does contain a file with the same base filename but a different md5 check-sum than a file in the 'source', a suffix is added before the extension to the base filename during copy process, which is constructed from an underscore and a positive integer number. Attributes of the files being copied such as modification date, etc. should be preserved.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-570

**Title:** Merging of folders

**Description:** The module should provide a function of a method to merge a content of one ('source') folder into another ('target') folder, i.e. after 'merging' the 'target' folder should contain all branches (nested sub-folders structure) and all unique leaves (files with the unique for this sub-folder base filename and md5 check-sum) initially present in either of the 'source' or 'target' folders. The name conflict (same base filename but different md5 check-sums) whithin each sub-folder should be resolved by adding a suffix ' (copy)', ' (copy 1)', ' (copy 2)', etc. before the extension. Attributes of the files being copied such as modification date, etc. should be preserved.

**Verification Method:** T
