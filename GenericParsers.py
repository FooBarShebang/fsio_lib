#!/usr/bin/python
"""
Module fsio_lib.GenericParsers

Implements singleton classes for parsing TSV, XML and JSON files with the data
mapping onto specified class instances using the specified templates. The
operation of these classes is based on the fsio_lib.StructureMapping.MapValues()
function. Please, consult with the documentation on that function.

Classes:
    Generic_Parser
    TSV_Parser
    JSON_Parser
    XML_Parser

Functions:
    parseFile()
        str/, class A, dict, logging.Logger OR `LoggingFSIO.ConsoleLogger,
            bool OR None, bool, bool/ -> list(type A)
    parseManyFiles()
        str, list(str)/, class A, dict
            logging.Logger OR `LoggingFSIO.ConsoleLogger, bool OR None, bool,
                bool/ -> collections.OrderedDict(str : list(type A))
"""

__version__ = "0.1.0.2"
__date__ = "15-11-2018"
__status__ = "Production"

#imports

#+ standard libraries

import os
import sys
import collections
import json
import xml.etree.ElementTree as ElementTree

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from fsio_lib.StructureMapping import MapValues, FlattenPath, GetElement
from fsio_lib.StructureMapping import LoadDefinition
from fsio_lib.dynamic_import import import_from_module
from locale_fsio import LoadTable

#globals

TEMPLATES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                    'Templates')

#+ look-up tables

with open(os.path.join(TEMPLATES_FOLDER, 'json_search_index.json'), 'rt') as FF:
    JSON_INDEX = json.load(FF)

with open(os.path.join(TEMPLATES_FOLDER, 'xml_search_index.json'), 'rt') as FF:
    XML_INDEX = json.load(FF)

with open(os.path.join(TEMPLATES_FOLDER, 'index.json'), 'rt') as FF:
    TEMPLATES_INDEX = json.load(FF)

#classes

