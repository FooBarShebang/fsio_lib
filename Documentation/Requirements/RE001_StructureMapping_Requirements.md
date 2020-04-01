# RE001 Requirements for the Module fsio_lib.StructureMapping

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

**Requirement ID:** REQ-FUN-100

**Title:** Data mapping between objects using JSON templates

**Description:** The module should provide functionality to transfer data from one structured or container object to another on the per element level using theinter-objects internal structure mapping rules defined in a JSON format template file according to the DSL specifications given in DE001 and DE002 documents.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-101

**Title:** Modified and unified attributes resolution 

**Description:** The module should provide a unified access to the elements of container objects (integer index access), entries of mapping objects (string key names access) and attributes (fields) of class instance objects (dot notation access). The corresponding functions should determine and automatically employ index or name access by the type of the respected passed argument; they should also be able to access entries of mapping objects and attributes of classes or class instances by names. Four access modes should be supported: read, write and delete access to the existing elements, attriubtes, etc, and creation of new ones, which are not present yet.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-102

**Title:** Path elements substitutions

**Description:** Path substitutions as defined in DE001 and DE002 documents should be supported, i.e. user should be able to define and use macroses for repetitive sub-paths in a template (similar to C / C++ #define pre-processor directive).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-103

**Title:** Chained definitions and sub-modules in templates

**Description:** The user should be able to re-use existing templates in construction of new templates (similar to C / C++ #include pre-processor directive): by adding new rules to the existing set, by deleting or re-writting the existing rules from another template.

**Verification Method:** I / A / T / D

---

**Requirement ID:** REQ-FUN-104

**Title:** Supported data types

**Description:** Dictionaries, sequences, class and class instance objects, inlcuding XML ElementTree must be supported as data source as well as target. The target should be a mutable type.

**Verification Method:** T

## Alarms, warnings, errors and user messages

**Requirement ID:** REQ-AWM-100

**Title:** Path and attribute manipulation functions raise TypeError

**Description:** Functions responsible for path expansion or substitution as well as functions accessing or modifing an attribute, key or element of an object should raise TypeError exception if any element of the path is not of the data type permitted by the DSL specifications.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-101

**Title:** Path and attribute manipulation functions raise ValueError

**Description:** Functions responsible for path expansion or substitution as well as functions accessing or modifing an attribute, key or element of an object should raise ValueError exception if any element of the path is of the data type permitted by the DSL specifications, but its value is not acceptable, e.g. a negative integer, an empty string or container object.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-102

**Title:** Attribute manipulation functions raise AttributeError

**Description:** AttributeError should be raised when a non-existing attribute, key or element of an object is accessed for reading, modification and deletion, with an exception of creation of a new attribute, etc.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-110

**Title:** Substitution resolution functions raise TypeError

**Description:** TypeError should be raised if the paths substitution rules schema is not defined / passed as a dictionary object, or it has key(s) of not a string type, or any of the bound values is not of the data type permitted by the DSL specifications.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-111

**Title:** Substitution resolution functions raise ValueError

**Description:** ValueError should be raised if, at least, one key in the paths substitution rules schema is a string not strarting with '$' symbol or it contains only '$', or any of the bound values is of the data type permitted by the DSL specifications, but its value is not acceptable, e.g. a negative integer, an empty string or container object, circular definitions of the path substitution, undefined substitutions, etc.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-120

**Title:** Top level mapping functions raise OSError or IOError

**Description:** Functions responsible for loading and parsing the data mapping templates should raise IOError or OSError if they cannot find or open a file containing the mapping template - as the standard, default behaviour for a Python program.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-121

**Title:** ValueError is raised when template is not a proper format JSON file

**Description:** Functions responsible for loading and parsing the data mapping templates should raise ValueError when they cannot parse the provided JSON template because the file is not a proper JSON format data, or the defined mapped rules do not comply with the DSL specifications.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-122

**Title:** AttributeError is raised when path is missing in the source or target objects

**Description:** During the data mapping process an AttributeError is raised if:

* The required element / entry / attribute is not found in the source object, unless the corresponding *ignore* flag is set
* The required element / entry / attribute is not found in the target object, unless the corresponding *ignore* flag is set and the creation of the missing elements in the target object is not forced
* The required element / entry / attribute is not found in the target object, the corresponding *ignore* flag is set, the creation of the missing elements in the target object is forced and there is immutable or incompatible object along the path

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-123

**Title:** Top level mapping functions log the raised exceptions into a file and / or into the console

**Description:** Descriprion / definition of the requirement

**Verification Method:** D
