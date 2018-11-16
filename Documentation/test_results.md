# Testing of the fsio_lib Library

## UnitTest UT001 - StructureMapping Module Base Functions

### UT001.1 - Function FlattenPath()

#### UT001.1.1 Raises TypeError

The tested function must raise TypeError if the recieved argument is not of any of the allowed types:

* integer number, but not boolean type
* string
* dictionary (mapping type in general) of string keys and values of any of the numeric types (including boolean and floating point) or strings
* flat sequence (list, tuple, etc. - generic sequence) of any of the three types above
* nested sequence of any of the 4 types above

#### UT001.1.2 Raises ValueError

The tested function must raise ValueError if the recieved argument is a negative integer or an empty string, or an empty name for the path or value substituion, or an empty sequence or dictionary.

#### UT001.1.3 Returns Expected Proper Values

With the proper input (see UT001.1.1 definition) the function returns a flat list containg only the elements of the first 3 types. Additional applied rule is that any string containing '.' (dots) and not starting with either '$' or '#' character is split into a sequence of strings by the '.' character

### UT001.2 - Function ResolvePathSubstitutions

#### UT001.2.1 Raises ValueError - Undefined Pattern

The function raises ValueError if at least one pattern references a pattern, for which there is no definition in the same dictionary.

#### UT001.2.2 Raises ValueError - Circular Dependence of Patterns

The function raises ValueError if at least one pair of patterns references each other, i.e. there is a circular dependence.

#### UT001.2.3 Raises ValueError - Improper Path Definition

The function raises ValueError if at least one pattern`s path definition contains a negative integer or an empty string, or an empty name for the path or value substituion, or an empty sequence or dictionary (see UT001.1.3).

#### UT001.2.4 Raises ValueError - Improper Keys

The function raises ValueError if at least one key of the passed dictionary is a string but it does not start with '$' or contains only this character.

#### UT001.2.5 Raises TypeError - Improper Path Definition

The function raises ValueError if at least one pattern`s path definition contains an element of a wrong type, see UT001.1.1.

#### UT001.2.6 Raises TypeError - Improper Keys

The function raises TypeError if at least one key of the passed dictionary is not a string.

#### UT001.2.7 Raises TypeError - Not a Dictionary Argument

The function raises TypeError if the passed argument is not a dictionary (mapping object in general).

#### UT001.2.8 Returns Expected Proper Values

The function properly resolves nested path substituion definitions.

### UT001.3 - Function GetElement

#### UT001.3.1 Raises TypeError

The tested function must raise TypeError if the recieved second argument (path) is not of any of the allowed types:

* integer number, but not boolean type
* string
* dictionary (mapping type in general) of string keys and values of any of the numeric types (including boolean and floating point) or strings
* flat sequence (list, tuple, etc. - generic sequence) of any of the three types above
* nested sequence of any of the 4 types above

#### UT001.3.2 Raises ValueError

The tested function must raise ValueError if the recieved second argument (path) is a negative integer or an empty string, or an empty name for the path or value substituion, or an empty sequence or dictionary.

#### UT001.3.3 Raises AttributeError

Tests that the function raises AttributeError exception if at least one element of the path is not found. This situation occurs if the taret object structure is different then expected by the mapping rules, e.g. with the wrong type of the object.

#### UT001.3.4 Returns the Proper Value

Tests that the function finds the required nested attribute and returns its value, with the numbers (floating point or integer) stored in a string being converted into float and int respectively.

### UT001.4 - Function SetElement

#### UT001.4.1 Raises TypeError - Wrong Path

The tested function must raise TypeError if the recieved second argument (path) is not of any of the allowed types:

* integer number, but not boolean type
* string
* dictionary (mapping type in general) of string keys and values of any of the numeric types (including boolean and floating point) or strings
* flat sequence (list, tuple, etc. - generic sequence) of any of the three types above
* nested sequence of any of the 4 types above

#### UT001.4.2 Raises ValueError - Wrong Path

The tested function must raise ValueError if the recieved second argument (path) is a negative integer or an empty string, or an empty name for the path or value substituion, or an empty sequence or dictionary.

