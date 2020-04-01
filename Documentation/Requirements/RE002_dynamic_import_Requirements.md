# RE002 Requirements for the Module dynamic_import

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

**Requirement ID:** REQ-FUN-200

**Title:** Functional API for ```import module``

**Description:** The module should provide functionality to perform the statement ```import module`` using a function's call. The module to import should be available afterwards.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-201

**Title:** Functional API for ```import module as alias``

**Description:** The module should provide functionality to perform the statement ```import module as alias`` using a function's call. The module to import should be available afterwards under the provided alias name.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-210

**Title:** Functional API for ```from module import object``

**Description:** The module should provide functionality to perform the statement ```from module import object`` using a function's call. The class / function / object to import should be available afterwards.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-211

**Title:** Functional API for ```from module import object as alias``

**Description:** The module should provide functionality to perform the statement ```from module import object as alias`` using a function's call. The class / function / object to import should be available afterwards under the provided alias name.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-220

**Title:** Dot notation / qualified names of the module

**Description:** The implemented functions should accept the qualified name of a module 'library.package.module' as their argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-221

**Title:** Functions return references to the imported objects or modules

**Description:** The implemented functions should return a reference to the imported module / object, which can be assigned to a variable as aliasing. The imported module / object should be accessible under its original name (or alias if provided) and the name of the variable to which its refrence is assigned.

**Verification Method:** T
