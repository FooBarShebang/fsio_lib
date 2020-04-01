# Library fsio_lib

## Table of Content

* [Goal](#Goal)
* [Installation](#Installation)
* [Structure and Functionality](#Structure-and-Functionality)
* [Documentation](#Documentation)

## Goal

This library implements common functionality for the data processing, mostly concerning the files collections synchronization and batch operations, work flow automation and structured data files reading and writing. All implemented functionality is generic without concerns about specifics of proprietary or highly specialized file formats or details of the actual data processing.

Concerning the files collections synchronization specifically and general files operations the following functionality is provided:

* Files collection maintenance and synchronization (see module *fs_maintenace*)
  * Safe and smart files copying without data duplication:
    * The file from 'source' is not copied if there is an identical file in the 'target'
    * The file from 'source' is copied into the 'target' preserving the base filename and date-time stamps when 'target' does not contain an identical file
    * The file from 'source' is copied into the 'target' preservig the date-time stamps but under a different base filename if there already exists a file with the same base filename but different md5 check-sum in the 'target' folder
  * Folder's name conflict resolution by automated merging of their content
  * Pulling of the new, not yet present data (files) into the 'root' of the 'master' from the 'slave' reagardless of its location in the 'slave' - all its nested sub-folders are iterated through
  * Unification of the internal structure of a folder by renaming and merging of its sub-folders and removal of the 'dead', empty branches
  * Removal of the duplicated *identical* files located in the different sub-folders
  * Removal of unwanted copies of the same file in the same (sub-) folder - same md5 check-sums but different base filenames
* Interception of the exception raised during files and folders operations - this approach allows continuous, not interrupted batch processing even if permissions or names conflict occurs (see module *LoggingFSIO*). All errors are still reported and logged.
* Locale independed processing of 'bad' format text files - non-POSIX line end conventions, digital dot / comma conventions, etc. - see module *locale_fsio*
* Parsing of the tabulated data (TSV, CSV, etc.) or structured data text files (XML, JSON, etc.) using templates for the data extraction, including automated detection of the input file structure and selection of the required template and parser object (see module *GenericParsers*)

Concerning the batch data processing (see module *DataProviders*) the goal is to provide a common, uniform API for the (batch) files I/O and frameworks for the work flow creations, into which the actual file parsers (structure aware) and data processing methods can be simply plugged-in. In turn, it expects certain API uniformity from such external methods.

## Installation

Clone the official repository into your local workspace / project folder:

```bash
$ git clone <repository_path> "your project folder"
```

Initialize the UML templates submodule

```bash
$ cd "your project folder"/fsio_lib/Documentation/UML/Templates
$ git submodule init
```

Download the content of the UML templates submodule

```bash
$ git submodule update --recursive --remote
```

**Note**: You do not have to intialize and download the UML templates submodule if you do not plan to update the library's documentation. They are not required for the functionality of the library iteself. 

## Structure and Functionality

### Module StructureMapping

Implements functions for mapping the content of a nested C struct (or Pascal record) like objects, nested dictionaries, nested sequences or even XML representation objects (xml.etree.ElementTree.Element class) onto another object of one of these types using defined templates.

### Module dynamic_import

Implements functions to import modules or objects from modules dynamically, i.e. using their string names at the runtime.

### LoggingFSIO

Implements 'safe/smart' copy / move / rename / delete file operations, which intercept OS and I/O related exceptions raised during operations, which are logged into console and / or file and returned as the result of an operation.

### Module locale_fsio

Implements functions for locale independent writing of tabulated data ASCII text files (TSV format) concerning the new line, decimal separator and delimiter conventions as well as use of usual spaces instead of TABs for the columns separation. Also implements function, which forces specific new line convention.

### Module fs_maintenance

Implements a number of functions for the maintenance of a file system, including recursive removal of the duplicating files, recursive folder's renaming, recursive deletion of empty sub-folders, pulling of the non-present files from another folder, etc.

### GenericParsers

Implements singleton classes for parsing TSV, XML and JSON files with the data mapping onto specified class instances using the specified templates. Also defines generic parsing functions, which automatically select the required parsing class.

### Module DataProviders

Implements classes for batch processing of the data files. Note that only the generic mechanics of the files selections and grouping as well as the data processing work flow is concerned. The actual files parsing / data processing mechanisms are to be implemented elsewhere and plugged-in (passing by reference) into the corresponding methods.

### Structure of the Library

![Library Structure](./Documentation/UML/fsio_lib_components.png)

## Documentation

All documentation can be found in the *Documentation* folder (see [Index](./Documentation/index.md)), and it is written using Markdown format.

* [Requirements](./Documentation/Requirements/index.md)
* [Design](./Documentation/Design/index.md)
* [Testing](./Documentation/Testing/index.md)
* [User and API References](./Documentation/References/index.md)
