#!/usr/bin/python
"""
Package fsio_lib

Library implementing common functionality for the data processing, mostly
concerning the batch operations, work flow automatization and structured data
files reading and writing. All implemented functionality is generic without
concerns about specifics of proprietary or highly specialized file formats or
details of the actual data processing. The goal is to provide a common, uniform
API for the (batch) files I/O. 

Modules:
    StructureMapping: implements functions for walking nested C struct (or
        Pascal record) like objects or nested dictionaries objects (like
        os.walk() in terms of the directories structure) mapping (copying
        values) from one such object into another of a different structure using
        defined templates.
    GenericParsers:  implements singleton classes for parsing TSV, XML and JSON
        files with the data mapping onto specified class instances using the
        specified templates. These classes are based on the
        fsio_lib.StructureMapping.MapValues() function.
    LoggingFSIO: implements 'safe/smart' copy / move / rename / delete file
        operations, which intercept OS and I/O related exceptions raised during
        operations, which are logged into console and / or file and returned as
        the result of an operation.
    locale_fsio: implements functions for locale independent writing of
        tabulated data ASCII text files (TSV format) concerning the new line,
        decimal separator and delimiter conventions as well as use of usual
        spaces instead of TABs for the columns separation. Also implements
        function, which forces specific new line convention.
    dynamic_import: implements functions to import modules or objects from
        modules dynamically, i.e. using their string names at the runtime.
"""

__author__ = "Anton Azarov"
__license__ = "GPL"
__version__ = "0.1.1.0"
__date__ = "15-11-2018"
__status__ = "Production"
__maintainer__ = "anton.v.azarov@gmail.com"

__all__ = ['StructureMapping', 'GenericParsers', 'LoggingFSIO', 'locale_fsio',
            'dynamic_import']