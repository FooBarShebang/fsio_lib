# TE004 Test Report on Module fsio_lib.locale_fsio

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

Create a unit tests suite *Tests/ut003_locale_fsio.py*, which implements the unit test cases for the tests defined in this document. Implement helper functions to generate a random ASCII string and a random sequence of random ASCII strings. Also prepare a number of specific format / combination of the conventions tabulated data text files as described in the TEST-T-404.

## Tests definition (Test)

**Test Identifier:** TEST-T-400

**Requirement ID(s)**: REQ-FUN-400

**Verification method:** T

**Test goal:** Forced end-of-line convention during files saving

**Expected result:** The function SaveForcedNewLine() saves the passed sequence of strings into a file and inserts the requested character(s) between the elements. When the end-of-line delimiter is not passed, the default CRLF sequence is used.

**Test steps:** Execute the unit test methods *test_LF*(), *test_CR*(), *test_CRLF*() and *test_DEF*() of the test class **Test_LineEndings** in the module *Tests/ut003_locale_fsio.py*, which implement the following test steps:

1. Generate a random amount of strings of a random length.
2. Generate the control string by joining them all using the expected line ending sequence in between and at the end of the control string.
3. Save the generated sequence of strings into a file using the function to be tested and pass exactly the same line ending sequence.
4. Open the generated file in the **binary** mode and read its entire content into another large string.
5. Compare the control string with the second string.
6. Repeat steps 2 to 5 with other types of the forced line endings.
7. Repeat step 2 using 'CRLF' ending and step 3 without specifying the forced line ending style (default option), then repeat steps 4 and 5.

**Test result:** PASS

---

**Test Identifier:** TEST-T-401

**Requirement ID(s)**: REQ-FUN-400, REQ-FUN-402

**Verification method:** T

**Test goal:** Automatic detection of the end-of-line charater(s) and splitting into lines

**Expected result:** The function LoadLines() can load the entire content of a text file and split it into lines allowing mixed usage of the CR, LF and CRLF end-of-line conventions in the same file; it can also skip (do not return) the required number of the lines in the beginning of the file.

**Test steps:**  Execute the unit test methods *test_LoadLines*() and *test_LoadSkipLines*() of the test class **Test_LoadLines** in the module *Tests/ut003_locale_fsio.py*, which implement the following test steps:

1. Generate a random amount of strings of a random length.
2. Write these random strings into a file using the function SaveForcedNewLine() and the default (not specified) end-of-line convention.
3. Read the content of the file using the function LoadLines() and compare the returned list of string with the orginal (generated) list of string.
4. Repeat steps 2 and 3 using the forced CR, LF and CRLF end-of-line conventions.
5. Repeat steps 2 to 4 asking function LoadLines() to skip various number of the lines and comparing with a slice of the original (generated) list of string without the same number of the first elements.

**Test result:** PASS

---

**Test Identifier:** TEST-T-402

**Requirement ID(s)**: REQ-FUN-401

**Verification method:** T

**Test goal:** Automatic detection of the locale-dependent numeric notation for the representation of the numbers in a string

**Expected result:**

The function DetectNotation() automatically detects the INT / NL number format based on a provided sequence of strings, with some of them being quoted numbers with or without decimal delimiters and / or separators. If at least one quoted number is unambiguously of INT or NL notation - this choice is to be returned. If the format cannot be determined unambiguously, the default format is INT.

The function ConvertFromString(), which uses DetectNotation() must properly convert the quoted numbers (in strings) stored in either INT or NL notation with possible decimal delimiters, if the format is known *a priori* and passed into the function.

**Test steps:** Execute the unit test method *test_Notation*() of the test class **Test_DetectNotation** and *test_Conversion*() of the test class **Test_ConvertFromString** in the module *Tests/ut003_locale_fsio.py*, which perform the following checks:

* Pass a number of lists of stings into function DetectNotation() and compare the returned value with the expected 0 or 1 value; each passed list of string includes non-numeric strings and, at least, 2 numeric strings all being constructed using the same convention on the use of comma and dot for the delimiter and separator, with optional use of the delimiters and exponentional notation.
* Pass similarly constructed lists of strings into function ConvertFromString() and compare the returned lists with the expected lists: the numeric strings should be detected and converted into integer or floating point numbers using the same convention for the entire list, although different lists can use different conventions.

**Test result:** PASS

---

**Test Identifier:** TEST-T-403

**Requirement ID(s)**: REQ-FUN-403

**Verification method:** T

**Test goal:** Splitting into columns allowing mixed TAB and SPACE usage

**Expected result:** The function SplitLine() must properly split strings into columns (elements) by TABs or an arbitrary amount of usual spaces. Continuous run of usual spaces is treated as a single TAB character regardless of the length of the run. Two TABs or TAB followed by spaces or spaces followed by a TAB are treated as an empty column between them. The leading TAB or space are treated as an empty column preceding them, tailing TAB or space - as an empty column following them.

**Test steps:** Execute the unit test method *test_SplitLine*() of the test class **Test_SplitLine** in the module *Tests/ut003_locale_fsio.py*, which passes a number of strings into the function SplitLine() one at the time and compares the returned list of strings with the expected one. The input strings contain various amount of TAB and SPACE characters intermixed with each other and non-whitespace ASCII characters; TAB and SPACE characters can be also the first and the last characters in a string.

**Test result:** PASS

---

**Test Identifier:** TEST-T-404

**Requirement ID(s)**: REQ-FUN-400, REQ-FUN-401, REQ-FUN-402, REQ-FUN-403, REQ-FUN-404

**Verification method:** T

**Test goal:** Splitting into columns allowing mixed TAB and SPACE usage

**Expected result:**

The function LoadTable() properly reads data from a text file without *a priori* knowledge of the used conventions on the line ending, TABs or usual spaces for column separation as well as of the number notation (INT / NL with or without decimal delimiters), i.e. it properly integrates all functionality implemented in the module being tested.

Tested formats:

* FBR file - Single column. CRLF line end. Mixed data - str + int + float in Dutch scientific notation.
* LMP file - Two columns, spaces. CRLF line end. Floats in international notation.
* LIN file - Three columns, tabs and spaces (variable length). LF line end. Mixed data: ints, floats in international notation and strings.
* Proprietary format TXT file - Three columns, tab-spaces (variable length). CRLF line end. Mixed data: ints and floats in Dutch notation with delimiters.

**Test steps:** Execute the unit test methods *test_LoadFBR*, *test_LoadLMP*, *test_LoadLIN* and *test_LoadSP_TXT* of the test class **Test_LoadTable** in the module *Tests/ut003_locale_fsio.py*, which read the content of the test files using the function LoadTable() and compare the values of the specific cells (specific raw and column position) with the expected values. **N.B.** these check positions and check values are hard-coded based on the actual content of the test files!

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                     | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------------------------------- | :----------------------- |
| REQ-FUN-400        | TEST-T-400, TEST-T-401, TEST-T-404                         | YES                      |
| REQ-FUN-401        | TEST-T-402, TEST-T-404                                     | YES                      |
| REQ-FUN-402        | TEST-T-401, TEST-T-404                                     | YES                      |
| REQ-FUN-403        | TEST-T-403, TEST-T-404                                     | YES                      |
| REQ-FUN-404        | TEST-T-400, TEST-T-401, TEST-T-402, TEST-T-403, TEST-T-404 | YES                      |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
