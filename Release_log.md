# Release Log of Library fsio_lib

## 2020-04-01 Version 0.2.1-rc1

Properly documented and tested: requirements, unit testing modules, test reports, user and API references

## 2020-03-10 Version 0.2.1-dev1

Added folders structure copy / merge functionality to the module 'fs_maintenance'.

## 2020-03-10 Version 0.2.0-dev1

Added module 'fs_maintenance' - file system maintenance, synchronization and cleaning-up tasks.

## 2020-01-22 Version 0.1.1-dev1

Migrted to GitLab.

## 2019-02-08 Version 0.1.0.5

Re-organized the UML templates (for the documnetation only) into a Git submodule. Updated UML diagram source files accordingly.

## 2018-11-15 Version 0.1.0.5

Fixed the automatic template look-up by the file structure in **GenericParsers.JSON_Parser._getHints()**:

* condition on the presence of all keys from the search pattern dictionary in the index dictionary
* the template is now loaded with StructureMapping.LoadDefinition() function instead of json.load() -> fixes the path and value substitution

Added "$" characters replacement by "%" in the source data file (not templates!) in **GenericParsers.JSON_Parser._loadFile**().

Fixed the path substitutions resolution in **StructureMapping.resolvePathSubstitutions()** - only strings in the paths are now looked up among the already resolved path substitutions.

Added templates for the JSON and XML reports for EndTest performed by HPS v2.0.2-2 on MFR devices and the corresponding search indexes.

## 2018-11-13 Version 0.1.0.4

Templates for the measurement data retrieval using libhps.hps_cli.js tool.

## 2018-11-09 Version 0.1.0.4

Finished documentation on the library.

## 2018-11-06 Version 0.1.0.4

Re-implemented and tested module GenericParsers.

## 2018-11-01 Version 0.1.0.3

Ported and tested modules dynamic_import and locale_fsio from other projects.

## 2018-10-31 Version 0.1.0.2

Finished re-factoring and testing of StructureMapping module.

## 2018-10-26 Version 0.1.0.1

Fixed improper resolution of the caller by the loggers with the level >= WARNING. Re-factoring StructureMapping module.

## 2018-10-18 Version 0.1.0.0

Changed the versionning scheme to Major.Minor.Patch.Build. Re-factored the LoggingFSIO module - concerning the loggers and logging I/O operations.

## 2018-06-07 Version 0.6.20180607

Stable and tested TSV and JSON parsing concerning HPS versions 0.3.6.4 and v2 / CFR rev C, rev D and rev 1.

Stable and tested structured objects mapping using templates.

Stable and tested double logging.

Stable and tested automated work flow management.

## 2018-05-29

Added LoggingFSIO.py module - smart file operations with logging

## 2018-04-17

Name-space re-factoring

## 2018-04-13

Implemented generic, JSON and TSV parsers based on the templates for data mapping - module GenericParsers.py

## 2018-04-12

Implemented structured objects mapping using templates - module StructuredMapping.py

## 2017-10-16

Implemented automated work flow management - module DataProviders.py

## 2017-10-12

Started implementation of the library.
