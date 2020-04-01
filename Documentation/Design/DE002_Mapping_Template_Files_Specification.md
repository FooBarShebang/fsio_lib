# DE002 Specification of the Structure of the Parsing Template Files

## Parsing Templates

Each file parsing template is to be stored in one of the sub-folders "TSV", "JSON" or "XML" of the folder "Templates" within the package *fsio_lib*, with the name of the sub-folder corresponding to the type of the source data file. Each templates describes the mapping rules for parsing of a single data element within the source file onto a single instance of the target class / type, whereas the TSV and JSON but not XML files may contain multiple data elements. The result of the parsing of a single source file is always a list of instances of the target class / type, even if the source file contains but one data element, in which case the generated results list also contains only a single element.

The single data element is:

* a single row (line) within TSV data file
* a single dictionary in the case of the JSON format data file
  - the entire content of the JSON file, if it stores a dictionary
  - a single element of an array (list) of the dictionaries, if the JSON file stores such an array
* the entire content of an XML file

The file parsing templates may also contain the file loading hints, e.g. - the length of the header / number of the first lines to skip within a TSV file, and the suggested target class.

Each template is formed as a dictionary and is stored as an JSON format file.

### Mandatory Entries

The only mandatory entry is the key "**DataMapping**" with the bound value being a dictionary, which defines the mapping rules set conforming the [DE001 DSL specifications](./DE001_Mapping_DSL_Specification.md). The most important points to remember are:

* It may be a flat or nested dictionary with each level of nesting corresponding to exactly one level of the target object`s data nesting structure
* At each level of the template`s dictionary nesting the allowed names of the keys are:
  - double quoted proper Python identifiers (hence, no dot notation) as the attributes / keys names at the corresponding nesting level of the target object
  - double quoted non-negative integer numbers as the sequence type container`s elements indexes at the corresponding nesting level of the target object
* The values bound to these keys may be:
  - a dictionary - the next nesting level`s structure within the target object
  - an 'end node' - double quoted strings, including the dot notation (e.g. "a.b"), non-negative integer numbers, or (nested) lists of these two types and 'choice' dictionaries - the proper description of a path within the source object to obtain a value, which will be assigned to this 'end node' in the target object

### Optional Entries - Generic

Two optional entries may be included into a template: "**TargetClassModule**" and "**TargetClass**" keys with the bound string values. These two entries must be included both or not used at all. For instance:

```json
{
    ...
    "TargetClassModule" : "mylib.classes",
    "TargeClass" : "ClassA",
    "DataMapping" : {
        ...
    }
    ...
}
```

In this case, the parser will import *ClassA* from the module *mylib.classes*, unless it has been already imported earlier, and will use this class as the suggested target class / type. If the required target class is not explicitly specified, the suggested by the template target class is used instead to instantiate the target objects.

### Optional Entries - TSV Specific

Specifically for the TSV format the parser searches for the entry with the key "**HeaderOffser**, which must have a non-negative integer as the bound value. This entry indicates, that the corresponding number of the first lines in the source file are the header, and they must be skipped. If such an entry is not found in an TSV parsing template the default value of 0 is used instead (all lines of the file are taken).

### Other Entries

All other top level entries in a file parsing template are currently ignored by the parsers, so they can be used as comments / human readable description of the template, its purpose and targeted source files.

### Warning

Since the strings starting with "$" are considered to be path substitutions, the strings starting with "$", including "$" alone, are not allowed as keys / attribute names in the source data file, because they cannot be used in the proper path within the source object definition. The JSON format, however, allows such keys / attributes. Therefore, the **JSON_Parser._loadFile**() method automatically replaces all encountered "$" characters in the source file into "%" characters. It must be taken into account during the creation of the mapping template. For instance, if the 'original' path within the JSON object looks like "a.$.b", i.e. path within such dictionary {"a" : {"$" : {"b" : "some_value"}}}, must be specified as "a.%.b" because the key "$" will be automatically replaced by "%".

## Templates Index

The special JSON file **index.json** in the folder *Templates* is created in order to support the automatic selection of the proper parsing template based on the source file content. It is a list (array) of flat dictionaries, whereas each dictionary must have:

* an entry with the key "Type" and the bound value "XML", "JSON" or "TSV" - the names of the sub-folders within the "*Templates*" folder and the corresponding types of the source data files
* an entry with the key "BaseName" and the bound string value as the base name of the referenced template within the corresponding sub-folder
* at least one other entry with a string key and the bound value being of any JSON allowed types - the search / selection tag

Each entry (dictionary) in the **index.json** file refers a single file parsing template. The new entries are supposed to be made by the user, when he adds new templates to the library, which should be selected automatically during the specific format source file processing. In this case the user must create new entries in the search indexes as well, see the next section.

## Search Indexes

