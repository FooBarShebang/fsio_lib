#usr/bin/python
"""
Module fsio_lib.LoggingFSIO.py

Implements 'safe/smart' copy / move / rename / delete file operations, which
intercept OS and I/O related exceptions raised during operations, which are
logged into console and / or file and returned as the result of an operation.

Also implements custom loggers to the console or to the console and a file,
which allow dynamic enabling and disabling of the output. Emulates 'virtual
inheritance' from the logging.Logger class by redirecting the attribute access;
thus the implemented classes provide direct access to all methods and data
fields expected from an instance of the logging.Logger class.

Implements the support of the loggers ancestor - descendant hierarchy: the names
of the loggers with the dots are supposed to indicate such relation: logger
'parent.child.grandchild' is descendant of 'parent.child', which is descendant
of 'parent' logger, even if it does not exist. The actual existence of the
supposed ancestors affects only the message propagation, but not the creation of
a logger, which can easily be 'orphan'.

The dynamic enabling / disabling of the console logging has an effect only on
the 'root' logger of the hierarchy and affects all its descendant; whereas
enabling / disabling of the console logging of a descendant logger has no effect
at all. The file logging can be enabled / disabled for each of the logger in the
hierarchy independently.

Classes:
    ConsoleLogger
        DualLogger
    LoggingFSIO

Warning:
    Due to the implementation of the 'virtual inheritance' the behavior of the
    function logging.getLogger() may be confusing. Suppose, that the class
    ConsoleLogger is instantiated as MyLoggger = ConsoleLogger('LoggerMy'). The
    call logging.getLogger('MyLogger') will return the reference to an instance
    of logging.Logger class, namely the value of MyLogger._logger, and not the
    instance MyLogger itself
"""

__version__ = "0.1.0.1"
__date__ = "26-10-2018"
__status__ = "Production"

#imports

#+standard libraries

import os
import inspect
import shutil
import logging
import datetime

#classes