#### UT001.4.3 Raises AttributeError

Tests that the function raises AttributeError exception if at least one element of the path is not found. This situation occurs if the taret object structure is different then expected by the mapping rules, e.g. with the wrong type of the object.

#### UT001.4.4 Raises TypeError - Wrong Type for the Path

The function must raise the TypeError exception if an XML node object is attempted to be assigned as an attribute of another XML node object (not as a sub-element), or a non XML node is attempted to be assigned to a sub-element of an XML node, or an immutable sequence as the last element is attempted to be modified. The path is proper.

#### UT001.4.5 Proper Assignment

The function must perform proper values assignment to the end and intermediate nested elements, as long as the path is proper and the conditions of the test UT0001.4.4 are not applicable (no type conflict).

### UT001.5 - Function DeleteElement

#### UT001.5.1 Raises TypeError - Wrong Path

The tested function must raise TypeError if the recieved second argument (path) is not of any of the allowed types:

* integer number, but not boolean type
* string
* dictionary (mapping type in general) of string keys and values of any of the numeric types (including boolean and floating point) or strings
* flat sequence (list, tuple, etc. - generic sequence) of any of the three types above
* nested sequence of any of the 4 types above

#### UT001.5.2 Raises ValueError - Wrong Path

The tested function must raise ValueError if the recieved second argument (path) is a negative integer or an empty string, or an empty name for the path or value substituion, or an empty sequence or dictionary.

#### UT001.5.3 Raises AttributeError

Tests that the function raises AttributeError exception if at least one element of the path is not found. This situation occurs if the taret object structure is different then expected by the mapping rules, e.g. with the wrong type of the object.

#### UT001.5.4 Proper Deletion

The function must perform proper deletion the end and intermediate nested elements.

### UT001.6 - Function AddElement

#### UT001.6.1 Raises TypeError - Wrong Path

The tested function must raise TypeError if the recieved second argument (path) is not of any of the allowed types:

* integer number, but not boolean type
* string
* dictionary (mapping type in general) of string keys and values of any of the numeric types (including boolean and floating point) or strings
* flat sequence (list, tuple, etc. - generic sequence) of any of the three types above
* nested sequence of any of the 4 types above

#### UT001.6.2 Raises ValueError - Wrong Path

The tested function must raise ValueError if the recieved second argument (path) is a negative integer or an empty string, or an empty name for the path or value substituion, or an empty sequence or dictionary, except for XML representation objects as the target and as the new value, in which case an empty string, an empty sequence and None values are acceptable.

#### UT001.6.3 Proper Overwritting of the Existing Elements

The function must perform proper values assignment to the end and intermediate nested elements, as long as the path is proper and the conditions of the test UT0001.4.4 are not applicable (no type conflict), and the target element exists in the target object

#### UT001.6.4 Raises AttributeError - Not Names in the Missing Part of the Path

The function must raise AttributeError if either a numeric index or a 'choice' dictionary element is encountered in the 'missing' part of the path after the 'branching' point.

#### UT001.6.5 Raises AttributeError - Not a Node / Immutable Object at the Branching Point

The function must raise AttributeError if the 'branching' point (last existing element along the path) is either not an XML node or an immutable object.

#### UT001.6.6 Properly Adds New Branches

The function must properly add new branch from the deepest existing element. For the non XML tree target object - intermediate levels as dictionaries, the last element - as key : value pair with the key is the last element in the path and the value - as passed. For an XML tree target object - all but last elements as nested nodes, the last element as a node as well if the passed values is a node itself, otherwise - the last element as the attribute name, and the passed value as its value.

## UnitTest UT002 - StructureMapping Module 'Main' Functions

### UT002.1 - Function LoadDefinition()

#### UT002.1.1 - Raises IOError / OSError / ValueError

The function raises IOError or OSError if the file cannot be found or opened. The function raises ValueError if the file cannot be parsed using JSON format - the exception raised by the standard JSON parser in such situations.

#### UT002.1.2 - Raises ValueError not Conforming DSL