class GenericParser(object):
    """
    Prototype singleton class for parsing data files.
    
    It is designed such that any derived class MUST re-define the helper class
    method _loadFile(), which is responsible for the actual parsing. It must be
    able to accept 2 arguments, first being the path to a file and the second
    - the dictionary containing the parsing hints. It must return a list of
    objects, which can be directly used as the source objects for the mapping by
    the class method parseSingleObject().
    
    The derived classes are also encouraged to define their own helper class
    method _getHints(), which can extract the file loading hints, e.g. the
    length of the header, from the file parsing template as well as the
    suggested target object class; it may also suggest the proper file parsing
    template based on the file`s content.
    
    The rest of the functionality can be simply inherited without any changes.
    
    Methods:
        parseSingleObject()
            type A, class B, dict/,
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool, bool, bool / -> type B
        parseFile()
            logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/ -> list(type A)
        parseManyFiles()
            str, list(str)/, class A, dict
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/
                        -> collections.OrderedDict(str : list(type A))
    
    Version 0.1.0.0
    """
    
    #'private' class methods
    
    @classmethod
    def _loadFile(cls, strFile, dictHints, objLogger = None):
        """
        Prototype for the helper class method for the actual parsing of the data
        files.
        
        The derived classes MUST define their own version of this helper method.
        The returned list should contain individual objects (e.g., TSV file
        lines, JSON objects, etc.), each being ready for parsing with the class
        method parseSingleObject() using a template. They are expected to
        preserve the signature.
        
        Signature:
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(type A)
        
        Args:
            strFile: str, the path to a file to process
            dictHints: dict, dictionary of hints for processing of the file, if
                such are extracted from the mapping template
            objLogger: logging.Logger OR `LoggingFSIO.ConsoleLogger, instance of
                as a logger object with the standard API
        
        Returns:
            list(type A): list of individual objects extracted from the file
        
        Version 0.1.0.0
        """
        return []
    
    @classmethod
    def _getHints(cls, objData, dictTemplate = None):
        """
        Prototype for the helper method to get the parsing hints.
        
        The derived classes MAY define their own variant, which MUST preserve
        the signature. The overridden method is advised to suggest the file
        loading hints, e.g. the length of the header, from the file parsing
        template as well as the target object class; it may also suggest the
        proper file parsing template based on the file`s content.
        
        This prototype is able only to get HeaderOffset value from the provided
        file parsing template and dynamically load the target object class.
        
        Signature:
            type A/, dict/ -> dict
        
        Args:
            objData: type A, a single data element extracted from a file
            dictTemplate: (optional) dict, the file parsing template
        
        Returns:
            dict: the hints dictionary
        
        Raises:
            ValueError: objData is None and dictTemplate is None - no data to
                process
        
        Version 0.1.0.0
        """
        if (objData is None) and (dictTemplate is None):
            strError = 'Neither data object nor template are provided'
            raise ValueError(strError)
        dictHints = {}
        if not (dictTemplate is None):
            cls._checkTemplate(dictTemplate)
            dictHints["Template"] = dictTemplate
            dictHints["HeaderOffset"] = dictTemplate.get("HeaderOffset", None)
            strTargetClassModule = dictTemplate.get("TargetClassModule", None)
            strTargetClass = dictTemplate.get("TargetClass", None)
            bCond1 = not (strTargetClassModule is None)
            bCond2 = not (strTargetClass is None)
            if bCond1 and bCond2:
                dictGlobals = globals()
                if not (strTargetClass in dictGlobals):
                    clsTarget = import_from_module(strTargetClassModule,
                                    strTargetClass, dictGlobals = dictGlobals)
                else:
                    clsTarget = dictGlobals[strTargetClass]
                dictHints["TargetClass"] = clsTarget
        return dictHints
    
    @classmethod
    def _checkFile(cls, strFile):
        """
        Helper method.
        
        Checks if the passed argument is a valid full path (absolute or relative
        to the current working directory) to a file. Two checks are performed:
            1) if the argument is a string
            2) if it is indeed a path to an existing file, see os.path.isfile()
        
        Signature:
            str -> None
        
        Args:
            strFile: str, the path to a file to checked for existance
        
        Raises:
            TypeError: the passed argument is not a string
            ValueError: the passed argument is not a path to an existing file
        
        Version 0.1.0.0
        """
        if not isinstance(strFile, basestring):
            strError="Wrong type of the argument for the source file {}".format(
                                                                type(strFile))
            strError = "{}, must be a string".format(strError)
            raise TypeError(strError)
        if not os.path.isfile(strFile):
            strError = "{} is not a path to a file".format(strFile)
            raise ValueError(strError)
    
    @classmethod
    def _checkTemplate(cls, dictTemplate):
        """
        Helper method.
        
        Checks if the passed argument is a valid data file processing template.
        Three checks are performed:
            1) if the argument is a mapping type
            2) if it has the top level key 'DataMapping'
            3) if that key has a dictionary as its value
        
        Signature:
            dict -> None
        
        Args:
            dictTemplate: dict, the mapping rules and parser hints dictionary
        
        Raises:
            TypeError: the passed argument is not a dictionary
            ValueError: the passed argument has no key 'DataMapping' or the
                value bound to it is not a dictionary
        
        Version 0.1.0.0
        """
        if not isinstance(dictTemplate, collections.Mapping):
            strError = "Wrong type of the argument for the template {}".format(
                                                            type(dictTemplate))
            strError = "{}, must be a dictionary".format(strError)
            raise TypeError(strError)
        if not ('DataMapping' in dictTemplate.keys()):
            strError="Missing 'DataMapping' entry in the template"
            raise ValueError(strError)
        if not isinstance(dictTemplate['DataMapping'], collections.Mapping):
            strError="'DataMapping' entry's value is not a dictionary "
            raise ValueError(strError)
    
    #public class methods
    
    @classmethod
    def parseSingleObject(cls, gSource, clsTarget, dictTemplate,
                                objLogger = None, bStrictTarget = True,
                                    bStrictSource = True, bForceTarget = False):
        """
        Maps the data from the source object onto a new instance of the target
        class using the mapping rules specified by the data file processing
        template.
        
        Wraps function fsio_lib.StructureMapping.MapValues().
        
        Signature:
            type A, class B, dict/,
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool, bool, bool / -> type B
        
        Args:
            gSource: type A, data source object, from which the data must be
                extracted
            clsTarget: class B, class onto instances of which the extracted from
                a file data must be mapped
            dictTemplate: dict, file parsing template, must contain the top
                level key 'DataMapping' with the mapping rules dictionary as its
                value
            objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
                instance of, the logger object, by default is None (not
                provided)
            bStrictTarget: (optional) bool, flag if the target object MUST have
                all expected elements, default value is True
            bStrictSource: (optional) bool, flag if the source object MUST have
                all expected elements, default value is True
            bForceTarget: (optional) bool, flag is the missing elements / paths
                are to be created in the target object, has an effect only if
                the value of bStrictTarget is False, the default value for
                bForceTarget False
        
        Returns:
            type B: an instance of the target class
        
        Raises:
            TypeError: wrong mapping dictionary format or missmatch between the
                structure of the target and source objects and the mapping rules
            ValueError: wrong mapping dictionary format or missmatch between the
                structure of the target and source objects and the mapping rules
                or the template has no key 'DataMapping' or the value bound to
                it is not a dictionary
            AttributeError: missing element of the target or source object if
                the corresponding flags are set to True, or an immutable element
                in the target object
        
        Version 0.1.0.0
        """
        try:
            cls._checkTemplate(dictTemplate)
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        objTarget = clsTarget()
        try:
            MapValues(objTarget, gSource, dictTemplate['DataMapping'],
                objLogger = objLogger, bStrictTarget = bStrictTarget,
                    bStrictSource = bStrictSource, bForceTarget = bForceTarget)
            if not (objLogger is None):
                strMessage = 'Mapped {} onto {}'.format(gSource, objTarget)
                objLogger.info(strMessage)
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='Exception re-raised'
                objLogger.error(strMessage)
            raise
        return objTarget
    
    @classmethod
    def parseFile(cls, strFile, clsTarget = None, dictTemplate = None,
                                objLogger = None, bStrictTarget = None,
                                    bStrictSource = True, bForceTarget = False):
        """
        Parses a single data file according to the specified template and
        returns a list of instances of the target class.
        
        Work flow:
            1) checks the path to the file - _checkFile() method
            2) gets file loading and parsing hints only by the parsing template
                using _getHints(None, dictTemplate)
            3) parses the file into a list of source data objects - _loadFile()
            4) gets file loading and parsing hints by the file content and the
                parsing template using _getHints(Data, dictTemplate)
            5) updates the mapping rules and parameters, if required
            6) maps the data from each source object onto a new instance (1:1)
                of the target class
            7) returns the resulting list
        
        If the target class is not specified, the suggested target class is
        taken from the file processing template - if this is not possible the
        ValueError is raised.
        
        If the file processing template is not provided, it should be determined
        by the content of the file to be processed - if this is not possible the
        ValueError is raised.
        
        Signature:
            str/, class A, dict,
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/ -> list(type A)
        
        Args:
            strFile: str, full path to the data file to be parsed
            clsTarget: (optional) class A, class onto instances of which the
                extracted from a file data must be mapped
            dictTemplate: (optional) dict, file parsing template, must contain
                the top level key 'DataMapping' with the mapping rules
                dictionary as its value
            objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
                instance of, the logger object, by default is None (not
                provided)
            bStrictTarget: (optional) bool OR None, flag if the target object
                MUST have all expected elements, default value is None, meaning
                that the parser decides itself
            bStrictSource: (optional) bool, flag if the source object MUST have
                all expected elements, default value is True
            bForceTarget: (optional) bool, flag is the missing elements / paths
                are to be created in the target object, has an effect only if
                the value of bStrictTarget is False, the default value for
                bForceTarget False
        
        Returns:
            list(type A): a list of an instances of the target class
        
        Raises:
            TypeError: wrong mapping dictionary format or missmatch between the
                structure of the target and source objects and the mapping rules
                or the path to a file is not a string
            ValueError: wrong mapping dictionary format or missmatch between the
                structure of the target and source objects and the mapping rules
                or the template has no key 'DataMapping' or the value bound to
                it is not a dictionary; or the file path does not reference an
                existing file
            AttributeError: missing element of the target or source object if
                the corresponding flags are set to True, or an immutable element
                in the target object
        
        Version 0.1.0.0
        """
        try:
            cls._checkFile(strFile)
            dictHints = cls._getHints(None, dictTemplate = dictTemplate)
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        if not (objLogger is None):
            strMessage = 'Loading file {}'.format(strFile)
            objLogger.info(strMessage)
        lstEntries = cls._loadFile(strFile, dictHints, objLogger = objLogger)
        if not len(lstEntries):
            strMessage = 'File {} is empty - nothing is loaded'.format(strFile)
            if not (objLogger is None):
                objLogger.info(strMessage)
            return []
        try:
            dictHints =cls._getHints(lstEntries[0], dictTemplate = dictTemplate)
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        _clsTarget = dictHints.get("TargetClass", None)
        _dictTemplate = dictHints.get("Template", None)
        if clsTarget is None:
            if _clsTarget is None:
                strError ='Target class is not specified and can not be guessed'
                if not (objLogger is None):
                    strMessage = 'ValueError: {}'.format(strError)
                    objLogger.error(strError)
                raise ValueError(strError)
            if bStrictTarget is None:
                _bStrictTarget = True
            else:
                _bStrictTarget = bStrictTarget
        else:
            if (_clsTarget is None) and (bStrictTarget is None):
                _bStrictTarget = True
            elif (not (clsTarget is _clsTarget)) and (bStrictTarget is None):
                _bStrictTarget = False
            elif bStrictTarget is None:
                _bStrictTarget = True
            else:
                _bStrictTarget = bStrictTarget
            _clsTarget = clsTarget
        if dictTemplate is None:
            if _dictTemplate is None:
                strError = 'Template is not specified and can not be guessed'
                if not (objLogger is None):
                    strMessage = 'ValueError: {}'.format(strError)
                    objLogger.error(strError)
                raise ValueError(strError)
        else:
            _dictTemplate = dictTemplate
        lstResult = [cls.parseSingleObject(Entry, _clsTarget, _dictTemplate,
                objLogger = objLogger, bStrictTarget = _bStrictTarget,
                    bStrictSource = bStrictSource, bForceTarget = bForceTarget)
                                                        for Entry in lstEntries]
        return lstResult
    
    @classmethod
    def parseManyFiles(cls, strFolder, strlstFiles, clsTarget = None,
                dictTemplate = None, objLogger = None, bStrictTarget = None,
                                    bStrictSource = True, bForceTarget = False):
        """
        Parses data from several specified data files within a single specified
        directory according to the specified template and returns an ordered
        dictionary of the base file names as keys and lists of instances of the
        target class as values.
        
        Work flow:
            1) check that the specified folder exists
            2) create an empty instance of collections.OrderedDict
            3) for each file in the specified list
                3.1) parse this file - _parseFile() method
                3.2) store the base file name : returned list pair as an entry
                    in the ordered dictionary
            4) return this ordered dictionary
        
        If the target class is not specified, the suggested target class is
        taken from the file processing template - if this is not possible the
        ValueError is raised. Dynamically for each file.
        
        If the file processing template is not provided, it should be determined
        by the content of the file to be processed - if this is not possible the
        ValueError is raised. Dynamically for each file.
        
        Signature:
            str, list(str)/, class A, dict
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/
                        -> collections.OrderedDict(str : list(type A))
        
        Args:
            strFolder: str, path to a folder containing the data files
            strlstFiles: list(str), base names of the data files to parse
                within that folder
            clsTarget: (optional) class A, class onto instances of which the
                extracted from a file data must be mapped
            dictTemplate: (optional) dict, file parsing template, must contain
                the top level key 'DataMapping' with the mapping rules
                dictionary as its value
            objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
                instance of, the logger object, by default is None (not
                provided)
            bStrictTarget: (optional) bool OR None, flag if the target object
                MUST have all expected elements, default value is None, meaning
                that the parser decides itself
            bStrictSource: (optional) bool, flag if the source object MUST have
                all expected elements, default value is True
            bForceTarget: (optional) bool, flag is the missing elements / paths
                are to be created in the target object, has an effect only if
                the value of bStrictTarget is False, the default value for
                bForceTarget False
        
        Returns:
            collections.OrderedDict: an ordered dictionary of pairs of the base
                file names and lists of the objects containing the data
                extracted from the corresponding file
        
        Raises:
            TypeError: wrong mapping dictionary format or missmatch between the
                structure of the target and source objects and the mapping rules
                or the path to a foler is not a string or any file name is not
                a string, or the list of base names is not a sequence
            ValueError: wrong mapping dictionary format or missmatch between the
                structure of the target and source objects and the mapping rules
                or the template has no key 'DataMapping' or the value bound to
                it is not a dictionary; or the folder path does not reference an
                existing folder or any referenced file there is missing
            AttributeError: missing element of the target or source object if
                the corresponding flags are set to True, or an immutable element
                in the target object
        
        Version 0.1.0.0
        """
        if not isinstance(strFolder, basestring):
            strError="Wrong type of the source folder {} argument".format(
                                                                type(strFolder))
            strError = "{}, must be a string".format(strError)
            if not (objLogger is None):
                strMessage ='TypeError: {}'.format(strError)
                objLogger.error(strMessage)
            raise TypeError(strError)
        if ((not isinstance(strlstFiles, collections.Sequence))
                                        or isinstance(strlstFiles, basestring)):
            strError="Wrong type of the files list {} argument".format(
                                                            type(strlstFiles))
            strError ="{}, must be a sequence and not a string".format(strError)
            if not (objLogger is None):
                strMessage ='TypeError: {}'.format(strError)
                objLogger.error(strMessage)
            raise TypeError(strError)
        if not os.path.isdir(strFolder):
            strError = "{} is not a path to a folder".format(strFolder)
            if not (objLogger is None):
                strMessage ='ValueError: {}'.format(strError)
                objLogger.error(strMessage)
            raise ValueError(strError)
        dictResult = collections.OrderedDict()
        for strFile in strlstFiles:
            if not isinstance(strFile, basestring):
                strError= "Wrong type of the base file name {}".format(
                                                                type(strFile))
                strError = "{}, must be a string".format(strError)
                if not (objLogger is None):
                    strMessage ='TypeError: {}'.format(strError)
                    objLogger.error(strMessage)
                raise TypeError(strError)
            strFilename = os.path.join(strFolder, strFile)
            lstResults = cls.parseFile(strFilename, clsTarget, dictTemplate,
                objLogger = objLogger, bStrictTarget = bStrictTarget,
                    bStrictSource = bStrictSource, bForceTarget = bForceTarget)
            if len(lstResults):
                dictResult[strFile] = lstResults
        return dictResult

