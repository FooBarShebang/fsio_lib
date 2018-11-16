#usr/bin/python
"""
Module fio_lib.dynamic_import

Implements functions to import modules or objects from modules dynamically, i.e.
using their string names at the runtime.

Functions:
    import_module(strPath, strAlias = None, dictGlobals = None):
        str/, str, dict/ -> __builtins__.module
    import_from_module(strPath, strName, strAlias = None, dictGlobals = None):
        str, str/, str, dict/ -> type A
"""

__version__ = "0.1.0.0"
__date__ = "01-11-2018"
__status__ = "Production"

#imports

#+ standard libraries

import importlib
import sys
import collections

#functions

def import_module(strPath, strAlias = None, dictGlobals = None):
    """
    Dynamic import of a module, optionally, with aliasing of its name. In order
    to place the reference to the imported module into the global symbol table
    of the caller's module such table must be passed as the keyword argument
    'dictGlobals' or a the third positional argument; otherwise the reference
    to the module is placed into the global symbol table of the module
    fsio_lib.dynamic_import itself.
    
    Example:
        import_module('library.package.module', dictGlobals = globals())
            ~ is equivalent to ~
                import library.package.module
        MyModule =import_module('library.package.module', dictGlobals=globals())
            ~ is equivalent to ~
                import library.package.module
                MyModule = library.package.module
        import_module('library.package.module', 'Alias', globals())
            ~ is equivalent to ~
                import library.package.module as Alias
        MyModule = import_module('library.package.module', 'Alias', globals())
            ~ is equivalent to ~
                import library.package.module as Alias
                MyModule = Alias
    
    Signature:
        str/, str, dict/ -> __builtins__.module
    
    Args:
        strPath: string, path to a module, e.g. 'library.package.module'
        strAlias: (optional) string, alias to be assigned to the imported module
        dictGlobals: (optional) dictionary representing the global symbol table
    
    Returns:
        __builtins__.module: a reference to the imported module
    
    Raises:
        TypeError: passed path to the module is not a string; or passed alias is
            not a string or None;  or the passed global symbols table is not a
            dictionary or None
        ImportError: required module is not found
    
    Version 0.1.0.0
    """
    #input data sanity checks
    if not isinstance(strPath, basestring):
        strError = '{} of {} is not a string'.format(strPath, type(strPath))
        raise TypeError(strError)
    if (not (strAlias is None)) and (not isinstance(strAlias, basestring)):
        strError = '{} of {} is not a string'.format(strAlias, type(strAlias))
        raise TypeError(strError)
    if (not (dictGlobals is None)) and (not isinstance(dictGlobals,
                                                        collections.Mapping)):
        strError = '{} of {} is not a dictionary'.format(dictGlobals,
                                                            type(dictGlobals))
        raise TypeError(strError)
    #actual job
    if dictGlobals is None:
        dictGlobals = globals()
    modModule = importlib.import_module(strPath)
    if strAlias is None:
        strName = strPath.split('.')[0]
        dictGlobals[strName] = sys.modules[strName]
    else:
        dictGlobals[strAlias] = modModule
    return modModule

def import_from_module(strPath, strName, strAlias = None, dictGlobals = None):
    """
    Dynamic import of an object from a module, optionally, with aliasing of its
    name. In order to place the reference to the imported object into the global
    symbol table of the caller's module such table must be passed as the keyword
    argument 'dictGlobals' or a the fourth positional argument; otherwise the
    reference to the object is placed into the global symbol table of the module
    fsio_lib.dynamic_import itself.
    
    Example:
        import_from_module('library.module', 'SomeClass', dictGlobals=globals())
            ~ is equivalent to ~
                from library.module import SomeClass
        MyClass=import_from_module('library', 'S_Class', dictGlobals=globals())
            ~ is equivalent to ~
                from library import S_Class
                MyClass = S_Class
        import_from_module('library', 'SomeClass', 'Alias', globals())
            ~ is equivalent to ~
                from library import SomeClass as Alias
        MyClass = import_module('library', 'SomeClass', 'Alias', globals())
            ~ is equivalent to ~
                from library import SomeClass as Alias
                MyClass = Alias
    
    Signature:
        str, str/, str, dict/ -> type A
    
    Args:
        strPath: string, path to a module, e.g. 'library.package.module'
        strName: name of an object defined in the module, e.g. 'SomeClass'
        strAlias: (optional) string, alias to be assigned to the imported object
        dictGlobals: (optional) dictionary representing the global symbol table
    
    Returns:
        type A: a reference to the imported object
    
    Raises:
        TypeError: passed path to the module is not a string; or passed name of
            the object is not a string; or the passed alias is not a string or
            None; or the passed global symbols table is not a dictionary or None
        ImportError: required module is not found
        AttributeError: required object is not found in the module
    
    Version 0.1.0.0
    """
    #input data sanity checks
    if not isinstance(strPath, basestring):
        strError = '{} of {} is not a string'.format(strPath, type(strPath))
        raise TypeError(strError)
    if not isinstance(strName, basestring):
        strError = '{} of {} is not a string'.format(strName, type(strName))
        raise TypeError(strError)
    if (not (strAlias is None)) and (not isinstance(strAlias, basestring)):
        strError = '{} of {} is not a string'.format(strAlias, type(strAlias))
        raise TypeError(strError)
    if (not (dictGlobals is None)) and (not isinstance(dictGlobals,
                                                        collections.Mapping)):
        strError = '{} of {} is not a dictionary'.format(dictGlobals,
                                                            type(dictGlobals))
        raise TypeError(strError)
    #actual job
    if dictGlobals is None:
        dictGlobals = globals()
    gObject = getattr(importlib.import_module(strPath), strName)
    if strAlias is None:
        dictGlobals[strName] = gObject
    else:
        dictGlobals[strAlias] = gObject
    return gObject