The function raises ValueError if the file being processed or at least one of the files it includes does not conform with the DSL specifications, specifically:

* Circular definition of a path substitution
* Missing dependence in a definition of a path substitution
* Missing definition of a path or value substitution in a mapping rule
* Incremental addition or deletion rule for non-existing mapping definition sub-dictionary
* Improper path definition in any path / value substitution or mapping rule
* Improper name of either path or value substritution pattern
* Misspelled special names 'PATHS' and 'INCLUDES'

#### UT002.1.3 - Loads and Parses Properly

The function must parse the proper formed JSON file with all entries conforming the mapping DSL properly.

### UT002.2 Function MapValues()

#### UT002.2.1 Raises TypeError - Wrong Type of the Mapping Rules Object

The function raises TypeError if any type but mapping (e.g. dict) is passed as the third argument - the mapping rules dictionary. Regardless of the bStrictSource and bStrictTarget flags.

#### UT002.2.2 Raises TypeError / ValueError - Wrong Format of the Mapping Rules Dictionary

The function raises TypeError or ValueError if the mapping dictionary is not of the proper format (DE001 DSL specifications). Regardless of the bStrictSource and bStrictTarget flags. The most common cases:

* Nested dictionaries keys are not of these types:
    - non-negative integers (indexes)
    - quoted non-negative integers (indexes)
    - strings being quoted proper Python identifiers, except for the single underscore
* The end values (leaves) are not of these types:
    - non-negative integers (indexes)
    - non-empty strings
    - 'choice' dictionaries
    - non-empty (nested) sequences of any of these types

#### UT002.2.3 Raises AttributeError - Not Found Source Element in Strict Mode

The function must raise AttributeError if the required element is not found in the source object and the bStrictSource flag is True.

#### UT002.2.4 Not Raises AttributeError - Not Found Source Element in Soft Mode

The function must not raise AttributeError if the required element is not found in the source object and the bStrictSource flag is False. The data is, however, not copied for this specific mapping rule.

#### UT002.2.5 Raises AttributeError - Not Found Target Element in Strict Mode

The function must raise AttributeError if the required element is not found in the target object and the bStrictTarget flag is True.

#### UT002.2.6 Raises AttributeError - Not Found Target Element in Soft + Forced Mode - Immutable Object in the Path

The function must raise AttributeError if the required element is not found in the target object and the bStrictTarget flag is False, whilst bForceTarget is True and there is an immutable or incopatible object in the path.

#### UT002.2.7 NotRaises AttributeError - Not Found Target Element in Soft + Forced Mode - Possible to Create

The function must not raise AttributeError if the required element is not found in the target object and the bStrictTarget flag is False, whilst bForceTarget is True and the required element can be created.

#### UT002.2.8 Maps Properly

The function performs the mapping properly in the default mode (both source and target are strict) in the case of the mapping rules properly reflecting the structure of both objects. The test cases must include complex / mixed types of the source and target objects, and the source path notation using strings, integers and 'choice' dictionaries:

* Class including nested sequence, dictionary and another struct-like class - > to the same type object
* Class including nested sequence, dictionary and another struct-like class - > to nested XML object
* Class including nested sequence, dictionary and another struct-like class - > to flat dictionary
* flat sequence -> class including nested sequence, dictionary and another struct-like class
* nested XML object -> class including nested sequence, dictionary and another struct-like class

## Functional Test FT001 - StructureMapping Module 'Main' Functions

### FT001.1 Logging of the Exceptions

The functions, to which this test is applicable, must properly log the intercepted and (re-) raised exceptions using the passed object (if any is provided) before raising the exception themselves. In the case of an intercepted exception, its original type and message must be referenced. The logger is not provided if the corresponding argument is not given or None is specified as its value explicitely. The log messages must be clear and informative enough to trace the source of the problem.

*Test method*: passing or not an instance of DualLogger class as an argument of the function being tested within the UT002 test suite. If an instance of DualLogger class is passed, it is set to create the log file in *Tests/Output* folder.

### FT001.1.1 LoadDefinition - Logging of the Exceptions

