# RE004 Requirements for the Module locale_fsio

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

**Requirement ID:** REQ-FUN-400

**Title:** Support for various end-of-line conventions

**Description:** The module should provide functionality to save a text file using not the OS-specific end-of-line character(s), e.g. CR ('\r'), LF ('\n') or CRLF ('\r\n'), but the user specifed delimeter character(s). It should also provide functionality to load a text file and split it into lines using automatic detection of the end-of-line character or sequence - one of the following patterns:

* CR ('\r') followed by any charater except for LF ('\n') - CR line ending convention (classic Mac OS)
* LF ('\n') followed by any character and preceded by any character except for CR ('\r') - LF line ending convention (POSIX systems)
* CRLF ('\r\n') sequence - MS Windows convention

Any combination of these three variants is allowed in a single file.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-401

**Title:** Support for localized notation of the numerals

**Description:** The module should provide functionality to detect the locale-dependent notation used for the representation of a numeral in a string:

* Use of a dot ('.') as decimal separator (integer from fractional parts) with optional use of a comma (',') as a delimiter (thousends, millions, etc.) - e.g., as an *international* notation
* Use of a comma (',') as decimal separator (integer from fractional parts) with optional use of a dot ('.') as a delimiter (thousends, millions, etc.) - e.g., as an *Dutch* notation
* Use of the scientific notation as '...E/e +/- ...', e.g. '2.5E-3'; 'plus' sign in the exponent is optional

In case of ambiguity the *international* notation should be used as the default one. The implemented function or method should be able to extract an integer or floating point number from the string using the determined locale-dependent numerical notation.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-402

**Title:** Skipping first lines in the file

**Description:** The module should provide functionality to load a text file with automatic detection of the end-of-line character(s) as in REQ-FUN-400, which can vary line to line, split the content into lines and skip the requested number of the lines in the begining of the file. The input should be a single string; the output - a list of strings.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-403

**Title:** Support for whitespaces tabulation

**Description:** The module should provide functionality to split a line into columns allowing mixed usage of TAB characters ('\t') and usual whitespaces (' ') as columns delimeters using the following rules:

* An arbitrary amount (1 or more) of usual SPACE characters as an uninterrupted run are treated as a single TAB character - i.e. a columns delimiter
* Two consequitive columns delimeters designate that an empty column shoud be inserted between them
* If a line start with a columns delimiter an empty column should be inserted before it
* If a line ends with a columns delimiter an empty column should be inserted after it
* Use of TAB and SPACEs runs as delimiters in the same line is allowed

The input should be a single string; the output - a list of strings.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-404

**Title:** Loading tabulated data from the text files

**Description:** The module should provide a function or method to load tabulated data stored in a text file using automated end-of-line detection (REQ-FUN-400), locale-depenedent numeric notation (REQ-FUN-401), automated columns delimiters detection (REQ-FUN-403) and skipping the indicated number of the first lines in the file. The input should be a single string; the output - a list of lists of strings.

**Verification Method:** T
