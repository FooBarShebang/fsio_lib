# DE001 Specification of the Values Mapping DSL

## Table of Content

* [Formal Definition](#Formal-Definition)
* [Informal Definition](#Informal-Definition)
* [Recommendations for Parsers and Mappers Implementation](#Recommendations-for-Parsers-and-Mappers-Implementation)

## Formal Definition

The formal definitions are described using the slightly modified Augmented Bakus-Naur Form notation, see see [RFC 5234](https://tools.ietf.org/html/rfc5234) or [Wikipedia](https://en.wikipedia.org/wiki/Augmented_Backus%E2%80%93Naur_form). The single addition to the original specification of the ABNF is the *exclusion*. The binary operator "^" can be used between a range of terminal values on the left hand, and a single terminal value or a range of the terminal values on the right hand - in the sense of any terminal value from the left-hand range except one or more values.

### Basic Rules

```abnf
NUMBER              = 1*DIGIT
                        ; any decimal number

FLOAT               = ["-" / "+"] 1*DIGIT ["." *DIGIT]

STRING              = DQUOTE VCHAR^("$" / "#") *VCHAR DQUOTE
                        ; any valid ASCII string in double quotes

BOOL                 = "true" / "false"
                        ; JSON representation of the boolean values

IDENTIFIER          = (ALPHA / "_") *(ALPHA / DIGIT / "_")
                        ; valid Python identificator
                        
NAME-STRING         = DQUOTE IDENTIFIER DQUOTE
                        ; valid Python identificator in double quotes

DOT-NAME-STRING     = DQUOTE IDENTIFIER 1*("." IDENTIFIER) DQUOTE
                        ; quoted valid Python name of a nested attribute

STR-NUMBER          = DQUOTE NUMBER DQUOTE
                        ; quoted decimal number

PATH-STRING         = DQUOTE "$" 1*(ALPHA / DIGIT) DQUOTE
                        ; proper name of a substituion path string

INCLUDE-STRING      = DQUOTE "#" 1*(ALPHA / DIGIT) DQUOTE
                        ; proper name of a substitution dicitonary

FILE-STRING         = DQUOTE 1*VCHAR "." 1*4ALPHA DQUOTE
                        ; proper name of an import file
```

### Structure Rules

```abnf
mapping-definition  = "{" [includes ","] [paths ","] *(extras ",")
                       *(addition ",") *(removal ",") *(mapping ",") mapping "}"
                        ; actual order may differ since the dictionary object
                        ; is not ordered, what is important that there is a
                        ; single "," (comma) between each element, but not after
                        ; the last one

includes            = DQUOTE "INCLUDES" DQUOTE ":" includes-dict

paths               = DQUOTE "PATHS" DQUOTE ":" path-macro-dict

extras              = STRING ":" (FLOAT / STRING)

addition            = DQUOTE "+" STRING DQUOTE ":" mapping-dict
                        ; mapping paths to be added to a specific mapping
                        ; the key must be the name of one of the mappings
                        ; prefixed with "+" sign

removal             = DQUOTE "-" STRING DQUOTE ":"
                        [path-to-entry *("," path-to-entry)]
                        ; paths to be removed from a specific mapping
                        ; the key must be the name of one of the mappings
                        ; prefixed with "-" sign
                        ; each path-to-entry must reference an item in the
                        ; target (not source) object

mapping             = STRING ":" mapping-dict

includes-dict       = "{" include-entry *("," include-entry) "}"

path-macro-dict     = "{" path-macro-entry *("," path-macro-entry) "}"

mapping-dict        = "{" mapping-entry *("," mapping-entry) "}"
mapping-dict        =/ INCLUDE-STRING

include-entry       = INCLUDE-STRING ":" FILE-STRING
include-entry       =/ INCLUDE-STRING ":" "[" FILE-STRING "," path-to-entry "]"

path-macro-entry    = PATH-STRING ":" path-to-entry

path-to-entry       = path-entry-element^choice-dict
path-to-entry       =/ "[" (path-entry-element / path-to-entry)
                        *("," path-entry-element / path-to-entry) "]"

path-entry-element  = NUMBER / NAME-STRING / DOT-NAME-STRING / choice-dict
path-entry-element  =/ PATH-STRING

choice-dict         = "{" choice-entry *("," choice-entry) "}"

choice-entry        = NAME-STRING ":" (FLOAT / STRING / BOOL)

mapping-entry       = mapping-key ":" (path-entry-element / mapping-dict)

mapping-key         = NAME-STRING / STR-NUMBER / NUMBER
                        ; a number must be in double quotes only inside JSON
                        ; file, it is acceptable and advised to store it as
                        ; plain integer (not negative) in dictionaries
```

### Informal Definition

The mapping DSL describes the rules of syntax for forming dictionaries of the mapping the content of one container or structured object onto another container or structured object. These dictionaries are to be stored in and read-out from JSON files, therefore the JSON syntax rules are applied.

A minimal mapping dictionary contains one or more nested dictionaries stored as values paired to string keys. The names of the keys are interpreted by the parser, which use this mapping dictionary, in order to decide which of the nested dictionaries to use and to which target object to apply. Thus, these names may be any valid strings.

The nested dictionaries themselves describe the rules on which (nested) attribute / element of the source object is to mapped on which (nested) attribute / element of the target object. The keys must be strings (due to JSON syntax): either a proper Python identifier (for target object attributes or dictionary keys) or a non-negative integer number (index of an element of a container type) taken into double quotes. The values paired to the keys might be either paths to the corresponding attribute / element of the source object (for the *end nodes* of the target object, e.g. numbers, strings or boolean types) or nested dictionaries of the same structure (for the attributes / elements of the target object referencing a nested containter / structured object). This definition is recursive, and it allows an arbitrary level of nesting. Naturally, each key value may be present only once amongst the keys of any dictionary, but it is allowed amongst the keys of the ancestors, descendants or siblings of this particular dictionary.

The path to a source (nested) attribute can be

* a non-negative integer, a string or a plain dictionary with string keys and values being either strings, or numbers or boolean types
* a plain list of any number of the types above
* a nested list containing any number of the elements from the above
* etc. - deeper nesting of the elements from the first option

Again, the definition is recursive, which allows arbitrary level of nesting. Strings containing ." (dots) are interpreted as paths to the nested attributes / elements. For example:

* 1 OR [1] - the source object is a container (sequence), and its 2nd element (index 1) is requested, i.e. *source*[1]
* "a" OR ["a"] - the source is a structured object and the value of its attribute "a" is requested, i.e. *source*.a, OR the source is a dictionary and the value paired to its key "a" is requested, i.e. *source*["a"]
* "a.b" OR ["a", "b"] - the source is a nested strucutured object and the value of *source.a.b" is requested, OR the source is a nested dictionary and the value *source*\["a"\]\["b"\] is requested, OR *source*["a"].b OR *source*.a["b"]
* {"name" : "test", "pass" : true} OR [{"name" : "test", "pass" : true}] - the source is a sequence (or compatible) object containing dictionaries / structured objects as its element, the required element must have the key / attribute "name" and its value must be "test" as well as the key / attribute "pass" with the value True; this pattern allows selection of the element with known *properties* but unknown index from a sequence. **Warning**: a 'choice dictionary' may be only an element of a sequence, not the 'top'(single) element of the path`s definition.

On the more advanced level the top level dictionary may have a *path substitution* entry - a plain dictionary paired to the special key "PATHS". Each entry in this plain dictionary is a pair of string key and a *path* value as defined above. Each string key must start with "$". The actual mapping dictionaries may use these keys ("$" strings) as a substitution of a part of or the entire path to the source attribute / element. Thus, following two definitions are identical:

```
{
    "PATHS" = {
        "$common" : ["a", 1, "b"]
    },
    "mapping_rule" :{
        "Arg1" : ["$common", 2],
        "Arg2" : ["$common", 1]
    }
}
```

is equivalent to

```
{
    "mapping_rule" :{
        "Arg1" : ["a", 1, "b", 2],
        "Arg2" : ["a", 1, "b", 1]
    }
}
```

The *path substitution* allows shorter and cleaner definitions, especially when the required (source) values are deeply nested.

The *path substitution" dictionary may contain arbitrary number of entries. The *path substitution* entries may use their siblings substitutions in their own definition as long as there is no circular dependency.

On even more advanced level the actual mapping rules may also be imported from another JSON files via *value substitution*. The *value substitution* definition is defined as a plain dictionary paired as value to the special key "INCLUDES" at the top level. The definitions dictionary must have string keys with their names starting with "#". The values paired to these keys must also be strings and contain paths to existing and proper JSON files, or 2-elements list with the first element being path to a file (string) and the second - a proper path to an element within the object to be imported from that file.

In the first case the entire content of the imported JSON file is treated as the *value substitution* for a specific mapping rules dictionary, whereas in the second case - a specific (nested) element of the imported object is extracted and used as the *value substitution*, whilst the rest of the imported data is ignored and discarded.

The *value substitution* can be used only at the top level, i.e. by assigning it to a mapping rule key instead of an actual dictionary definition.

**Note**: the *value substitution* imported from another JSON file must be fully resolved before it can be applied. For instance, the imported JSON file may have its own *path substitutions* and / or *value substitutions*, but they are resolved and applied during the import of that file, therefore, the other dictionary, which imports it, is unaware of the substitutions used in the imported file.

In addition to the *value substitution* the *incremental definition* is also supported. To define an addition a special entry is to be added at the top level (multiple but unique keys entries are also allowed). The key of this entry must be a string starting with "+" and followed by the name of any of the mapping rules definitions made in the same top level dictionary. The value paired to this key must be either a *value substitution* or an actual mapping rules definition dictionary. The idea behind is that a set of mapping rules can be imported from another file and one or more rules can be added.

To define a removal a special entry is to be added at the top level (multiple but unique keys entries are also allowed). The key of this entry must be a string starting with "-" and followed by the name of any of the mapping rules definitions made in the same top level dictionary. The value paired to this key must be a list of one or more paths referring an attribute / element (may be nested) of the **target** object, which are defined in the corresponding *main* mapping rules definition dictionary.

Both addition and removal are intended for clearer and shorter definitions in the case, when the source or target object structure differ only slightly between the different mapping definitions.

Example:

_**file1.json**_

```
{
    "mapping_rule" :{
        "Arg1" : ["a", 1, "b", 2],
        "Arg2" : ["a", 1, "b", 1]
    }
}
```

_**file2.json**_


```
{
    "Arg1" : ["a", "b"]
}
```

_**main definition**_

```
{
    "INCLUDES" : {"#1": ["file1.json", "mapping_rule"],
                    "#2" : "file2.json"},
    "rule1" : "#1",
    "rule2" : "#2",
    "+rule2" : {
        "Arg2" : "c"
    },
    "-rule1" : ["Arg2"]
}
```

is equivalent to:

_**main definition**_

```
{
    "rule1" : {
        "Arg1" : ["a", 1, "b", 2]
    },
    "rule2" : {
        "Arg1" : ["a", "b"],
        "Arg2" : "c"
    }
}
```

Finally, *extra entries* may be defined at the top level as key : values pairs with the keys being strings and not starting with "+" or "-" signs, and the values being either strings not starting with "$" / "#", or any other valid JSON types except for the dictionaries. Neither *path substitutions* nor *value substitutions* are applied to these entries. Their purpose is to store some data *as it is*, for instance, some instructions / additional data to be used by parsers.

## Recommendations for Parsers and Mappers Implementation

The recommended order of the parsing of a mapping definition stored in a JSON file:

* Load the file into an in-memory dictionary object
* The not found file or an excepion raised by JSON parser / loader is an error situation, and it must result in an exception
* If the "PATHS" key is present - *path substitutions*
  - sort the substitions definitions by the amount of other substitutions used in them
  - start with the definitions using 0 other substitutions and use them to (partially) resolve the remaining definitions
  - Each round of the *already resolved* definitions application to another substitutions must yield at least one new *fully resolved* substituion definition
  - Repeat the process until all definitions are resolved or no more new definitions can be resolved
    + if not all substitution definitions can be resolved - the circular dependence exists in their definitions; such situation is an error, and it must result in an exception
* If the "INCLUDES" key is present - *value substitutions*
  - For each entry in the substitution definitions import the corresponding file; it may be implemented as the recursive call
  - If a substituion entry is defined only as a path to a file - replace this string value by the entire content of the imported JSON file - a proper Python type
  - If a sustitution entry is defined as a path to a file and a path to an element within the object imported from that file - retrieve the value of the element referenced by the path - replace the definition of the substitution by that value
    + if the required element is not found within the imported object - raise an exception
* Select all entries defining the actual *mappings* and ignore the *extras*
  - Apply the *path substitutions* and the *value substitutions* to the mapping definitions
  - Apply incremental additions, if any is defined:
    + Add new (nested) entries to the corresponding dictionaries
    + An already exisiting entry with the same path within the *target* object is to be overwritten
  - Apply incremental removals, if any is defined - remove the corresping mapping definition by the given path within the *target* object
  - Flatten and unify the paths of each entry within each mapping definition dictionary - each path to an element / attribute of the *source* object is a list of string, numeric or dictionary elements, whith each element referencing only a single level of the nesting
    + The improper defined path, i.e. containing not allowed elements, is an error situation, which must result in an exception
* Either remove the "PATHS", "INCLUDES" and incremental addition / removal entries; OR create a new dictionary object and copy the actual *mapping definition* entries (now fully resolved) and *extra* entries into it
* Return a dictionary containing only the *mapping definition* and *extra* entires

Recommendations for the mapping implementation:

* The mapping rules assume that for each rule the corresponding elements / attributes exist in both the *source* and *target* objects; a not found element / atttribute in either of them is an indication of:
  - The improper mapping rule definition
  - OR the improper / unexpected structure of the corresponding object
* A *strict mode* mapper should, at least, report such situations or even raise an exception
* A *soft mode* mapper may ignore the corresponding rule and proceed to the next
  - The advantage of the *soft mode* is that broader generic rules can be applied to different specific *target* and / or *source* object types, which may miss one or several elements / attributes expected by the rules
  - The disadvantage of the *soft mode* is that it is more difficult to 'debug' and it may 'hide' the actual implementation or input data errors
* The most universal approach is to implement a mapper with independently switchable between *soft* and *strict* modes for the *source* and *target* objects
* Specifically for the mapping from / to an XML representation object, e.g. ElementTree, etc.:
  - Path element given by an integer number (index) or by a dictionary (required elements and their values) is to be applied to the list of the *children nodes*
    + the required elements are supposed to be usual attributes of an XML node
  - Path element given by a string (name of an element / attribute) should be looked up by that name in the following order:
    + amongst the *children nodes* of the XML node
    + amongst the usual attributes of the XML node
    + amongst the 'text' and 'tail' of the XML node (as specail attributes)