The search indexes are the sets of templates describing how a proper file parsing template is to be selected based on the content / structure of the source data file. This mechanism is implemented only for parsing of the structured source data files, currently - XML and JSON. Both the *fsio_lib.GenericParsers.JSON_Parser* and the *fsio_lib.GenericParsers.XML_Parser* classes have their own search indexes, stored in the separate files - "*json_search_index.json*" and "*xml_search_index.json*" respectively - within the folder "*Templates*".

A search index is a list (array) of dictionaries. Each search index entry (dictionary) describes a structure of the source file, which can match one or more entries in the **index.json** file, thus - the corresponding file parsing templates. Each must have:

* at least, one or both elements with the keys "SearchTags" / "Markers"
  - "Markers" entry`s bound value is a list of lists of, at least, 2 elements each, with the first element of the nested list being the expected value and the rest (one or more elements) - the path to an element of the source object, which value is to be compared with the expected one
  - "SearchTags" entry`s bound value is a flat dictionary of string keys and list of lists bound values, with each nested list being a path to an element of the source object
* (optionally) an element with the key "FixedTags" with the bound value as a flat dictionary or string keys and any JSON allowed types as the bound values

All required "Markers" must be present in the source object, e.g. the entry

```json
"Markers" : [
    ["a", "type"],
    ["b", "records", 5]
]
```

means that:

* the source object must have the top level element / attribute named "type", and its value must be "a"
* AND the source object must have the top level element "records", which can be treated as a sequence type, and its 6-th (sub-) element`s value must be "b"

The "Markers" are used for the selection of a logical group of the templates for the specific formats of the source data files. Their values are not directly used to form the search tags. When required, the specific search tags for this group can be added suing the "FixedTags" entry value.

Each entry in the "SearchTags" can define more than one path within the source object (all possible paths will be tested until a match is found or all paths are tried), but at least one path must be valid for each of the entries. For example, the entry:

```json
"SearchTags" : {
    "Version" : [["a", "b"], ["c"]],
    "Date" : ["d"]
}
```

means that:

* the source object must have the top level element / attribute "d", which value will be assigned to the search tag "Date"
* AND the source object must have
  - the top level element / attribute "a" with the sub-element / attribute "b", and the value of a->b will be assigned to the search tag "Version"
  - OR the top level element / attribute "c", which value will be assigned to the search tag "Version"

If more than one possible path is indicated, they are tried in the same order as defined. The first found path referencing an existing (nested) element within the source object is used to extract the value to be assigned to the corresponding search tag.

If the source object contains all required elements ("Markers" and at least one existing path for each "SearchTags" element) a search pattern is formed using all entries from the "SearchTags" - tag name : extracted value pairs. If the entry "FixedTags" is present, all key : value pairs from it are added into the search pattern dictionary. The special entries "Type" : "XML" or "Type" : "JSON" are added automatically, depending on which parser class - JSON_Parser or XML_Parser - is used.

The entries in the **index.json** file are checked against the formed search pattern dictionary in the same order, as they are defined. The first entry, which has all the key : value pairs from the search pattern dictionary is selected, and the corresponding template file is loaded.

For instance, a "SuperTester" software generates report files in the XML format. The internal structure of the report changes between the releases of the software, therefore, different parsing templates are requried. Suppose, that tag (name) of the root element is the same, for instance, "test_report", and it always has an attribute "version", which reflects the software release. In this case the proper template can be chosen on the following checks:

* the source file is of XML format (automatically during the parser selection)
* the root element is "test_report" (tag)
* the root element has the attribute "version"
* the value of this attribute

The template for the version 1 of the software report is stored in the file "template1.json", and for the version 2 - in the file "template2.json". The both templates are logically grouped as belonging to the "SuperTester" software data processing. Thus, the possible entries in the **index.json** file can be:

```json
    ...
    {
        "Type" : "XML",
        "Software" : "SuperTester",
        "Version" : 1,
        "BaseName" : "template1.json"
    },
    {
        "Type" : "XML",
        "Software" : "SuperTester",
        "Version" : 2,
        "BaseName" : "template2.json"
    }
    ...
```

The both entries in the index file can be matched by a single entry in the search index file:

```json
    ...
    {
    "FixedTags" : {
        "Software" : "SuperTester"
        },
    "Markers" : [
        ["test_report", "tag"]
        ],
    "SearchTags" : {
        "Version" : [["version"]]
    }
    }
    ...
```

Thus, when an XML file with the root element 'test_report' is processed, and this root element has the attribute "version", the proper template can be automatically selected based on the value of that attribute:

* "version"="1" -> template1.json
* "version"="2" -> template2.json

Note, that the quoted numbers as the values of the attributes are automatically converted into Python numeric types.

## Use Example

The test case used within the UT004 unit testing suite. An XML and a JSON files contain the nested structure data:

**dummy.xml**

```xml
<dummy>
    <node id="1" type="dummy">
        <test result="FAIL" value = "0" />
        <test result="PASS" value = "1" />
    </node>
