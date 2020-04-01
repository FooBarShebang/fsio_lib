#!/usr/bin/python
"""
Package fsio_lib

Library implementing common functionality for the data processing, mostly
concerning the batch operations, work flow automatization and structured data
files reading and writing. All implemented functionality is generic without
concerns about specifics of proprietary or highly specialized file formats or
details of the actual data processing. The goal is to provide a common, uniform
API for the (batch) files I/O and frameworks for the work flow creations, into
which the actual file parsers (structure aware) and data processing methods can
be simply plugged-in. In turn, it expects certain API uniformity from such
external methods. 

Modules:
    StructureMapping: implements functions for walking nested C struct (or
        Pascal record) like objects or nested dictionaries objects (like
        os.walk() in terms of the directories structure) mapping (copying
        values) from one such object into another of a different structure using
        defined templates.
    dynamic_import: implements functions to import modules or objects from
        modules dynamically, i.e. using their string names at the runtime.
    LoggingFSIO: implements 'safe/smart' copy / move / rename / delete file
        operations, which intercept OS and I/O related exceptions raised during
        operations, which are logged into console and / or file and returned as
        the result of an operation.
    locale_fsio: implements functions for locale independent writing of
        tabulated data ASCII text files (TSV format) concerning the new line,
        decimal separator and delimiter conventions as well as use of usual
        spaces instead of TABs for the columns separation. Also implements
        function, which forces specific new line convention.
    fs_maintenance: implements a number of functions for the maintenance of a
        file system, including recursive removal of the duplicating files,
        recursive folder's renaming, recursive deletion of empty sub-folders,
        pulling of the non-present files from another folder, etc.
    GenericParsers:  implements singleton classes for parsing TSV, XML and JSON
        files with the data mapping onto specified class instances using the
        specified templates. These classes are based on the
        fsio_lib.StructureMapping.MapValues() function.
"""

__project__ = 'Python framework for the structured and TSV files parcing'
__version_info__= (0, 2, 1)
__version_suffix__= '-rc1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '01-04-2020'
__status__ = 'Production'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['StructureMapping', 'GenericParsers', 'LoggingFSIO',
            'locale_fsio', 'dynamic_import', 'fs_maintenance']