class TSV_Parser(GenericParser):
    """
    Specialized singleton class for parsing the TSV files. Derived from the
    prototype class Generic_Parser. Redefines the helper class method
        _loadFile()
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(list(str OR int OR float))
    
    Inherits all class methods of the super class.
    
    Methods:
        parseSingleObject()
            type A, class B, dict/,
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool, bool, bool / -> type B
        parseFile()
            logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/ -> list(type A)
        parseManyFiles()
            str, list(str)/, class A, dict
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/
                        -> collections.OrderedDict(str : list(type A))
    
    Version 0.1.0.0
    """
    
    #'private' class methods
    
    @classmethod
    def _loadFile(cls, strFile, dictHints, objLogger = None):
        """
        Helper class method for the actual parsing of a data file, which reads
        out all lines starting from the offset specified within the template by
        the top level key 'HeaderOffset'. If such entry is absent, all lines
        are read.
        
        Wraps the function fsio_lib.locale_fsio.LoadTable()
        
        Signature:
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(list(str OR int OR float))
        
        Args:
            strFile: str, the path to a file to process
            dictHints: dict, dictionary of hints for processing of the file, if
                such are extracted from the mapping template
            objLogger: logging.Logger OR `LoggingFSIO.ConsoleLogger, instance of
                as a logger object with the standard API
        
        Returns:
            list(list(str OR int OR float)): list of lists of individual objects
                extracted from the file (rows of columns)
        
        Version 0.1.0.0
        """
        if dictHints["HeaderOffset"] is None:
            iOffset = 0
        else:
            iOffset = dictHints["HeaderOffset"]
        try:
            lstResult = LoadTable(strFile, iSkipLines = iOffset)
        except (IOError, OSError) as Err:
            if not (objLogger is None):
                strMessage = '{}: {}'.format(Err.__class__.__name__,
                                                Err.errno, Err.strerror)
                objLogger.error(strMessage)
            raise
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        return lstResult