class ConsoleLogger(object):
    """
    Custom logger class implementing logging into the console, which can be
    suppressed or re-enabled dynamically.
    
    Note that due to the support of the loggers ancestor - descendant hierarchy
    the names of the loggers with the dots are supposed to indicate such
    relation: logger 'parent.child.grandchild' is descendant of 'parent.child',
    which is descendant of 'parent' logger, even if it does not exist. The
    actual existence of the supposed ancestors affects only the message
    propagation, but not the creation of a logger, which can easily be 'orphan'.
    
    The dynamic enabling / disabling of the console logging has an effect only
    on the 'root' logger of the hierarchy and affects all its descendant;
    whereas enabling / disabling of the console logging of a descendant logger
    has no effect at all.
    
    By default, the logger event logging level is set to logging.DEBUG, but it
    can be changed at any moment using inherited method setLevel() as well as
    during the instantiation. The logging into console is enabled at the level
    passed as the optional keywird argument of the initialization method (
    defaults to logging.DEBUG). The console logging level can be changed, as
    well as the console logging may be entirely suppressed and then re-enabled.
    
    Any class instance has a hidden 'dummy' handler of NullHandler class, thus
    the real console logging handler can be disabled without complains from the
    logging module.
    
    The default format is:
        * For the level below WARNING - 2 lines:
            - logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            - actual message sent the logger
        * For the level of WARNING and above - 3 lines:
            - logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            - line number within and the path to the module, where the logging
                entry is issued
            - actual message sent the logger
    
    Virtually 'inherits' all API from the class logging.Logger by attribute
    resolution redirection, and adds new data fields and methods.
    
    Attributes:
        console: instance of logging.StreamHandler class, can be used for the
            direct access to the console logger handler
        formatter: instance of logging.Formatter class, can be used for the
            changing of the log entries format
    
    Methods:
        setConsoleLoggingLevel()
            int -> None
        enableConsoleLogging()
            None -> None
        disableConsoleLogging()
            None -> None
        setLevel()
            int -> None
        debug()
            str -> None
        info()
            str  -> None
        error()
            str -> None
        warning()
            str -> None
        critical()
            str -> None
    
    Version 0.1.0.1
    """
    
    #special methods
    
    def __init__(self, strName, level = logging.DEBUG):
        """
        Initialization method, which sets the logger instance name and logging
        level of the console output handler.
        
        Note that due to the support of the loggers ancestor - descendant
        hierarchy the names with the dots are supposed to indicate such relation
        as logger 'parent.child.grandchild' is descendant of 'parent.child',
        which is descendant of 'parent' logger, even if it does not exist.
        
        Signature:
            str/, int/ -> None
        
        Args:
            strName: string, the name of the logger to be created; it will be
                displayed as a part of the log entries, and it determines the
                loggers hierarchy (ancestor - descendant)
            level: (optional) non-negative integer, the logging level, e.g.
                logging.DEBUG, logging.WARNING, etc.
        
        Version 0.1.0.0
        """
        self.__dict__['_logger'] = logging.getLogger(strName)
        self._logger.setLevel(logging.DEBUG)
        self.addHandler(logging.NullHandler()) #dummy
        self.console = logging.StreamHandler()
        self.console.setLevel(level)
        self._setFormatNoLineCode()
        self.enableConsoleLogging()
    
    def __getattribute__(self, strName):
        """
        Modified getter method of the attributes resolution. Redirects the
        resolution scheme such, that the attributes of an instance of the class
        logging.Logger (referenced by the instance attribute self._logger) can
        be accessed directly, e.g. the call self.info(msg) is equivalent to the
        call self._logger.info(msg).
        
        Signature:
            str -> type A
        
        Args:
            strName: string, name of an attribute to obtain
        
        Returns:
            type A: the value of an attribute self._logger.strName (if exists)
                or self.strName (if exists, but not within self._logger)
        
        Raises:
            AttributeError: an attribute with this name is not found within
                the current object (or its ancestors) nor within the attribute
                _logger of the current object
        
        Version 0.1.0.0
        """
        if strName in ['__dict__', '__class__']:
            objResult = object.__getattribute__(self, strName)
        else:
            bCond1 = strName in self.__dict__
            bCond2 = any(map(lambda x: strName in x.__dict__,
                                                        self.__class__.__mro__))
            if bCond1 or bCond2:
                objResult = object.__getattribute__(self, strName)
            else:
                try:
                    objTemp = object.__getattribute__(self, '_logger')
                    if hasattr(objTemp, strName):
                        objResult=object.__getattribute__(self._logger, strName)
                    else: #should result in AttributeError exception
                        objResult = object.__getattribute__(self, strName)
                except AttributeError:
                    #should still result in AttributeError exception
                    objResult = object.__getattribute__(self, strName)
        return objResult
    
    def __setattr__(self, strName, gValue):
        """
        Modified setter method of the attributes resolution. Redirects the
        resolution scheme such, that the attributes of an instance of the class
        logging.Logger (referenced by the instance attribute self._logger) can
        be accessed directly, e.g. the call self.info(msg) is equivalent to the
        call self._logger.info(msg).
        
        Signature:
            str, type A -> None
        
        Args:
            strName: string, name of an attribute to assign to
            gValue: any type, the value to be assigned
        
        Version 0.1.0.0
        """
        try:
            objTemp = object.__getattribute__(self, '_logger')
            if hasattr(objTemp, strName):
                object.__setattr__(objTemp, strName, gValue)
            else:
                object.__setattr__(self, strName, gValue)
        except AttributeError:
            object.__setattr__(self, strName, gValue)
    
    def _setFormatWithLineCode(self, strModule, strCaller, iLine, strPath):
        """
        Helper method.
        
        Sets the  format of a log entry is a 3-lines string:
            * logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            * line number within and the path to the module, where the logging
                entry is issued
            * actual message sent the logger
        
        Signature:
            str, str, int, str -> None
        
        Args:
            strModule: str, name of the caller`s module, extracted from the
                stack traceback
            strCaller: str, name of the caller function / method, extracted from
                the stack traceback
            iLine: int, code line number, where the logger is called, extracted
                from the stack traceback
            strPath: str, path to the caller module, extracted from the stack
                traceback
        
        Version 0.1.0.1
        """
        if strCaller == '<module>':
            _strCaller = '__main__'
        else:
            _strCaller = strCaller
        if strModule == '__main__':
            _strModule = os.path.basename(os.path.abspath(strPath))
            _strModule = ".".join(_strModule.split('.')[:-1])
        else:
            _strModule = strModule
        self.formatter = logging.Formatter('\n'.join([
            '<<%(levelname)s>> %(asctime)s @{}.{}.{}'.format(_strModule,
                                                self._logger.name, _strCaller),
                'Line {} in {}'.format(iLine, strPath),
                '%(message)s']), '%Y-%m-%d %H:%M:%S')
        self.console.setFormatter(self.formatter)
    
    def _setFormatNoLineCode(self):
        """
        Helper method.
        
        Sets the  format of a log entry is a 2-lines string:
            * logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            * actual message sent the logger
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        self.formatter = logging.Formatter('\n'.join([
            '<<%(levelname)s>> %(asctime)s @%(module)s.%(name)s.%(funcName)s',
                '%(message)s']), '%Y-%m-%d %H:%M:%S')
        self.console.setFormatter(self.formatter)
    
    #public instance methods
    
    def enableConsoleLogging(self):
        """
        Method to enable logging into the console.
        
        The dynamic enabling / disabling of the console logging has an effect
        only on the 'root' logger of the hierarchy and affects all its
        descendant; it has no effect at all on a descendant logger.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        if isinstance(self.parent, logging.RootLogger):
            self._logger.addHandler(self.console)
    
    def disableConsoleLogging(self):
        """
        Method to disable logging into the console.
        
        The dynamic enabling / disabling of the console logging has an effect
        only on the 'root' logger of the hierarchy and affects all its
        descendant; it has no effect at all on a descendant logger.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        self._logger.removeHandler(self.console)
    
    def setConsoleLoggingLevel(self, level):
        """
        Method to change the logging level of the handler for the logging into
        the console. Basically, an alias for self.console.setLevel(level).
        
        Signature:
            int -> None
        
        Args:
            level: non-negative integer, the logging level, e.g. logging.DEBUG,
                logging.WARNING, etc
        
        Version 0.1.0.0
        """
        self.console.setLevel(level)
    
    def warning(self, strMessage, *args, **kwargs):
        """
        Wrapper for the logging.Logger.warning() method, which also temporary
        changes the format of the log entries.
        
        Signature:
            str/, type A/, ... // -> None
        
        Args:
            strMessage: str, (supposedly), the message body to be logged
            *args: type A, any number of the positional argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.warning()
            *kwargs: type A, any number of the keyword argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.warning()
        
        Version 0.1.0.1
        """
        objFrame, strPath, iLine, strCaller, _, _ = inspect.stack()[1]
        objModule = inspect.getmodule(objFrame)
        if not (objModule is None):
            strModule = objModule.__name__
        else:
            strModule = '<console input>'
        self._setFormatWithLineCode(strModule, strCaller, iLine, strPath)
        self._logger.warning(strMessage, *args, **kwargs)
        self._setFormatNoLineCode()
    
    def error(self, strMessage, *args, **kwargs):
        """
        Wrapper for the logging.Logger.error() method, which also temporary
        changes the format of the log entries.
        
        Signature:
            str/, type A/, ... // -> None
        
        Args:
            strMessage: str, (supposedly), the message body to be logged
            *args: type A, any number of the positional argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.error()
            *kwargs: type A, any number of the keyword argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.error()
        
        Version 0.1.0.1
        """
        objFrame, strPath, iLine, strCaller, _, _ = inspect.stack()[1]
        objModule = inspect.getmodule(objFrame)
        if not (objModule is None):
            strModule = objModule.__name__
        else:
            strModule = '<console input>'
        self._setFormatWithLineCode(strModule, strCaller, iLine, strPath)
        self._logger.error(strMessage, *args, **kwargs)
        self._setFormatNoLineCode()
    
    def exception(self, strMessage, *args, **kwargs):
        """
        Wrapper for the logging.Logger.error() method, which also temporary
        changes the format of the log entries.
        
        Signature:
            str/, type A/, ... // -> None
        
        Args:
            strMessage: str, (supposedly), the message body to be logged
            *args: type A, any number of the positional argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.error()
            *kwargs: type A, any number of the keyword argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.error()
        
        Version 0.1.0.1
        """
        objFrame, strPath, iLine, strCaller, _, _ = inspect.stack()[1]
        objModule = inspect.getmodule(objFrame)
        if not (objModule is None):
            strModule = objModule.__name__
        else:
            strModule = '<console input>'
        self._setFormatWithLineCode(strModule, strCaller, iLine, strPath)
        self._logger.exception(strMessage, *args, **kwargs)
        self._setFormatNoLineCode()
    
    def critical(self, strMessage, *args, **kwargs):
        """
        Wrapper for the logging.Logger.critical() method, which also temporary
        changes the format of the log entries.
        
        Signature:
            str/, type A/, ... // -> None
        
        Args:
            strMessage: str, (supposedly), the message body to be logged
            *args: type A, any number of the positional argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.critical()
            *kwargs: type A, any number of the keyword argumens, not really
                used, just kept for the compatibility with the wrapped method
                logging.Logger.critical()
        
        Version 0.1.0.1
        """
        objFrame, strPath, iLine, strCaller, _, _ = inspect.stack()[1]
        objModule = inspect.getmodule(objFrame)
        if not (objModule is None):
            strModule = objModule.__name__
        else:
            strModule = '<console input>'
        self._setFormatWithLineCode(strModule, strCaller, iLine, strPath)
        self._logger.critical(strMessage, *args, **kwargs)
        self._setFormatNoLineCode()

class DualLogger(ConsoleLogger):
    """
    Custom logger class implementing logging into the console and / or into a
    file, which can be suppressed or re-enabled dynamically.
    
    Note that due to the support of the loggers ancestor - descendant hierarchy
    the names of the loggers with the dots are supposed to indicate such
    relation: logger 'parent.child.grandchild' is descendant of 'parent.child',
    which is descendant of 'parent' logger, even if it does not exist. The
    actual existence of the supposed ancestors affects only the message
    propagation, but not the creation of a logger, which can easily be 'orphan'.
    
    The dynamic enabling / disabling of the console logging has an effect only
    on the 'root' logger of the hierarchy and affects all its descendant;
    whereas enabling / disabling of the console logging of a descendant logger
    has no effect at all. The file logging can be enabled / disabled for each
    of the logger in the hierarchy independently.
    
    By default, the logger event logging level is set to logging.DEBUG, but it
    can be changed at any moment using inherited method setLevel() as well as
    during the instantiation. The logging into console is enabled at the level
    passed as the optional keyword argument of the initialization method 
    defaults to logging.DEBUG). The console logging level can be changed, as
    well as the console logging may be entirely suppressed and then re-enabled.
    
    The logging into a file is disabled initially unless explicitly asked
    otherwise during the instantiation, whilst the default file logging level is
    set to logging.WARNING. If the name of the log file to be used is not
    specified, its created automatically by the date and time of instantiation
    and the logger instance name, even if the file logging is disabled.
    
    Implementation details:
        * has a hidden 'dummy' handler of NullHandler class, thus the both real
            handlers can be disabled without complains from the logging
            functionality
        * actual log file is not created / re-opened until the file logging is
            enabled implicitly (or by setting the flag to True during the
            instantiation)
        * call to the method changeLogFile() automatically enables the file
            logging, thus log file is created / re-opened
        * the log files are created / re-opened in the 'w' mode, thus clearing
            their previous content, but disabling / suppressing of the file
            logging doesn't actually closes the log file, therefore the re-
            enabling of the file logging doesn't delete the previously made
            entries
    
    The default format is:
        * For the level below WARNING - 2 lines:
            - logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            - actual message sent the logger
        * For the level of WARNING and above - 3 lines:
            - logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            - line number within and the path to the module, where the logging
                entry is issued
            - actual message sent the logger
    
    Virtually 'inherits' all API from the class logging.Logger by attribute
    resolution redirection via its direct super class ConsoleLogger, and adds
    new data fields and methods.
    
    Attributes:
        console: instance of logging.StreamHandler class, can be used for the
            direct access to the console logger handler
        file_logging: instance of logging.FileHandler or logging.NullHandler
            class, can be used for the direct access to the file logger handler
        formatter: instance of logging.Formatter class, can be used for the
            changing of the log entries format
    
    Methods:
        setConsoleLoggingLevel()
            int -> None
        enableConsoleLogging()
            None -> None
        disableConsoleLogging()
            None -> None
        setFileLoggingLevel()
            int -> None
        enableFileLogging()
            None -> None
        disableFileLogging()
            None -> None
        changeLogFile()
            /str/ -> None
        setLevel()
            int -> None
        debug()
            str -> None
        info()
            str  -> None
        error()
            str -> None
        warning()
            str -> None
        critical()
            str -> None
    
    Version 0.1.0.1
    """
    
    #special methods
    
    def __init__(self, strName, bLogToFile = False, strFileName = None,
                    level = logging.DEBUG):
        """
        Initialization method, which sets the logger instance name, logging
        level and log file (even if the logging into a file is suppressed).
        
        Note that due to the support of the loggers ancestor - descendant
        hierarchy the names with the dots are supposed to indicate such relation
        as logger 'parent.child.grandchild' is descendant of 'parent.child',
        which is descendant of 'parent' logger, even if it does not exist.
        
        If optional file name is not passed during instantiation of the class,
        it is defined automatically from the current date and time as well as
        the 'name' of the logger instance with the extension '.log'. Otherwise,
        the file name passed during instantiation of the class is remembered
        with the standard convention on absolute / relative to the current
        working directory path being applied.
        
        Note that the log file is not created / opened immediately if the
        second (optional) argument - boolean flag - is False, i.e. the logging
        into a file is suppressed. However, if the file logging is enabled, the
        actual log file is created or re-opened in 'w' mode using the filename
        passed into this method or automatically defined during the
        instantiation.
        
        Signature:
            str/, bool, str, int/ -> None
        
        Args:
            strName: string, the name of the logger to be created; it will be
                displayed as a part of the log entries, and can be used for the
                (de-) selection of this particular logger from the pool of the
                available ones, see function logging.getLogger()
            bLogToFile: (optional) boolean flag, if the file logging is to be
                initially enabled
            strFileName: (optional) string, filename to be used for the log file
                if the file logging is enabled
            level: (optional) non-negative integer, the logging level, e.g.
                logging.DEBUG, logging.WARNING, etc.
        
        Version 0.1.0.0
        """
        if strFileName is None:
            self.log_file = '{}_{}.log'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'), strName)
        else:
            self.log_file = str(strFileName)
        if bLogToFile:
            self.file_logging = logging.FileHandler(self.log_file, mode = 'w')
        else:
            self.file_logging = logging.NullHandler()
        self.file_logging.setLevel(logging.WARNING)
        super(DualLogger, self).__init__(strName, level = level)
        if bLogToFile and isinstance(self.parent, logging.RootLogger):
            self.enableFileLogging()
    
    def _setFormatWithLineCode(self, *args):
        """
        Helper method.
        
        Sets the  format of a log entry is a 3-lines string:
            * logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            * line number within and the path to the module, where the logging
                entry is issued
            * actual message sent the logger
        
        Signature:
            str, str, int, str -> None
        
        Args:
            strModule: str, name of the caller`s module, extracted from the
                stack traceback
            strCaller: str, name of the caller function / method, extracted from
                the stack traceback
            iLine: int, code line number, where the logger is called, extracted
                from the stack traceback
            strPath: str, path to the caller module, extracted from the stack
                traceback
        
        Version 0.1.0.1
        """
        super(DualLogger, self)._setFormatWithLineCode(*args)
        self.file_logging.setFormatter(self.formatter)
    
    def _setFormatNoLineCode(self):
        """
        Helper method.
        
        Sets the  format of a log entry is a 2-lines string:
            * logging level, date and time in ASCII format, name of the module,
                name of the logger (not its class), name of the calling function
            * actual message sent the logger
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        super(DualLogger, self)._setFormatNoLineCode()
        self.file_logging.setFormatter(self.formatter)
    
    #public instance methods
    
    def enableFileLogging(self):
        """
        Method to enable logging into a file. If the logging into the file was
        not enabled upon instantiation of the class, a log file is created;
        otherwise the existing log file is 're-used'.
        
        If optional file name is not passed during instantiation of the class,
        it is defined automatically from the date and time of instantiation as
        well as the 'name' of the logger instance with the extension '.log'.
        Otherwise, the file name passed during instantiation of the class is
        used with the standard convention on absolute / relative to the current
        working directory path being applied.
        
        Note that the file logging can be enabled / disabled for each of the
        logger in the hierarchy independently.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        if isinstance(self.file_logging, logging.NullHandler):
            iCurrentLevel = self.file_logging.level
            self._logger.removeHandler(self.file_logging)
            del self.file_logging
            self.file_logging = logging.FileHandler(self.log_file, mode = 'w')
            self.file_logging.setLevel(iCurrentLevel)
            self.file_logging.setFormatter(self.formatter)
        self._logger.addHandler(self.file_logging)
    
    def disableFileLogging(self):
        """
        Method to disable logging into a file. Note that the active log file is
        not actually closed, its handler is simply removed from the list of
        handlers. Therefore, is the file logging is re-enabled later, the
        already made log entries are not removed.
        
        Note that the file logging can be enabled / disabled for each of the
        logger in the hierarchy independently.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        if isinstance(self.file_logging, logging.FileHandler):
            self._logger.removeHandler(self.file_logging)
    
    def setFileLoggingLevel(self, level):
        """
        Method to change the logging level of the handler for the logging into
        a file. Basically, an alias for self.file_logging.setLevel(level).
        
        Signature:
            int -> None
        
        Args:
            level: non-negative integer, the logging level, e.g. logging.DEBUG,
            logging.WARNING, etc.
        
        Version 0.1.0.0
        """
        self.file_logging.setLevel(level)
    
    def changeLogFile(self, strFileName = None):
        """
        Method to change the active log file. If logging to a file was disabled
        this method automatically enables it. Otherwise, the log file used
        before is closed, and the new log file is created.
        
        If optional file name is not passed, it is defined automatically from
        the current date and time as well as the 'name' of the logger instance
        with the extension '.log'. Note that in this case the log file is
        created in the current working directory.
        
        Signature:
            /str/ -> None
        
        Args:
            strFileName: (optional) string, or any type convertible to a string,
                the filename of a log file to switch to; the standard convention
                on absolute / relative to the current working directory path is
                applied.
        
        Version 0.1.0.0
        """
        iCurrentLevel = self.file_logging.level
        if strFileName is None:
            self.log_file = '{}_{}.log'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'),
                    self.name)
        else:
            self.log_file = str(strFileName)
        self.file_logging.close()
        self._logger.removeHandler(self.file_logging)
        del self.file_logging
        self.file_logging = logging.FileHandler(self.log_file, mode = 'w')
        self.file_logging.setLevel(iCurrentLevel)
        self.file_logging.setFormatter(self.formatter)
        self._logger.addHandler(self.file_logging)

class LoggingFSIO(object):
    """
    Implements 'safe/smart' copy / move / rename / delete file operations, which
    intercept OS and I/O related exceptions raised during operations, which are
    logged into console and / or file and returned as the result of the
    operation. Also the file copy / move / rename operation preserves the file's
    metadata, like created date, etc.
    
    Designed to be used as a Singleton, thus it doesn't require instantiation,
    and all implemented methods are class methods.
    
    All methods perform input data sanity checks and intercept the raised
    IOError and OSError exceptions, which are converted into string error
    messages. This approach ensures continuous, non-interruptive (without not
    caught exceptions) but controllable batch file operations, like mass copy,
    etc. All methods return a 2-tuple of an integer error / status code and a
    string textual explanation as follows:
        0 : 'Ok',
        1 : 'Not a string argument:',
        2 : 'Path is not found:',
        3 : 'System error:',
        4 : 'Failed to perform an operation without system error:'
    
    The exit code > 0 is an error situation, in which case the string
    explanation is normally extended with the details of the error, e.g., with
    which file or folder there is a problem, or the details of the raised and
    caught exception.
    
    In addition, all methods log the progress of the work flow and the
    encountered problems at different severity levels:
        * DEBUG - normal work flow along the paths, which do not change the
            state of the file system
        * INFO - normal work flow along the paths, which result in creation of
            files or folders or deletion of files
        * WARNING - not true errors and part of the normal work flow, but the
            result may differ from the user's expectations, e.g., refused copy
            operation of a file onto itself
        * ERROR - actual errors, interrupted work flow, including failed input
            data sanity checks and raised and caught exceptions
    
    N.B. the default logger referenced by a 'private' class field _Logger is an
    instance of the DualLogger class, which includes the handlers for the
    console logging (enabled by default at INFO severity level) and for the
    logging into a file (by default set at WARNING severity level and disabled),
    whereas the logger itself is set at DEBUG level.
    
    Class methods:
        makeDirs()
            str -> int, str
        copyFile()
            str\, str, str\ -> int, str
        deleteFile()
            str -> int, str
        moveFile()
            str, str\, str\ -> int, str
        renameFile()
            str, str -> int, str
        setConsoleLoggingLevel()
            int -> None
        setLoggingLevel()
            int -> None
        setConsoleLoggingLevel()
            int -> None
        setFileLoggingLevel()
            int -> None
        changeLogFile()
            /str/ -> None
        enableConsoleLogging()
            None -> None
        disableConsoleLogging()
            None -> None
        enableFileLogging()
            None -> None
        disableFileLogging()
            None -> None
    
    Version 0.1.0.0
    """
    
    #class data attributes
    
    _Logger = DualLogger('LoggingFSIO', bLogToFile = False)
    
    _dictErrors = {
            0 : 'Ok',
            1 : 'Not a string argument:',
            2 : 'Path is not found:',
            3 : 'System error:',
            4 : 'Failed to perform an operation without system error:'
        }
    
    @classmethod
    def makeDirs(cls, strFolder):
        """
        Method to create recursively (all nested levels) a folder specified by
        relative or absolute path passed as the argument. If this end leaf
        folder already exists, the method simply returns the success status
        (error code 0) with the corresponding string message.
        
        Relies upon the Standard Python Library function os.makedirs(). If this
        folder cannot be created due to permission limitations, the normally
        raised OSError or IOError exceptions are intercepted and converted into
        the string textual explanation, which is returned together with the
        error code 3.
        
        Logs the work flow and encountered errors / exceptions using the class'
        logger.
        
        Signature:
            str -> int, str
        
        Args:
            strFilePath: str, relative or absolute path to a file to be deleted
        
        Returns:
            tuple(int, str): an unpacked tuple of an integer (error code, 0 is
                Ok) and a string (textual description of an error).
        
        Version 0.1.0.0
        """
        iError = 0
        strError = cls._dictErrors[iError]
        if not isinstance(strFolder, basestring):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strFolder),
                                                    'of', str(type(strFolder))])
            cls._Logger.error(strError)
        else:
            if os.path.isdir(strFolder):
                cls._Logger.debug('{} folder already exists'.format(strFolder))
            else:
                try:
                    _strFolder = os.path.abspath(strFolder)
                    os.makedirs(_strFolder)
                    if not os.path.isdir(_strFolder):
                        iError = 4
                        strError = '{} create folder {}'.format(
                                            cls._dictErrors[iError], _strFolder)
                        cls._Logger.error(strError)
                    else:
                        strMessage = 'Created {} folder'.format(_strFolder)
                        cls._Logger.info(strMessage)
                except (IOError, OSError) as err:
                    iError = 3
                    strError = ' '.join([cls._dictErrors[iError],
                                         '{}:'.format(err.__class__.__name__),
                                         '[Errno {}]'.format(err.errno),
                                         'on "{}" -'.format(_strFolder),
                                         str(err.strerror)])
                    cls._Logger.error(strError)
        return iError, strError
    
    @classmethod
    def copyFile(cls, strSourceFilePath, strTargetFolder = None,
                    strNewBaseName = None):
        """
        Method to copy a file into a new folder with the optional renaming of
        the created copy. Three major modes of operation are available depending
        on the passed (optional) arguments for the new location (folder) and
        the new base file name:
            * new location (folder) is provided and different from the current
                one, and the new base name is provided and different from the
                current one - the file is copied into a new folder and the copy
                is renamed
            * new location (folder) is provided and different from the current
                one, and the new base name is not provided or is the same as the
                current one - the file is copied into a new folder with the same
                base name
            * new location (folder) is not provided or is the same as the
                current one, and the new base name is provided and different
                from the current one - a new copy of the file with a diffent
                base name is created in the same (source) folder
        
        Relies upon the Standard Python Library function shutil.copy2(), which
        preserves the file's metadata. If this file cannot be copied into the
        specified destination due to permission limitations, the normally
        raised OSError or IOError exceptions are intercepted and converted into
        the string textual explanation, which is returned together with the
        error code 3.
        
        Existing file in the target folder is overwritten.
        
        Logs the work flow and encountered errors / exceptions using the class'
        logger.
        
        Signature:
            str\, str, str\ -> int, str
        
        Args:
            strSourceFilePath: str, relative or absolute path to a file to be
                copied
            strTargetFolder: (optional) str, relative or absolute path to the
                target folder; if not specified (or the default value None is
                passed), the current location (folder) of the file to be copied
                is used as the target folder as well, in this case the new base
                name must differ from the current base name of the file,
                otherwise the file will not be copied upon itself
            strNewBaseName: (optional) str, new base name of the file; N.B. this
                string should not contain any folders, only the base name (with
                the extension if required); if this attribute is not passed (or
                default None value is passed) the file is simply moved into the
                new folder without change of its base name. Note: both the
                strTargetFolder and strNewBaseName arguments cannot be None
                simultaneously; such case is treated as an error with the return
                code 1.
        
        Returns:
            tuple(int, str): an unpacked tuple of an integer (error code, 0 is
                Ok) and a string (textual description of an error).
        
        Version 0.1.0.0
        """
        iError = 0
        strError = cls._dictErrors[iError]
        if not isinstance(strSourceFilePath, basestring):
            iError = 1
            strError =' '.join([cls._dictErrors[iError], str(strSourceFilePath),
                                            'of', str(type(strSourceFilePath))])
            cls._Logger.error(strError)
        elif not os.path.isfile(os.path.abspath(strSourceFilePath)):
            iError = 2
            strError = '{} {}'.format(cls._dictErrors[iError], os.path.abspath(
                                                            strSourceFilePath))
            cls._Logger.error(strError)
        elif (strTargetFolder is None) and (strNewBaseName is None):
            iError = 1
            strError =' '.join([cls._dictErrors[iError], 'either target folder',
                                'or new base file name must be not None'])
            cls._Logger.error(strError)
        elif ((not (strTargetFolder is None)) and
                                (not isinstance(strTargetFolder, basestring))):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strTargetFolder),
                                            'of', str(type(strTargetFolder))])
            cls._Logger.error(strError)
        elif ((not (strNewBaseName is None)) and
                                (not isinstance(strNewBaseName, basestring))):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strNewBaseName),
                                            'of', str(type(strNewBaseName))])
            cls._Logger.error(strError)
        else:
            if not (strTargetFolder is None):
                iError, strError = cls.makeDirs(strTargetFolder)
            if not iError:
                _strSourceFilePath = os.path.abspath(strSourceFilePath)
                if strTargetFolder is None:
                    strNewFolder = os.path.dirname(_strSourceFilePath)
                else:
                    strNewFolder = os.path.abspath(strTargetFolder)
                if strNewBaseName is None:
                    strBaseName = os.path.basename(_strSourceFilePath)
                else:
                    strBaseName = strNewBaseName
                strNewFullPath = os.path.abspath(os.path.join(strNewFolder,
                                                                strBaseName))
                try:
                    if _strSourceFilePath != strNewFullPath:
                        shutil.copy2(strSourceFilePath, strNewFullPath)
                        if os.path.isfile(strNewFullPath):
                            strMessage = 'Copied {} file to {}'.format(
                                            _strSourceFilePath, strNewFullPath)
                            cls._Logger.info(strMessage)
                        else:
                            iError = 4
                            strError = '{} copy file {} to {}'.format(
                                        cls._dictErrors[iError],
                                        _strSourceFilePath, strNewFullPath)
                            cls._Logger.error(strError)
                    else:
                        cls._Logger.warning(
                                'same path {}, file is not copied'.format(
                                                            _strSourceFilePath))
                except (IOError, OSError) as err:
                    iError = 3
                    strError = ' '.join([cls._dictErrors[iError],
                                         '{}:'.format(err.__class__.__name__),
                                         '[Errno {}]'.format(err.errno),
                                         'on "{}" -'.format(strNewFullPath),
                                         str(err.strerror)])
                    cls._Logger.error(strError)
            else:
                cls._Logger.error(strError)
        return iError, strError
    
    @classmethod
    def deleteFile(cls, strFilePath):
        """
        Method to delete a file specified by relative or absolute path passed as
        the argument.
        
        Relies upon the Standard Python Library function os.remove(). If file
        cannot be deleted due to permission limitations, the normally raised
        OSError or IOError exceptions are intercepted and converted into the
        string textual explanation, which is returned together with the error
        code 3.
        
        Logs the work flow and encountered errors / exceptions using the class'
        logger.
        
        Signature:
            str -> int, str
        
        Args:
            strFilePath: str, relative or absolute path to a file to be deleted

        Returns:
            tuple(int, str): an unpacked tuple of an integer (error code, 0 is
                Ok) and a string (textual description of an error).
        
        Version 0.1.0.0
        """
        iError = 0
        strError = cls._dictErrors[iError]
        if not isinstance(strFilePath, basestring):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strFilePath),
                                                'of', str(type(strFilePath))])
            cls._Logger.error(strError)
        else:
            _strFilePath = os.path.abspath(strFilePath)
            if os.path.isdir(_strFilePath):
                iError = 3
                strError = '{} {} is a directory'.format(
                                        cls._dictErrors[iError], _strFilePath)
                cls._Logger.error(strError)
            elif not os.path.isfile(_strFilePath):
                iError = 2
                strError = '{} {}'.format(cls._dictErrors[iError], _strFilePath)
                cls._Logger.error(strError)
            else:
                try:
                    os.remove(_strFilePath)
                    if os.path.isfile(_strFilePath):
                        iError = 4
                        strError = '{} delete file {}'.format(
                                        cls._dictErrors[iError], _strFilePath)
                        cls._Logger.error(strError)
                    else:
                        strMessage = 'Removed {} file'.format(_strFilePath)
                        cls._Logger.info(strMessage)
                except (IOError, OSError) as err:
                    iError = 3
                    strError = ' '.join([cls._dictErrors[iError],
                                         '{}:'.format(err.__class__.__name__),
                                         '[Errno {}]'.format(err.errno),
                                         'on {} -'.format(_strFilePath),
                                         str(err.strerror)])
                    cls._Logger.error(strError)
        return iError, strError
    
    @classmethod
    def moveFile(cls, strSourceFilePath, strTargetFolder,
                    strNewBaseName = None):
        """
        Method to move a file specified by relative or absolute path as the
        first argument into another folder specified as relative or absolute
        path and, optionally, change its base name into a new one provided as
        the third (keyword, optional) argument.
        
        Note that if the target folder is the same as the current folder of the
        file to be moved, the new base name must be provided - in this case the
        file is renamed, see also class method renameFile() - otherwise the
        requested operation is ignored.
        
        If the new base name is not provided (or the default None value is
        given), the base name of the file is not changed, only its location.
        
        The original file is, at first, copied into a new location with optional
        change of its base name. Only if copying operation is successful, the
        original file is deleted. Thus, due to file permissions it is possible
        that a new file is created but the original one is not deleted.
        
        Existing file in the target folder is overwritten.
        
        Wraps the class methods copyFile() and deleteFile().
        
        Logs the work flow and encountered errors / exceptions using the class'
        logger.
        
        Signature:
            str, str\, str\ -> int, str
        
        Args:
            strSourceFilePath: str, relative or absolute path to a file to be
                renamed
            strTargetFolder: str, relative or absolute path to the target folder
            strNewBaseName: (optional) str, new base name of the file; N.B. this
                string should not contain any folders, only the base name (with
                extension if required); if this attribute is not passed (or
                default None value is passed) the file is simply moved into the
                new folder without change of its base name

        Returns:
            tuple(int, str): an unpacked tuple of an integer (error code, 0 is
                Ok) and a string (textual description of an error).
        
        Version 0.1.0.0
        """
        if not isinstance(strSourceFilePath, basestring):
            iError = 1
            strError =' '.join([cls._dictErrors[iError], str(strSourceFilePath),
                                            'of', str(type(strSourceFilePath))])
            cls._Logger.error(strError)
        elif not os.path.isfile(os.path.abspath(strSourceFilePath)):
            iError = 2
            strError = '{} {}'.format(cls._dictErrors[iError],
                                            os.path.abspath(strSourceFilePath))
            cls._Logger.error(strError)
        elif not isinstance(strTargetFolder, basestring):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strTargetFolder),
                                            'of', str(type(strTargetFolder))])
            cls._Logger.error(strError)
        elif ((not (strNewBaseName is None)) and
                                (not isinstance(strNewBaseName, basestring))):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strNewBaseName),
                                            'of', str(type(strNewBaseName))])
            cls._Logger.error(strError)
        else:
            _strSourceFilePath = os.path.abspath(strSourceFilePath)
            _strTargetFolder = os.path.abspath(strTargetFolder)
            if not (strNewBaseName is None):
                strFullNewPath = os.path.join(_strTargetFolder, strNewBaseName)
            else:
                strFullNewPath = os.path.join(_strTargetFolder,
                                        os.path.basename(_strSourceFilePath))
            
            strFullNewPath = os.path.abspath(strFullNewPath)
            if _strSourceFilePath != strFullNewPath:
                strFolderPath = os.path.dirname(strFullNewPath)
                strBaseFileName = os.path.basename(strFullNewPath)
                iError, strError = cls.copyFile(_strSourceFilePath,
                                                strFolderPath, strBaseFileName)
                if iError:
                    cls._Logger.error(strError)
                else:
                    cls._Logger.debug('file copy is ok')
                    iError, strError = cls.deleteFile(strSourceFilePath)
                    if iError:
                        cls._Logger.error(strError)
                    else:
                        cls._Logger.debug('file delete is ok')
            else:
                cls._Logger.warning('same path, file is not moved')
                iError = 0
                strError = cls._dictErrors[iError]
        return iError, strError
    
    @classmethod
    def renameFile(cls, strSourceFilePath, strNewBaseName):
        """
        Method to rename a file specified by relative or absolute path as the
        first argument, i.e. to change its base name to a new value given as
        the second argument without relocation (file remains in its original
        folder).
        
        Wraps the class method moveFile().
        
        Logs the work flow and encountered errors / exceptions using the class'
        logger.
        
        Signature:
            str, str -> int, str
        
        Args:
            strSourceFilePath: str, relative or absolute path to a file to
                be renamed
            strNewBaseName: str, new base name of the file; N.B. this string
                should not contain any folders, only the base name (with
                extension if required)
        
        Returns:
            tuple(int, str): an unpacked tuple of an integer (error code, 0 is
                Ok) and a string (textual description of an error).
        
        Version 0.1.0.0
        """
        if not isinstance(strSourceFilePath, basestring):
            iError = 1
            strError =' '.join([cls._dictErrors[iError], str(strSourceFilePath),
                                            'of', str(type(strSourceFilePath))])
            cls._Logger.error(strError)
        elif not os.path.isfile(os.path.abspath(strSourceFilePath)):
            iError = 2
            strError = '{} {}'.format(cls._dictErrors[iError],
                                            os.path.abspath(strSourceFilePath))
            cls._Logger.error(strError)
        elif not isinstance(strNewBaseName, basestring):
            iError = 1
            strError = ' '.join([cls._dictErrors[iError], str(strNewBaseName),
                                            'of', str(type(strNewBaseName))])
            cls._Logger.error(strError)
        else:
            strBaseFileName = os.path.basename(strNewBaseName)
            if strBaseFileName != strNewBaseName:
                iError = 2
                strError='{} {}'.format(cls._dictErrors[iError], strNewBaseName)
                cls._Logger.error(strError)
            else:
                strFolderPath = os.path.dirname(os.path.abspath(
                                                            strSourceFilePath))
                iError, strError = cls.moveFile(strSourceFilePath,
                                                    strFolderPath,
                                                        strBaseFileName)
                if iError:
                    cls._Logger.error(strError)
                else:
                    cls._Logger.debug('file rename is ok')
        return iError, strError
    
    @classmethod
    def setLoggingLevel(cls, iLevel):
        """
        Sets the overal logging level of the bound logger object. Wrapper for
        ConsoleLogger.setLevel() method, which is, actually, the 'short-cut' for
        logging.Logger.setLevel() method.
        
        Signature:
            int -> None
        
        Args:
            iLevel: non-negative integer, the logging level, e.g. logging.DEBUG,
                logging.WARNING, etc
        
        Version 0.1.0.0
        """
        cls._Logger.setLevel(iLevel)
    
    @classmethod
    def setConsoleLoggingLevel(cls, iLevel):
        """
        Sets the logging level into the file of the bound logger object. Wrapper
        for ConsoleLogger.setConsoleLoggingLevel() method.
        
        Signature:
            int -> None
        
        Args:
            level: non-negative integer, the logging level, e.g. logging.DEBUG,
                logging.WARNING, etc
        
        Version 0.1.0.0
        """
        cls._Logger.setConsoleLoggingLevel(iLevel)
    
    @classmethod
    def setFileLoggingLevel(cls, iLevel):
        """
        Sets the logging level into the file of the bound logger object. Wrapper
        for DualLogger.setFileLoggingLevel() method.
        
        Signature:
            int -> None
        
        Args:
            level: non-negative integer, the logging level, e.g. logging.DEBUG,
                logging.WARNING, etc
        
        Version 0.1.0.0
        """
        cls._Logger.setFileLoggingLevel(iLevel)
    
    @classmethod
    def changeLogFile(cls, strFileName = None):
        """
        Method to change the active log file. If logging to a file was disabled
        this method automatically enables it. Otherwise, the log file used
        before is closed, and the new log file is created.
        
        If optional file name is not passed, it is defined automatically from
        the current date and time as well as the 'name' of the logger instance
        with the extension '.log'. Note that in this case the log file is
        created in the current working directory.
        
        Wraps the DualLogger.changeLogFile() method.
        
        Signature:
            /str/ -> None
        
        Args:
            strFileName: (optional) string, or any type convertible to a string,
                the filename of a log file to switch to; the standard convention
                on absolute / relative to the current working directory path is
                applied.
        
        Version 0.1.0.0
        """
        cls._Logger.changeLogFile(strFileName)
    
    @classmethod
    def enableConsoleLogging(cls):
        """
        Method to enable logging into the console.
        
        Wraps the ConsoleLogger.enableConsoleLogging() method.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        cls._Logger.enableConsoleLogging()
    
    @classmethod
    def disableConsoleLogging(cls):
        """
        Method to disable logging into the console.
        
        Wraps the ConsoleLogger.disableConsoleLogging() method.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        cls._Logger.disableConsoleLogging()
    
    @classmethod
    def enableFileLogging(cls):
        """
        Method to enable logging into a file. If the logging into the file was
        not enabled upon instantiation of the class, a log file is created;
        otherwise the existing log file is 're-used'.
        
        If optional file name is not passed during instantiation of the class,
        it is defined automatically from the date and time of instantiation as
        well as the 'name' of the logger instance with the extension '.log'.
        Otherwise, the file name passed during instantiation of the class is
        used with the standard convention on absolute / relative to the current
        working directory path being applied.
        
        Wraps the DualLogger.enableFileLogging() method.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        cls._Logger.enableFileLogging()
    
    @classmethod
    def disableFileLogging(cls):
        """
        Method to disable logging into a file. Note that the active log file is
        not actually closed, its handler is simply removed from the list of
        handlers. Therefore, is the file logging is re-enabled later, the
        already made log entries are not removed.
        
        Wraps the DualLogger.disableFleLogging() method.
        
        Signature:
            None -> None
        
        Version 0.1.0.0
        """
        cls._Logger.disableFileLogging()