See definition of FT001.1. Output file name is ut002_1.log.

### FT001.1.2 MapValues - Logging of the Exceptions

See definition of FT001.1 Output file name is ut002_2.log. The **warning** level messages must be logged as well, unless the logger is set to the higher severity level.

## UnitTest UT003 - Module locale_fsio

###  UT003.1 - Function SaveForcedNewLine()

### UT003.1.1 - Enforces the Specified Line Endings

1. Generate a random amount of strings of a random length.
2. Generate the control string by joining them all using the expected line ending sequence in between and at the end of the control string.
3. Save the generated sequence of strings into a file using the function to be tested and pass exactly the same line ending sequence.
4. Open the generated file in the **binary** mode and read its entire content into another large string.
5. Compare the control string with the second string.
6. Repeat steps 2 to 5 with other types of the forced line endings.
7. Repeat step 2 using 'CRLF' ending and step 3 without specifying the forced line ending style (default option), then repeat steps 4 and 5.

### UT003.2 - Function DetectNotation()

#### UT003.2.1 - INT / NL Number Format Recognition

The test function automatically detects the INT / NL number format based on a provided sequence of strings, with some of them being quoted numbers with or without decimal delimiters and/ or separators. If at least one quoted number is unambiguously of INT or NL notation - this choice is to be returned. If the format cannot be determined unambiguously, the default format is INT.

### UT003.3 - Function ConvertFromString()

#### UT003.3.1 - INT / NL Number Format String -> Number Conversion

The function must properly convert the quoted numbers (in strings) stored in either INT or NL notation with possible decimal delimiters, if the format is known *a priori* and passed into the function.

### UT003.4 - Function LoadLines()

#### UT003.4.1 - Spliting into Lines

The function must properly split a text file into lines regardless of the used new line convention: LF, CR or CRLF. The temporary file is generated by the already tested function SaveForcedNewLine() using all of these convention (one at a time) using fixed input data (list of strings). The tested function reads the content of the file back after each iteration. The read-out data is compared with the input data. After the test the temporary file is removed.

Concerns proper treatment of the line endings, their proper removal and preservation of the tailing TABs and spaces.

#### UT003.4.2 - Skipping of the First Lines

The function must propely skip the required amount of the first lines (e.g., a header of tabulated data) regardless the used new line convention: LF, CR or CRLF. The remaining lines must be read out properly, as in UT003.4.1 preserving the tailing TABs and properly removing the new line characters after spliting.

Uses the same test approch as UT003.4.1 but with variable number of lines to skip. The created temporary file is removed afterwards.

### UT003.5 - Function SplitLine()

#### UT003.5.1 - Spliting Lines into Columns

The function must properly split strings into columns (elements) by TABs or an arbitrary amount of usual spaces. Continuous run of usual spaces is treated as a single TAB character regardless of the length of the run. Two TABs or TAB followed by spaces or spaces followed by a TAB are treated as an empty column between them. The leading TAB or space are treated as an
empty column preceding them, tailing TAB or space - as an empty column following them.

### UT003.6 - Function LoadTable()

#### UT003.6.1 - Properly Reads Data from File

The function properly reads data from a text file without *a priori* knowledge of the used conventions on the line ending, TABs or usual spaces for column separation as well as of the number notation (INT / NL with or without decimal delimiters). It is an integration test on the automatic detection of the format, i.e. LoadLines(), SplitLine(), DetectNotation() and ConvertFromString() working together.

Tested formats:

* FBR file - Single column. CRLF line end. Mixed data - str + int + float in dutch scientific notation.
* LMP file - Two columns, spaces. CRLF line end. Floats in international notation.
* LIN file - Three columns, tabs and spaces (variable length). LF line end. Mixed data: ints, floats in international notation and strings.
* Spectrometer (PZ) generated TXT file - Three columns, tab-spaces (variable length). CRLF line end. Mixed data: ints and floats in dutch notation with delimiters.

## UnitTest UT004 - Module GenericParsers

### UT004.1 - Class GenericParser

#### UT004.1.1 - Raises ValueError - No Template and It Cannot Be Determined