class JSON_Parser(GenericParser):
    """
    Specialized singleton class for parsing the JSON files. Derived from the
    prototype class Generic_Parser. Redefines the helper class methods
        _getHints()
            type A/, dict/ -> dict
        _loadFile()
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(type A)
    
    Note, that if the file parsing template is not provided, it is determined
    automatically based on the content of the already loaded data. If the
    proper template cannot be determined the ValueError exception is raised.
    
    Inherits all class methods of the super class.
    
    Methods:
        parseSingleObject()
            type A, class B, dict/,
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool, bool, bool / -> type B
        parseFile()
            logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/ -> list(type A)
        parseManyFiles()
            str, list(str)/, class A, dict
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/
                        -> collections.OrderedDict(str : list(type A))
    
    Version 0.1.0.0
    """
    
    #'private' class fields
    
    _TemplatesIndex = TEMPLATES_INDEX
    
    _SearchIndex = JSON_INDEX
    
    _Type = 'JSON'
    
    #'private' class methods
    
    @classmethod
    def _getHints(cls, objData, dictTemplate = None):
        """
        Specialized version of the 'private' helper method to get the file
        processing instructions from the template as well as to determine them
        when possible by the content of the data file itself.
        
        Signature:
            type A/, dict/ -> dict
        
        Args:
            objData: type A, a single data element extracted from a file
            dictTemplate: (optional) dict, the file parsing template
        
        Returns:
            dict: the hints dictionary
        
        Version 0.1.0.0
        """
        bCond1 = not (objData is None)
        bCond2 = not (dictTemplate is None)
        if bCond1 or bCond2:
            dictHints = GenericParser._getHints(objData,
                                                    dictTemplate = dictTemplate)
        else:
            dictHints = {}
        if bCond1 and (not bCond2):
            dictSearchRequired = dict()
            for dictOption in cls._SearchIndex:
                bFound = True
                #check mandatory elements - markers
                lstMarkers = dictOption.get("Markers", [])
                for lstMarkerOption in lstMarkers:
                    gControlValue = lstMarkerOption[0]
                    lstPath = FlattenPath(lstMarkerOption[1:])
                    try:
                        gValue = GetElement(objData, lstPath)
                        bFound = (gValue == gControlValue)
                    except AttributeError:
                        bFound = False
                    if not bFound:
                        break
                if not bFound:
                    continue
                #check the existance and get the values of the search elements
                dictSearchTags = dictOption.get("SearchTags", {})
                for strTag, lstlstPaths in dictSearchTags.items():
                    bFoundPath = True
                    for lstPath in lstlstPaths:
                        _lstPath = FlattenPath(lstPath)
                        try:
                            gValue = GetElement(objData, _lstPath)
                            bFoundPath = True
                        except AttributeError:
                            bFoundPath = False
                        if bFoundPath:
                            dictSearchRequired[strTag] = gValue
                            break
                    if not bFoundPath:
                        break
                if not bFoundPath:
                    continue
                #add mandatory elements
                dictFixedTags = dictOption.get("FixedTags", {})
                for strTag, gValue in dictFixedTags.items():
                    dictSearchRequired[strTag] = gValue
                dictSearchRequired["Type"] = cls._Type
                break
            if len(dictSearchRequired):
                for dictOption in cls._TemplatesIndex:
                    lstTags = dictSearchRequired.keys()
                    bCond1 = all(map(lambda x: x in dictOption, lstTags))
                    if bCond1:
                        bCond2 = all(map(
                            lambda x: dictOption[x] == dictSearchRequired[x],
                                lstTags))
                        if bCond2:
                            strTemplateFile = os.path.join(TEMPLATES_FOLDER,
                                            cls._Type, dictOption["BaseName"])
                            _dictTemplate = LoadDefinition(strTemplateFile)
                            dictHints = GenericParser._getHints(None,
                                                dictTemplate = _dictTemplate)
                            break
        return dictHints
    
    @classmethod
    def _loadFile(cls, strFile, dictHints, objLogger = None):
        """
        Helper class method for the actual parsing of JSON data file.
        
        Parses a text file containing a single or multiple JSON objects and
        returns a list of JSON objects representing the parsed data. Can handle
        the proper multiple JSON objects file (stored as an array of objects)
        as well as simple concatenation of multiple proper JSON file each
        containing a single object.
        
        Signature:
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(type A)
        
        Args:
            strFile: str, the path to a file to process
            dictHints: dict, dictionary of hints for processing of the file, if
                such are extracted from the mapping template
            objLogger: logging.Logger OR `LoggingFSIO.ConsoleLogger, instance of
                as a logger object with the standard API
        
        Returns:
            list(type A): list of individual objects extracted from the file
        
        Raises:
            ValueError: the content of the file cannot be spit properly into
                separate JSON objects. Note that in the case of CFR / MFR
                measurements data each of the returned objects in the list is a
                nested dictionary.
        
        Version 0.1.0.0
        """
        try:
            with open(strFile, 'rt') as fFile:
                strBuffer = fFile.read()
            strBuffer = strBuffer.replace("$", "%") #walk-around for "$" keys in
            # the calibration JSON files
        except (IOError, OSError) as Err:
            if not (objLogger is None):
                strMessage = '{}: {}'.format(Err.__class__.__name__,
                                                Err.errno, Err.strerror)
                objLogger.error(strMessage)
            raise
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        ituplstTemp = list()
        iCount = 0
        for iIdx, strChar in enumerate(strBuffer):
            if str(strChar) == '{':
                if not iCount:
                    iStart = iIdx
                iCount += 1
            elif str(strChar) == '}':
                if iCount <= 0:
                    strError = "Wrong file structure - not JSON in {}".format(
                                                                        strFile)
                    if not (objLogger is None):
                        strMessage = 'ValueError: {}'.format(strError)
                        objLogger.error(strMessage)
                    raise ValueError(strError)
                iCount -= 1
                if not iCount:
                    ituplstTemp.append((iStart, iIdx))
        dictlstResult = list()
        try:
            for itupPos in ituplstTemp:
                dictlstResult.append(json.loads(
                                        strBuffer[itupPos[0] : itupPos[1] + 1]))
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        return dictlstResult

