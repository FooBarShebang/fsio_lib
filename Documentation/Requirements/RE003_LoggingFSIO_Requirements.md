# RE003 Requirements for the Module LoggingFSIO

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

**Requirement ID:** REQ-FUN-300

**Title:** Dual output logger object

**Description:** The module should provide a logger object capable of logging into the console, into a file, or into the console and a file simultaniously.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-301

**Title:** Logging severy level

**Description:** It should be possible to vary / adjust the severy level of the logging at any moment during the logger object's lifetime independently for the console and file output as well as to disable and (re-) enable the logging into a file or into the console.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-302

**Title:** Changing the output file

**Description:** It should be possible to change the output log file at any time. This operation should automaticaly enable file logging if it was disabled.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-310

**Title:** Exceptions free file operations

**Description:** The module should provide functionality wrapping the Standard Library functions *os.makedirs*(), *os.remove*() and *shutil.copy2*() and prevents exception raising in the following situations:

* Provided attribute is not a string, when a path is expected - TypeError / ValueError
* Specified path is not found - IOError / OSError
* Specified and found file cannot be open, or a file or folder cannot be created due to insufficient access rights - IOError / OSError

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-311

**Title:** Implemented functionality

**Description:** The following functionality should be implemented:

* Creation of a folder with all missing 'parent' folders along the path
* Copying of a file:
  * Into the same folder with a different base filename
  * Into another folder with the same base filename; missing path's folders should be created
  * Into another folder with a different base filename; missing path's folders should be created
* Removal of a file
* Renaming of a file - changing of the base filename, whilst the file remains in the same folder
* Moving of a file into another folder (copy + delete):
  * Preserving the base filename
  * Changing the base filename

The attributes of the files (creation, access, modification date-time stamp, etc.) should be preserved.

**Verification Method:** T

## Alarms, warnings, errors and user messages

**Requirement ID:** REQ-AWM-310

**Title:** Succes / failure of operation is returned

**Description:** The succes or failure of the requested operation should be returned as an unpacked tuple of an integer code and string explanation of the error code using the following scheme:

* 0 - OK
* 1 - Provided path argument is not a string (source or target)
* 2 - Path not found (for the source file only!)
* 3 - System IOError / OSError is raised - usuallay, due to access rights
* 4 - Other failure, not IOError / OSError

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-311

**Title:** Logging

**Description:** The implemented functions / methods should log the successful and failed operations using a logger object capable of logging into the console and / or a file, with the adjustable severity level of logging, ability to change the log file, etc. The raised and intercept exceptions should be logged at the ERROR level, successful operations - at the INFO level, and skipped - at the DEBUG level.

**Verification Method:** D