Methods **parseFile**() and **parseManyFiles**() raise **ValueError** if no template is provided and it cannot be guessed by the file content. Basically, this is a test on the 'private' method **_getHints**(), which is not supposed to be called directly, only by the public class method **parseFile**(), which is also used by the public class method **parseManyFiles**().

#### UT004.1.2 - Raises TypeError - Improper Type of the Paths to File Elements

Method **parseFile**() must raise **TypeError** if the file name is not a string and method **parseManyFiles**() must raise **TypeError** if either the folder name or any of the file names are not a string.

#### UT004.1.3 - Raises ValueError - Missing Parts of the Paths to File

Methods **parseFile**() and **parseManyFiles**() raise **ValueError** if, at least, one file path does not point to an existing file. Method **parseManyFiles**() also raises **ValueError** if the folder path argument does not point to an existing folder.

#### UT004.1.4 - Raises TypeError by _checkTemplate()

Methods **parseSingleObject**(), **parseFile**() and **parseManyFiles**() raise **TypeError** if the template agrument is not a template (but not None). Internally, it is a check on the 'private' class method _**checkTemplate**().

#### UT004.1.5 - Raises ValueError by _checkTemplate()

Methods **parseSingleObject**(), **parseFile**() and **parseManyFiles**() raise **ValueError** if the template agrument is a dictionary, but it does not have the key 'DataMapping', or the value bound to this key is not a dictionary. Internally, it is a check on the 'private' class method _**checkTemplate**().

#### UT004.1.6 - Raises TypeError or ValueError - Mapping is not DSL Conforming

The methods **parseSingleObject**(), **parseFile**() and **parseManyFiles**() raise **TypeError** or **ValueError** if the mapping dictionary is not of the proper format (DE001 DSL specifications). Regardless of the *bStrictSource* and *bStrictTarget* flags. Note, the **parseFile**() and **parseManyFiles**() methods are checked only with the derived test clases, not this one. Under the hood, this test checks that the function *fsio_lib.StructureMapping.MapValues*(), hence - *fsio_lib.StructureMapping.FlattenPath*(), are called, and the exceptions raised by them propagates.

#### UT004.1.7 - Raises AttributeError - Missing Source Element in Strict Mode

The method **parseSingleObject**() raises **Attribute** error if the source object does not have the required element and the flag *bStrictSource* is **True**. If the flag *bStrictSource* is **False**, the exception is not raised, but the corresponding element of the target object is not changed but remains at its initial value.

#### UT004.1.8 - Raises AttributeError - Missing Target Element in Strict Mode

The method **parseSingleObject**() raises **Attribute** error if the target object does not have the required element and the flag *bStrictTarget* is **True**. If the flag *bStrictTarget* is **False** and *bForceTarget* is **False** - the exception is not raised, but the missing element is not created; if the *bForceTarget* is **True** - the missing element is created and the proper value is assigned to it.

### UT004.2 - Class TSV_Parser

#### UT004.2.1 - Raises ValueError - No Template and It Cannot Be Determined

Same as UT004.1.1

#### UT004.2.2 - Raises TypeError - Improper Type of the Paths to File Elements

Same as UT004.1.2

#### UT004.2.3 - Raises ValueError - Missing Parts of the Paths to File

Same as UT004.1.3

#### UT004.2.4 - Raises TypeError by _checkTemplate()

Same as UT004.1.4

#### UT004.2.5 - Raises ValueError by _checkTemplate()

Same as UT004.1.5

#### UT004.2.6 - Raises TypeError or ValueError - Mapping is not DSL Conforming

Same as UT004.1.6

#### UT004.2.7 - Raises AttributeError - Missing Source Element in Strict Mode

Same as UT004.1.7

#### UT004.2.8 - Raises AttributeError - Missing Target Element in Strict Mode

Same as UT004.1.8

#### UT004.2.9 - Raises AttributeError - Missing Source Element in Strict Mode

Extension of the test UT004.2.7 onto the methods **parseFile**() and **parseManyFiles**(). In the case of not raising the exception, only the first object returned is tested in terms of its content. The target class and the mapping dictionary are provided explicitly.