class XML_Parser(JSON_Parser):
    """
    Specialized singleton class for parsing the XML files. Derived from the
    class JSON_Parser. Redefines the helper class method
        _loadFile()
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(xml.etree.ElementTree.Element)
    
    Note, that if the file parsing template is not provided, it is determined
    automatically based on the content of the already loaded data. If the
    proper template cannot be determined the ValueError exception is raised.
    
    Inherits all class methods of the super class.
    
    Methods:
        parseSingleObject()
            type A, class B, dict/,
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool, bool, bool / -> type B
        parseFile()
            logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/ -> list(type A)
        parseManyFiles()
            str, list(str)/, class A, dict
                logging.Logger OR `LoggingFSIO.ConsoleLogger,
                    bool OR None, bool, bool/
                        -> collections.OrderedDict(str : list(type A))
    
    Version 0.1.0.0
    """
    
    #'private' class fields
    
    _SearchIndex = XML_INDEX
    
    _Type = 'XML'
    
    #'private' class methods
    
    @classmethod
    def _loadFile(cls, strFile, dictHints, objLogger = None):
        """
        Helper class method for the actual parsing of XML data file.
        
        Signature:
            str, dict/, logging.Logger OR `LoggingFSIO.ConsoleLogger/
                -> list(xml.etree.ElementTree.Element)
        
        Args:
            strFile: str, the path to a file to process
            dictHints: dict, dictionary of hints for processing of the file, if
                such are extracted from the mapping template
            objLogger: logging.Logger OR `LoggingFSIO.ConsoleLogger, instance of
                as a logger object with the standard API
        
        Returns:
            list(xml.etree.ElementTree.Element): 1 element list - individual
                object extracted from the file
        
        Version 0.1.0.0
        """
        try:
            etTree = ElementTree.parse(strFile)
            eteRoot = etTree.getroot()
        except Exception as Err:
            if not (objLogger is None):
                strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
                objLogger.error(strMessage)
            raise
        return [eteRoot]