</dummy>
```

**dummy.json**

```json
{
"dummy" : {
    "id" :" 1",
    "type" : "dummy",
    "tests" : [
        {"result" : "FAIL", "value" : 0},
        {"result" : "PASS", "value" : 1}
    ]
    }
}
```

In the both cases the data to be extracted is the values of:

* "id"
* "type"
* "value" of the element, which also contains the "PASS" value of the "result"

These three values are to be assigned to:

* TestObject.report["id"]
* TestObject.report["type"]
* TestObject.result

where *TestObject* is an instance of the *HelperClass* class.

**HelperClass** - defined in the file *fsio_lib/Tests/ut004_helper_class.py*

```python
class HelperClass(object):
    def __init__(self):
        self.report = {"id" : None, "type" : None}
        self.result = None
```

The file parsing templates are defined in the following files:

**xml_test.json** - in the folder *Templates/XML*

```json
{
    "Type" : "XML",
    "Software" : "UnitTest",
    "TargetClassModule" : "fsio_lib.Tests.ut004_helper_class",
    "TargetClass" : "HelperClass",
    "DataMapping" : {
        "report" : {
            "id" : "node.id",
            "type" : "node.type"
        },
        "result" : ["node", {"result" : "PASS"}, "value"]
    }
}
```

**json_test.json** - in the folder *Templates/JSON*

```json
{
    "Type" : "JSON",
    "Software" : "UnitTest",
    "TargetClassModule" : "fsio_lib.Tests.ut004_helper_class",
    "TargetClass" : "HelperClass",
    "DataMapping" : {
        "report" : {
            "id" : "dummy.id",
            "type" : "dummy.type"
        },
        "result" : ["dummy.tests", {"result" : "PASS"}, "value"]
    }
}
```

These two templates are registered in the templates` index as:

**index.json** - in the folder *Templates*

```json
[
    {
        "Type" : "XML",
        "Software" : "UnitTest",
        "Mode" : "dummy",
        "BaseName" : "xml_test.json"
    },
    {
        "Type" : "JSON",
        "Software" : "UnitTest",
        "Mode" : "dummy",
        "BaseName" : "json_test.json"
    }
]
```

Finally, the search index patterns are defined in order to ensure that the template "xml_test.json" is automatically chosen during the parsing of the "dummy.xml" data file (or of the compatible structure), and "json_test.json" - for the "dummy.json".

**xml_search_index.json** - in the folder *Templates*

```json
[
{
    "FixedTags" : {
        "Software" : "UnitTest"
        },
    "Markers" : [
        ["dummy", "tag"]
        ],
    "SearchTags" : {
        "Mode" : [["node.type"]]
    }
}
]
```

This search index pattern requires that:

* the XML object` root element is "dummy" (the value of its tag)
* the XML object has a sub-element "node" (its tag) with an attribute "type", since it is the only one search path provided, which value will be assigned to the search key "Mode"

Hence, in the case of the data file "dummy.xml", which is supposed to be parsed with help of the class XML_Parser, the formed search index entries are:

```python
{
    "Software" : "UnitTest",
    "Mode" : "dummy",
    "Type" : "XML"
}
```

Apparently, this search pattern matches the first entry in the **index.json**, with the value of the "BaseName" key is "xml_test.json".

**json_search_index.json** - in the folder *Templates*

```json
[
{
    "FixedTags" : {
        "Software" : "UnitTest"
        },
    "Markers" : [
        ["dummy", "dummy.type"]
        ],
    "SearchTags" : {
        "Mode" : [["dummy.type"]]
    }
}
]
```

This search index pattern requires that:

* the JSON object to be parsed is a dictionary
* it has the top level key "dummy"
* the value bound to this top level key is itself a dictionary, which has a key "type", since it is the only one search path provided, which value will be assigned to the search key "Mode"

Hence, in the case of the data file "dummy.json", which is supposed to be parsed with help of the class JSON_Parser, the formed search index entries are:

```python
{
    "Software" : "UnitTest",
    "Mode" : "dummy",
    "Type" : "JSON"
}
```

Obviously, this search pattern matches the second entry in the **index.json**, with the value of the "BaseName" key is "json_test.json".

With these arrangements, the data files "dummy.xml" and "dummy.json" can be parsed with the automatic determination of the required parsing templates, which, in turn, determine the required target class:

**example.py**

```python
from fsio_lib.GenericParsers import parseFile

objTest1 = parseFile("dummy.xml")[0] # -> HelperClass instance

objTest2 = parseFile("dummy.json")[0] # -> HelperClass instance
```