#### UT004.2.10 - Raises AttributeError - Missing Target Element in Strict Mode

Extension of the test UT004.2.8 onto the methods **parseFile**() and **parseManyFiles**(). In the case of not raising the exception, only the first object returned is tested in terms of its content. The target class and the mapping dictionary are provided explicitly. The **None** (explicit or default) value of the flag bStrictTarget in this case is treated as **True**.

#### UT004.2.11 - Properly Copies the Data with Explicit and Proper Mapping and Target

The methods **parseFile**() and **parseManyFiles**() create the expected number of the target objects packed into the expected container types and fill them properly when both the target class (type) and the template are provided explicitely, and the mapping matches the structure of the both source and target objects.

#### UT004.2.12 - Properly Copies the Data with Explicit and Proper Mapping but without Target

The methods **parseFile**() and **parseManyFiles**() create the expected number of the target objects packed into the expected container types and fill them properly when only the template is provided explicitely, and the mapping matches the structure of the both source and target objects. The target class (type) is not provided, but taken from the template. All flags are left at their default values.

#### UT004.2.13 - Strict Target Mode Choice with Target Class Definition by Template

The default (absent) or explicit **None** value of the *bStrictTarget* flag should be treated as **True** if the explicit target class is not given but can be derved from the template, or it is the same as the suggested by the template. If the explicitly given target class is not the same as suggested by the template, the **None** value of the *bStrictTarget* flag should be treated as **False**. The explicitly specified **True** or **False** values of this flag should not be modified in any of the cases.

The scheme is summarized in the table below. The first column - if the target class explicitly provided; the second - if the explicit target class and the suggested by the template are the same; the last three columns - the 'actual' value of the Strict Target Mode to be used depending on the value of the flag passed as the argument (header).

| Target   | Same as Suggested? | None  | True  | False |
| :------- | :----------------: | :---: | :---: | :---: |
| None     | Not applicable     | True  | True  | False |
| NOT None | No                 | False | True  | False |
| NOT None | Yes                | True  | True  | False |

### UT004.3 - Class JSON_Parser

#### UT004.3.1 - Raises ValueError - No Template and It Cannot Be Determined

Same as UT004.1.1

#### UT004.3.2 - Raises TypeError - Improper Type of the Paths to File Elements

Same as UT004.1.2

#### UT004.3.3 - Raises ValueError - Missing Parts of the Paths to File

Same as UT004.1.3

#### UT004.3.4 - Raises TypeError by _checkTemplate()

Same as UT004.1.4

#### UT004.3.5 - Raises ValueError by _checkTemplate()

Same as UT004.1.5

#### UT004.3.6 - Raises TypeError or ValueError - Mapping is not DSL Conforming

Same as UT004.1.6

#### UT004.3.7 - Raises AttributeError - Missing Source Element in Strict Mode

Same as UT004.1.7

#### UT004.3.8 - Raises AttributeError - Missing Target Element in Strict Mode

Same as UT004.1.8

#### UT004.3.9 - Raises AttributeError - Missing Source Element in Strict Mode

Same as UT004.2.9

#### UT004.3.10 - Raises AttributeError - Missing Target Element in Strict Mode

Same as UT004.2.10

#### UT004.3.11 - Properly Copies the Data with Explicit and Proper Mapping and Target

Same as UT004.2.11. Also checks that the 'special' cases of the improper formed JSON as '{} {}' or '{}, {}' instead of '[{}, {}]' are treated as lists of dictionaries as well.

#### UT004.3.12 - Properly Copies the Data with Explicit and Proper Mapping but without Target

Same as UT004.2.12. Also checks that the 'special' cases of the improper formed JSON as '{} {}' or '{}, {}' instead of '[{}, {}]' are treated as lists of dictionaries as well.

#### UT004.3.13 - Strict Target Mode Choice with Target Class Definition by Template

Same as UT004.2.13

#### UT004.3.14 - Raises Exceptions with Wrong Format Source Data File

