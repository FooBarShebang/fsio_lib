# RE006 Requirements for the Module GenericParsers

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

**Requirement ID:** REQ-FUN-600

**Title:** Parsing of the files and data mapping

**Description:** The module should provide a number of format-specific parsers, which can extract data from specific structured data files (tabulated, tag based as XML, or direct representation of a structure as JSON) and map it onto another oject (sequence, dictionary, C-sturct like object, etc.) using a specific data mapping template, as defined by DSL specification in DE001 document. The data type of the 'target' object can be requested explicitely; otherwise the data type of a target object should be defined by a template, as described in the DE002 document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-601

**Title:** Automatic selection of the proper files parser

**Description:** The module should provide functionality to determine and use the proper files parser object based on the source file extension and internal format.

**Verification Method:** I / A / T / D

---

**Requirement ID:** REQ-FUN-602

**Title:** Automatic selection of the target object's data type

**Description:** All file parsers should be able to determine the default data type of a target object from the content of the passed template. This default data type is to be used unless the required target data type is passed explicitely.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-603

**Title:** Automatic selection of a proper template

**Description:** The file parsers should be able to determine the default template suitable for a specific source data file when a template is not passed explicitely. This is possible only for the structured data formats like XML or JSON and if the specific search patterns are defined, see DE002 document. In short, a parser should apply the defined in the search index patterns to the source files until a proper pattern is found or the list of patterns is exhausted. A source data file matches a pattern if it contains all required tags / paths, and the required attributes / end nodes hold the expected values.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-604

**Title:** Strict and relaxed modes of mapping

**Description:** The parsers should support strict and relaxed modes of data mapping concerning missing paths in the source and target objects. The concept of the strict and relaxed should be applied separately for the source and target:

* Source
  * Strict mode for the source (default value) - an exception is raised if a path defined in a template is not found in the source object
  * Relaxed mode for the source - when a path defined in a template is not found in the source object this mapping rule is ignored; the corresponding element in the target object is not modified (if already created) or not created at all (for the dynamically generated elements)
* Target
  * Strict mode for the target - an exception is raised if a path defined in a template is not found in the target object
  * Relaxed mode for the target - when a path defined in a template is not found in the target object
    * This mapping rule is ignored, the corresponding element in the target object is not modified (if already created) or not created at all (for the dynamically generated elements) - if the 'force target elements creation' flag is not set (default value)
    * The corresponding element is added to the target object and the value from the source is copied into - if the 'force target elements creation' flag is set

Normally, the mapping templated are expected to match the structure of the target data type object and the value of this 'strict / relaxed' mode flag for the target object should not affect the mapping. However, a user can request mapping to another data type, which may have a different internal structure than expected by the template. In this case a user should explicitely pass either **True** or **False** value for this flag (as a keyword argument *bStrictTarget*) in order to enforce or suppress exceptions raising due to data structure mismatch. Otherwise due to the default value **None** of this flag the strict or relaxed mode for the target will be selected automatically as described below.

The default (absent) or explicit **None** value of the *bStrictTarget* flag should be treated as **True** if the explicit target class is not given but can be derived from the template, or it is the same as the suggested by the template. If the explicitly given target class is not the same as suggested by the template, the **None** value of the *bStrictTarget* flag should be treated as **False**. The explicitly specified **True** or **False** values of this flag should not be modified in any of the cases.

The scheme is summarized in the table below. The first column - if the target class explicitly provided; the second - if the explicit target class and the suggested by the template are the same; the last three columns - the 'actual' value of the Strict Target Mode to be used depending on the value of the flag passed as the argument (header).

| Target   | Same as Suggested? | None  | True  | False |
| :------- | :----------------: | :---: | :---: | :---: |
| None     | Not applicable     | True  | True  | False |
| NOT None | No                 | False | True  | False |
| NOT None | Yes                | True  | True  | False |

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-605

**Title:** Mapping of a single object and multiple objects at once

**Description:** The file parsers should be able to perform mapping of a single object at a time using the data already extracted from a file and stored in RAM. A single data file should be treated as a collection of such single data objects: one row in a TSV file is a single object, a single dictionary in a list of dictionaries in JSON file is a single data object, etc. An entire XML file or a JSON file representing a single dictionary should be treated as a list of data objects containg a single element. The parsers should also be able to parse multiple files in a single folder, with the result being, naturally, a (nested) sequence of data objects.

**Verification Method:** D

## Alarms, warning and error messages

**Requirement ID:** REQ-AWM-600

**Title:** ValueError is raised when target data type is ambiguious

**Description:** The file parsers should raise ValueError if the target data type is neither specified explicitely or defined in a template.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-601

**Title:** TypeError is raised when a path is passed not as a string

**Description:** Any parser should raise TypeError if it receives any data type but a string when a path to a file or a folder is expected

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-602

**Title:** ValueError in response to a non-existing path

**Description:** Any parser should raise TypeError if it receives a string value as a path, but it is a non-exisiting or wrong path, including a path to an exisiting file when a folder's path is expected, and vice versa.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-603

**Title:** TypeError is raised if not a dicitonary is passed as a parsing template

**Description:** Any parser should raise TypeError exception if it receives neither a dictionary nor the **None** value as the parsing template argument.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-604

**Title:** Improper format of a parsing template results in ValueError exception

**Description:** Any parser should raise ValueError if the passed parsing template dictionary does not contain required entries, or its format does not meet the DSL specifications given in DE002 document.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-605

**Title:** Non-conformity of a mapping template

**Description:** TypeError or ValueError should be raised by any parser if the data mapping template loaded according to the already processed parsing template does not meet the DSL specification defined in the DE001 document.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-606

**Title:** AttributeError in strict source mode

**Description:** Any parser should raise AttributeError if the 'strict source mode' flag is set and the expected path is not found in the source data object. 

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-607

**Title:** AttributeError in strict target mode

**Description:** Any parser should raise AttributeError if the 'strict target mode' flag is set explicitely by the caller or automatically by the parser (see REQ-FUN-604) and the expected path is not found in the target data object. 

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-610

**Title:** Not properly formated input JSON file reuslts in an exception

**Description:** The JSON files parser should raise ValueError exception if the input JSON data file is not properly formatted.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-620

**Title:** Not properly formated input XML file reuslts in an exception

**Description:** The XML files parser should raise xml.etree.ElementTree.ParserError exception if the input JSON data file is not properly formatted.

**Verification Method:** T