#functions

def parseFile(strFile, clsTarget = None, dictTemplate = None, objLogger = None,
            bStrictTarget = None, bStrictSource = True, bForceTarget = False):
    """
    Parses a single data file according to the specified template and returns a
    list of instances of the target class. Wraps the corresponding methods of
    the classes TSV_Parser, JSON_Parser and XML_Parser.
    
    If the target class is not specified, the suggested target class is taken
    from the file processing template - if this is not possible the ValueError
    is raised.
    
    If the file processing template is not provided, it should be determined by
    the content of the file to be processed - if this is not possible the
    ValueError is raised.
    
    Signature:
        str/, class A, dict, logging.Logger OR `LoggingFSIO.ConsoleLogger,
            bool OR None, bool, bool/ -> list(type A)
    
    Args:
        strFile: str, full path to the data file to be parsed
        clsTarget: (optional) class A, class onto instances of which the
            extracted from a file data must be mapped
        dictTemplate: (optional) dict, file parsing template, must contain the
            top level key 'DataMapping' with the mapping rules dictionary as its
            value
        objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
            instance of, the logger object, by default is None (not provided)
        bStrictTarget: (optional) bool OR None, flag if the target object MUST
            have all expected elements, default value is None, meaning that the
            parser decides itself
        bStrictSource: (optional) bool, flag if the source object MUST have all
            expected elements, default value is True
        bForceTarget: (optional) bool, flag is the missing elements / paths are
            to be created in the target object, has an effect only if the value
            of bStrictTarget is False, the default value for bForceTarget False
    
    Returns:
        list(type A): a list of an instances of the target class
    
    Raises:
        TypeError: wrong mapping dictionary format or missmatch between the
            structure of the target and source objects and the mapping rules or
            the path to a file is not a string
        ValueError: wrong mapping dictionary format or missmatch between the
            structure of the target and source objects and the mapping rules or
            the template has no key 'DataMapping' or the value bound to it is
            not a dictionary; or the file path does not reference an existing
            file
        AttributeError: missing element of the target or source object if the
            corresponding flags are set to True, or an immutable element in the
            target object
    
    Version 0.1.0.0
    """
    try:
        GenericParser._checkFile(strFile)
    except Exception as Err:
        if not (objLogger is None):
            strMessage ='{}: {}'.format(Err.__class__.__name__, Err.message)
            objLogger.error(strMessage)
        raise
    _strFile = strFile.lower()
    if _strFile.endswith('.json'):
        lstClasses = [JSON_Parser, TSV_Parser, XML_Parser]
    elif _strFile.endswith('.xml'):
        lstClasses = [XML_Parser, TSV_Parser, JSON_Parser]
    else:
        lstClasses = [TSV_Parser, JSON_Parser, XML_Parser]
    lstResult = []
    for clsParser in lstClasses:
        try:
            lstResult = clsParser.parseFile(strFile, clsTarget = clsTarget,
                dictTemplate = dictTemplate, objLogger = objLogger,
                    bStrictTarget = bStrictTarget,
                    bStrictSource = bStrictSource, bForceTarget = bForceTarget)
        except:
            pass
        if len(lstResult):
            break
    if not len(lstResult):
        strError = 'Cannot parse {} file'.format(strFile)
        if not (objLogger is None):
            strMessage ='ValueError: {}'.format(strError)
            objLogger.error(strMessage)
        raise ValueError(strError)
    return lstResult