The methods **parseFile**() and **parseManyFiles**() raise **ValueError** if the source data file is not a proper format JSON, excluding the cases of '{} {}' or '{}, {}' instead of '[{}, {}]'.

#### UT0004.3.15 - Automatic Detection of the Template and Target Class

The methods **parseFile**() and **parseManyFiles**() must return the target objects of the expected types (class instances) properly filled with the data from the source file(s) and packed into the proper container objects - when neither the template nor the target class are explicitely provided, but the required template can be selected on the basis of the source file content. Internally, this test checks the 'private' method _getHints().

### UT004.4 - Class XML_Parser

#### UT004.4.1 - Raises ValueError - No Template and It Cannot Be Determined

Same as UT004.1.1

#### UT004.4.2 - Raises TypeError - Improper Type of the Paths to File Elements

Same as UT004.1.2

#### UT004.4.3 - Raises ValueError - Missing Parts of the Paths to File

Same as UT004.1.3

#### UT004.4.4 - Raises TypeError by _checkTemplate()

Same as UT004.1.4

#### UT004.4.5 - Raises ValueError by _checkTemplate()

Same as UT004.1.5

#### UT004.4.6 - Raises TypeError or ValueError - Mapping is not DSL Conforming

Same as UT004.1.6

#### UT004.4.7 - Raises AttributeError - Missing Source Element in Strict Mode

Same as UT004.1.7

#### UT004.4.8 - Raises AttributeError - Missing Target Element in Strict Mode

Same as UT004.1.8

#### UT004.4.9 - Raises AttributeError - Missing Source Element in Strict Mode

Same as UT004.2.9

#### UT004.4.10 - Raises AttributeError - Missing Target Element in Strict Mode

Same as UT004.2.10

#### UT004.4.11 - Properly Copies the Data with Explicit and Proper Mapping and Target

Same as UT004.2.11

#### UT004.4.12 - Properly Copies the Data with Explicit and Proper Mapping but without Target

Same as UT004.2.12

#### UT004.4.13 - Strict Target Mode Choice with Target Class Definition by Template

Same as UT004.2.13

#### UT004.4.14 - Raises Exceptions with Wrong Format Source Data File

The methods **parseFile**() and **parseManyFiles**() raise **xml.etree.ElementTree.ParseError** if the source data file is not a proper format XML.

### UT004.5 - Function parseFile()

Integration test suite.

#### UT004.5.1 - Raises TypeError

Function parseFile() raises TypeError if the file name is not a string.

#### UT004.5.2 - Raises ValueError

Function **parseFile**() raises **ValueError** if the file path does not point to an existing file.

#### UT004.5.3 - Properly Automatically Determines the Template and Target Class and Parses

Function **parseFile**() must automatically detect the required parsing template and the target class by the content of the file, when possible, and return the proper container object with the proper type elements, filled with the data from the source file as expected.

### UT004.5 - Function parseFile()

Integration test suite.

#### UT004.6.1 - Raises TypeError

Function **parseManyFiles**() raises **TypeError** if the folder name is not a string or, at least, one base file name is not a string.

#### UT004.6.2 - Raises ValueError

Function **parseManyFiles**() raises **ValueError** if the file path does not point to an existing file, for any of the base names, which includes the path to their folder not pointing to an existing folder.

#### UT004.6.3 - Properly Automatically Determines the Template and Target Class and Parses

Function **parseManyFiles**() must automatically detect the required parsing template and the target class by the content of the file - individually per file, when possible, and return the proper container object with the proper type elements, filled with the data from the source file as expected.

## Functional Test FT002 - GenericParsers Module 'Main' Functions and Class Methods

### FT002.1 Logging of the Exceptions

All functions and public class methods must properly log the intercepted and (re-) raised exceptions using the passed object (if any is provided) before raising the exception themselves. In the case of an intercepted exception, its original type and message must be referenced. The logger is not provided if the corresponding argument is not given or None is specified as its value explicitely. The log messages must be clear and informative enough to trace the source of the problem.

*Test method*: passing or not an instance of DualLogger class as an argument of the function / method being tested within the UT004 test suite. If an instance of DualLogger class is passed, it is set to create the log file in *Tests/Output* folder.

## Test Results

| Test Id    | Tested Module    | Tested Function / Method | Test Module             | Test Type  | Result | Date       |
| :--------- | :--------------: | :----------------------: | :---------------------: | :--------: | :----: | :--------: |
| UT001.1.1  | StructureMapping | FlattenPath              | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.1.2  | StructureMapping | FlattenPath              | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.1.3  | StructureMapping | FlattenPath              | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.1  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.2  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.3  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.4  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.5  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.6  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.7  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.2.8  | StructureMapping | ResolvePathSubstitutions | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.3.1  | StructureMapping | GetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.3.2  | StructureMapping | GetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.3.3  | StructureMapping | GetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.3.4  | StructureMapping | GetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.4.1  | StructureMapping | SetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.4.2  | StructureMapping | SetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.4.3  | StructureMapping | SetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.4.4  | StructureMapping | SetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.4.5  | StructureMapping | SetElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.5.1  | StructureMapping | DeleteElement            | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.5.2  | StructureMapping | DeleteElement            | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.5.3  | StructureMapping | DeleteElement            | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.5.4  | StructureMapping | DeleteElement            | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.6.1  | StructureMapping | AddElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.6.2  | StructureMapping | AddElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.6.3  | StructureMapping | AddElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.6.4  | StructureMapping | AddElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.6.5  | StructureMapping | AddElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT001.6.6  | StructureMapping | AddElement               | ut001_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.1.1  | StructureMapping | LoadDefinition           | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.1.2  | StructureMapping | LoadDefinition           | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.1.3  | StructureMapping | LoadDefinition           | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.1  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.2  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.3  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.4  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.5  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.6  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.7  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| UT002.2.8  | StructureMapping | MapValues                | ut002_structure_mapping | UnitTest   | Pass   | 2018-11-15 |
| FT001.1.1  | StructureMapping | LoadDefinition           | ut002_structure_mapping | Functional | Pass   | 2018-11-15 |
| FT001.1.2  | StructureMapping | MapValues                | ut002_structure_mapping | Functional | Pass   | 2018-11-15 |
| UT003.1.1  | locale_fsio      | SaveForcedNewLine        | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT003.2.1  | locale_fsio      | DetectNotation           | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT003.3.1  | locale_fsio      | ConvertFromString        | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT003.4.1  | locale_fsio      | LoadLines                | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT003.4.2  | locale_fsio      | LoadLines                | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT003.5.1  | locale_fsio      | SplitLine                | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT003.6.1  | locale_fsio      | LoadTable                | ut003_locale_fsio       | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.1  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.2  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.3  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.4  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.5  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.6  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.7  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.1.8  | GenericParsers   | GenericParser            | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.1  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.2  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.3  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.4  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.5  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.6  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.7  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.8  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.9  | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.10 | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.11 | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.12 | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.2.13 | GenericParsers   | TSV_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.1  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.2  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.3  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.4  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.5  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.6  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.7  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.8  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.9  | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.10 | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.11 | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.12 | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.13 | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.14 | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.3.15 | GenericParsers   | JSON_Parser              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.1  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.2  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.3  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.4  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.5  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.6  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.7  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.8  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.9  | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.10 | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.11 | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.12 | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.13 | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.14 | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.4.15 | GenericParsers   | XML_Parser               | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.5.1  | GenericParsers   | parseFile()              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.5.2  | GenericParsers   | parseFile()              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.5.3  | GenericParsers   | parseFile()              | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.6.1  | GenericParsers   | parseManyFiles()         | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.6.2  | GenericParsers   | parseManyFiles()         | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| UT004.6.3  | GenericParsers   | parseManyFiles()         | ut004_generic_parsers   | UnitTest   | Pass   | 2018-11-15 |
| FT002.1    | GenericParsers   | all functions / methods  | ut002_structure_mapping | Functional | Pass   | 2018-11-15 |

## Retro-testing log

### 2018-11-15

Retested all cases after fixes introduced into the modules **StructureMapping** and **GenericParsers**