def parseManyFiles(strFolder, strlstFiles, clsTarget = None,
                    dictTemplate = None, objLogger = None, bStrictTarget = None,
                                    bStrictSource = True, bForceTarget = False):
    """
    Parses data from several specified data files within a single specified
    directory according to the specified template and returns an ordered
    dictionary of the base file names as keys and lists of instances of the
    target class as values. For each individual file calls the function
    parseFile().
    
    Work flow:
        1) check that the specified folder exists
        2) create an empty instance of collections.OrderedDict
        3) for each file in the specified list
            3.1) parse this file - parseFile() function
            3.2) store the base file name : returned list pair as an entry in
                the ordered dictionary
        4) return this ordered dictionary
    
    If the target class is not specified, the suggested target class is taken
    from the file processing template - if this is not possible the ValueError
    is raised. Dynamically for each file.
    
    If the file processing template is not provided, it should be determined by
    by the content of the file to be processed - if this is not possible the
    ValueError is raised. Dynamically for each file.
    
    Signature:
        str, list(str)/, class A, dict
            logging.Logger OR `LoggingFSIO.ConsoleLogger, bool OR None, bool,
                bool/ -> collections.OrderedDict(str : list(type A))
    
    Args:
        strFolder: str, path to a folder containing the data files
        strlstFiles: list(str), base names of the data files to parse
            within that folder
        clsTarget: (optional) class A, class onto instances of which the
            extracted from a file data must be mapped
        dictTemplate: (optional) dict, file parsing template, must contain
            the top level key 'DataMapping' with the mapping rules dictionary as
            its value
        objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
            instance of, the logger object, by default is None (not provided)
        bStrictTarget: (optional) bool OR None, flag if the target object MUST
            have all expected elements, default value is None, meaning that the
            parser decides itself
        bStrictSource: (optional) bool, flag if the source object MUST have all
            expected elements, default value is True
        bForceTarget: (optional) bool, flag is the missing elements / paths are
            to be created in the target object, has an effect only if the value
            of bStrictTarget is False, the default value for bForceTarget False
    
    Returns:
        collections.OrderedDict: an ordered dictionary of pairs of the base file
            names and lists of the objects containing the data extracted from
            the corresponding file
    
    Raises:
        TypeError: wrong mapping dictionary format or missmatch between the
            structure of the target and source objects and the mapping rules or
            the path to a foler is not a string or any file name is not a
            string, or the list of base names is not a sequence
        ValueError: wrong mapping dictionary format or missmatch between the
            structure of the target and source objects and the mapping rules or
            the template has no key 'DataMapping' or the value bound to it is
            not a dictionary; or the folder path does not reference an existing
            folder or any referenced file there is missing
        AttributeError: missing element of the target or source object if the
            corresponding flags are set to True, or an immutable element in the
            target object
    
    Version 0.1.0.0
    """
    if not isinstance(strFolder, basestring):
        strError="Wrong type of the source folder {} argument".format(
                                                                type(strFolder))
        strError = "{}, must be a string".format(strError)
        if not (objLogger is None):
            strMessage ='TypeError: {}'.format(strError)
            objLogger.error(strMessage)
        raise TypeError(strError)
    if ((not isinstance(strlstFiles, collections.Sequence))
                                        or isinstance(strlstFiles, basestring)):
        strError="Wrong type of the files list {} argument".format(
                                                            type(strlstFiles))
        strError ="{}, must be a sequence and not a string".format(strError)
        if not (objLogger is None):
            strMessage ='TypeError: {}'.format(strError)
            objLogger.error(strMessage)
        raise TypeError(strError)
    if not os.path.isdir(strFolder):
        strError = "{} is not a path to a folder".format(strFolder)
        if not (objLogger is None):
            strMessage ='ValueError: {}'.format(strError)
            objLogger.error(strMessage)
        raise ValueError(strError)
    dictResult = collections.OrderedDict()
    for strFile in strlstFiles:
        if not isinstance(strFile, basestring):
            strError="Wrong type of the base file name {}".format(type(strFile))
            strError = "{}, must be a string".format(strError)
            if not (objLogger is None):
                strMessage ='TypeError: {}'.format(strError)
                objLogger.error(strMessage)
            raise TypeError(strError)
        strFilename = os.path.join(strFolder, strFile)
        lstResults = parseFile(strFilename, clsTarget, dictTemplate,
                objLogger = objLogger, bStrictTarget = bStrictTarget,
                    bStrictSource = bStrictSource, bForceTarget = bForceTarget)
        if len(lstResults):
            dictResult[strFile] = lstResults
    return dictResult