#!/usr/bin/python
"""
Module fsio_lib.StructureMapping

Implements functions for mapping the content of a nested C struct (or Pascal
record) like objects, nested dictionaries, nested sequences or even XML
representation objects (xml.etree.ElementTree.Element class) onto another object
of one of these types using defined templates.

Functions:
    FlattenPath()
        type A -> list(int OR str OR dict(str : int OR float OR str OR bool))
    ResolvePathSubstitutions()
        dict(str : type A) ->
            dict(str:list(int OR str OR dict(str:int OR float OR str OR bool)))
    GetElement()
        type A, type B -> type C
    SetElement()
        type A, type B, type C -> None
    DeleteElement()
        type A, type B -> None
    AddElement()
        type A, type B, type C -> None
    LoadDefinition()
        str/, logging.Logger OR 'LoggingFSIO.ConsoleLogger/ -> dict
    MapValues()
        type A, type B, dict/, logging.Logger OR
            'fsio_lib.LoggingFSIO.ConsoleLogger, bool, bool, bool/ -> None
"""

__version__ = "0.1.0.0"
__date__ = "31-10-2018"
__status__ = "Production"

__all__ = ["FlattenPath", "ResolvePathSubstitutions", "GetElement", "MapValues",
            "SetElement", "DeleteElement", "AddElement", "LoadDefinition"]
#to prevent 'private' functions import with the 'import *' construct

#imports

#+ standard libraries

import os
import collections
import xml.etree.ElementTree as ElementTree
import json
import string

#functions

#+ atomic operation functions

def FlattenPath(gPath):
    """
    Flattens and unifies the path to an element / attribute of an object by
    converting it into a a flat list (without nesting) with each element being
    either a number or a string or a dictionary of string keys and numeric /
    boolean / string values. A string containg a dot notation path to an element
    / attribute is converted into a list of strings with each consecutive
    element referencing the corresponding level of the nesting.
    
    Signature:
        type A -> list(int OR str OR dict(str : int OR float OR str OR bool))
    
    Args:
        gPath: type A, a path or a single element of a path to be flatten and
            unified, can be an integer or string or a dictionary of string keys
            and numeric / boolean / string values or a (nested) sequence of
            these types
    
    Returns:
        list(): a flat list (without nesting) with each element being either a
            number or a string or a dictionary of string keys and numeric /
            boolean / string values
    
    Raises:
        TypeError: the input argument is not of the allowed type
        ValueError: negative index (integer path element) or an empty string,
            (nested) sequence or choice dictionary or part of the dot notation
            path reference is found to be empty
    
    Version 0.1.0.0
    """
    if isinstance(gPath, basestring):
        if gPath.startswith('#') or gPath.startswith('$'):
            if gPath == '#' or gPath == '$':
                strError = 'Empty name {}'.format(gPath)
                raise ValueError(strError)
            glstResult = [gPath]
        else:
            glstResult = gPath.split(".")
            if any(map(lambda x: not len(x), glstResult)):
                strError = 'Empty name (in) {}'.format(gPath)
                raise ValueError(strError)
    elif isinstance(gPath, (int, long)) and not isinstance(gPath, bool):
        if gPath < 0:
            strError = "Negative index {}".format(gPath)
            raise ValueError(strError)
        glstResult = [gPath]
    elif isinstance(gPath, collections.Mapping):
        if not len(gPath):
            strError = 'Empty choice element dictionary'
            raise ValueError(strError)
        for gKey, gValue in gPath.items():
            if not isinstance(gKey, basestring):
                strError = "Not a string key {} {} in dictionary {}".format(
                                                        gKey, type(gKey), gPath)
                raise TypeError(strError)
            if not isinstance(gValue, (basestring, int, float, long)):
                strError = "Not allowed {} value of key {} in dict {}".format(
                                                    type(gValue), gKey, gPath)
                raise TypeError(strError)
        glstResult = [gPath]
    elif isinstance(gPath, collections.Sequence):
        if not len(gPath):
            strError = 'Empty path elements sequence'
            raise ValueError(strError)
        glstResult = []
        for gItem in gPath:
            glstResult.extend(FlattenPath(gItem))
    else:
        strError = 'Not allowed type {} of the path (element) {}'.format(
                                                            type(gPath), gPath)
        raise TypeError(strError)
    return glstResult

def ResolvePathSubstitutions(dictPaths):
    """
    Resolves and converts to the flat list format the path substitution
    definitions passed as a dictionary. Any path substitution definition may
    refer another substitution definition as long as the circular dependence is
    avoided.
    
    Proper definition:
        * {"$1" : "a", "$2" : "b", "$3" : ["$1", "$2"], "$4" : ["$3", "c"]}
        * => {"$1": ["a"], "$2": ["b"], "$3": ["a", "b"], "$4": ["a", "b", "c"]}
    Improper definitions:
        * {"$1" : "a", "$3" : "$2"} - missing definition of "$2"
        * {"$1" : "a", "$2" : "$3", "$3" : "$2"} - circular dependence
    
    Signature:
        dict(str : type A) ->
            dict(str:list(int OR str OR dict(str:int OR float OR str OR bool)))
    
    Args:
        dictPaths: dict(str : type A), dictionary of string keys (pattern names)
            and values being proper path to an element descriptions
    
    Returns:
        dict(): dictionary of the same keys but values being fully resolved and
            flattened paths to elements / attributes
    
    Raises:
        TypeError: either at least one key is not a string or at least one value
            of the input dictionary is not a proper path definition, or the
            received argument is not a dictionary
        ValueError: at least one element of at least one path definition is a
            negative index (integer path element) or an empty string, (nested)
            sequence or choice dictionary or part of the dot notation path
            reference is found to be empty; or there is a circular definition 
            of patterns, or a missing pattern definition
    
    Version 0.1.0.0
    """
    if not isinstance(dictPaths, collections.Mapping):
        strError = 'Inproper argument {} of {} - must be a dictionary'.format(
                                                    dictPaths, type(dictPaths))
        raise TypeError(strError)
    dictResolved = {}
    dictUnresolved = {}
    for Key, Value in dictPaths.items():
        if not isinstance(Key, basestring):
            strError = 'Improper key {} in path substitutions {}'.format(
                                                        type(Key), dictPaths)
            raise TypeError(strError)
        if not _IsPathKey(Key):
            strError = 'Improper key {} in path substitutions {}'.format(Key,
                                                                    dictPaths)
            raise ValueError(strError)
        glstTemp = FlattenPath(Value)
        bCond1 = any(map(_IsPathKey, glstTemp))
        if bCond1:
            bCond2 = any(map(lambda x: _IsPathKey(x) and (not (x in dictPaths)),
                                                                    glstTemp))
            if bCond2:
                strError ='Undefined pattern in {} in {}'.format(Key, dictPaths)
                raise ValueError(strError)
            dictUnresolved[Key] = glstTemp
        else:
            dictResolved[Key] = glstTemp
    while len(dictUnresolved):
        strlst2Remove = []
        for Key, Value in dictUnresolved.items():
            glstTemp = []
            for gItem in Value:
                if isinstance(gItem, basestring) and (gItem in dictResolved):
                    glstTemp.append(dictResolved[gItem])
                else:
                    glstTemp.append(gItem)
            glstTemp = FlattenPath(glstTemp)
            if not any(map(lambda x: isinstance(x, basestring) and (
                                                    x in dictPaths), glstTemp)):
                dictResolved[Key] = glstTemp
                strlst2Remove.append(Key)
        for Key in strlst2Remove:
            del dictUnresolved[Key]
        if not len(strlst2Remove):
            strError = 'Circular dependencies {} in {}'.format(dictUnresolved,
                                                                    dictPaths)
            raise ValueError(strError)
    return dictResolved

def GetElement(objTarget, glstPath):
    """
    Extracts a value of an arbitrary level deep nested element of an object.
    
    Flattens and unifies the path to an element / attribute of an object by
    converting it into a a flat list (without nesting) with each element being
    either a number or a string or a dictionary of string keys and numeric /
    boolean / string values. A string containg a dot notation path to an element
    / attribute is converted into a list of strings with each consecutive
    element referencing the corresponding level of the nesting.
    
    After that attempts to find the corresponding element of the object by
    walking along the flattened / unified path. If the corresponding element is
    found it is converted into int or float if possible (only for string values)
    and returned. If any of the nested elements along the path does not exist,
    the AttributeError exception is raised.
    
    Specifically for the xml.etree.ElementTree.Element instance objects:
    
    * Resolution order by the name (string path element)
        - Special attributes: "tag", "text" and "tail"
        - Children sub-elements by their tags
        - Normal attributes of the node itself by their names
    * When looking by an integer index or properties ("choice") dictionary only
        the direct children sub-elements are concerned
    
    Signature:
        type A, type B -> type C
    
    Args:
        objTarget: type A, the target object, from which the value of an element
            is to be obtained, supposedly C-struct like object or a sequence
            (container), or a dictionary (mapping type), or an XML file content
            representation (xml.etree.ElementTree.Element)
        glstPath: type B, a path or a single element of a path to be flatten and
            unified, can be an integer or string or a dictionary of string keys
            and numeric / boolean / string values or a (nested) sequence of
            these types
    
    Returns:
        type C: the value of the corresponding nested element, the numbers
            (floating point or integer) stored in a string are converted into
            float and int respectively.
    
    Raises:
        TypeError: the second input argument is not of the allowed type
        ValueError: the second input argument is not of the allowed values
        AttributeError: any of the (nested) elements along the path is not found
            in the object
    
    Version 0.1.0.0
    """
    _glstPath = FlattenPath(glstPath)
    objTemp = objTarget
    for iIndex, gItem in enumerate(_glstPath):
        strError = 'Object {} has no element index {} in path {}'.format(
                                                objTarget, iIndex, _glstPath)
        if isinstance(gItem, basestring):
            if isinstance(objTemp, ElementTree.Element):
                if gItem in ['text', 'tail', 'tag']:
                    objTemp = getattr(objTemp, gItem)
                elif any(map(lambda x: x.tag == gItem, list(objTemp))):
                    objTemp = objTemp.find(gItem)
                elif gItem in objTemp.attrib:
                    objTemp = objTemp.get(gItem)
                else:
                    raise AttributeError(strError) 
            elif isinstance(objTemp, collections.Mapping):
                if not (gItem in objTemp):
                    raise AttributeError(strError)
                objTemp = objTemp[gItem]
            else:
                if hasattr(objTemp, gItem):
                    objTemp = getattr(objTemp, gItem)
                else:
                    raise AttributeError(strError)
        elif isinstance(gItem, (int, long)):
            if (isinstance(objTemp, (ElementTree.Element, collections.Sequence))
                                    and (not isinstance(objTemp, basestring))):
                try:
                    objTemp = list(objTemp)[gItem]
                except IndexError:
                    raise AttributeError(strError)
            else:
                raise AttributeError(strError)
        elif isinstance(gItem, collections.Mapping):
            if (isinstance(objTemp, (ElementTree.Element, collections.Sequence))
                                    and (not isinstance(objTemp, basestring))):
                objFound = None
                for objElement in list(objTemp):
                    bEqual = False
                    for Key, Value in gItem.items():
                        try:
                            bEqual = (Value == GetElement(objElement, [Key]))
                        except AttributeError:
                            pass
                        if not bEqual:
                            break
                    if bEqual:
                        objFound = objElement
                        break
                if not (objFound is None):
                    objTemp = objFound
                else:
                    raise AttributeError(strError)
            else:
                raise AttributeError(strError)
        else:
            raise AttributeError(strError)
    if isinstance(objTemp, basestring):
        try:
            objTemp = int(objTemp)
        except (ValueError, TypeError):
            try:
                objTemp = float(objTemp)
            except (ValueError, TypeError):
                pass
    return objTemp
    
def SetElement(objTarget, glstPath, gValue):
    """
    Assigns a value to an arbitrary level deep nested element of an object if
    such element is found within the object
    
    Flattens and unifies the path to an element / attribute of an object by
    converting it into a a flat list (without nesting) with each element being
    either a number or a string or a dictionary of string keys and numeric /
    boolean / string values. A string containg a dot notation path to an element
    / attribute is converted into a list of strings with each consecutive
    element referencing the corresponding level of the nesting.
    
    After that attempts to find the corresponding element of the object by
    walking along the flattened / unified path. If the corresponding element is
    found the new value is assigned to it. If any of the nested elements along
    the path does not exist, the AttributeError exception is raised.
    
    Specifically for the xml.etree.ElementTree.Element instance objects:
    
    * Resolution order by the name (string path element)
        - Special attributes: "tag", "text" and "tail"
        - Children sub-elements by their tags
        - Normal attributes of the node itself by their names
    * When looking by an integer index or properties ("choice") dictionary only
        the direct children sub-elements are concerned
    * An XML node object (as the new value) can only replace an existing
        sub-element of an XML node, but not the value of its attribute
    
    Signature:
        type A, type B, type C -> None
    
    Args:
        objTarget: type A, the target object, from which the value of an element
            is to be set, supposedly C-struct like object or a sequence
            (container), or a dictionary (mapping type), or an XML file content
            representation (xml.etree.ElementTree.Element)
        glstPath: type B, a path or a single element of a path to be flatten and
            unified, can be an integer or string or a dictionary of string keys
            and numeric / boolean / string values or a (nested) sequence of
            these types
        gValue: type C, the value to be assigned to the element (if found)
    
    Raises:
        TypeError: the second input argument is not of the allowed type, or an
            XML node object is attempted to be assigned as an attribute of
            another XML node object (not as a sub-element), or a non XML node is
            attempted to be assigned to a sub-element of an XML node, or an
            immutable sequence as the last element is attempted to be modified
        ValueError: the second input argument is not of the allowed values
        AttributeError: any of the (nested) elements along the path is not found
            in the object
    
    Version 0.1.0.0
    """
    _glstPath = FlattenPath(glstPath)
    GetElement(objTarget, _glstPath) #as sanity check on the path and elements
    if len(_glstPath) > 1:
        objTemp = GetElement(objTarget, _glstPath[:-1])
    else:
        objTemp = objTarget
    gItem = _glstPath[-1]
    strError = 'Cannot assign {} to element {} of {}'.format(gValue, _glstPath,
                                                                    objTarget)
    if isinstance(gItem, basestring):
        if isinstance(objTemp, ElementTree.Element):
            if not isinstance(gValue, ElementTree.Element):
                if gItem in ['text', 'tail', 'tag']:
                    setattr(objTemp, gItem, str(gValue))
                elif gItem in objTemp.attrib:
                    objTemp.set(gItem, str(gValue))
                else:
                    raise TypeError(strError)
            else:
                objChild = objTemp.find(gItem)
                if not (objChild is None):
                    for iIndex, objNode in enumerate(list(objTemp)):
                        if objNode is objChild:
                            break
                    objTemp.remove(objChild)
                    del objChild
                    objTemp.insert(iIndex, gValue)
                else:
                    raise TypeError(strError)
        elif isinstance(objTemp, collections.Mapping):
            objTemp[gItem] = gValue
        else:
            setattr(objTemp, gItem, gValue)
    elif isinstance(gItem, (int, long)):
        if isinstance(objTemp, ElementTree.Element):
            if isinstance(gValue, ElementTree.Element):
                objChild = list(objTemp)[gItem]
                objTemp.remove(objChild)
                del objChild
                objTemp.insert(gItem, gValue)
            else:
                raise TypeError(strError)
        else:
            objTemp[gItem] = gValue
    else: #dictionary path element!
        objChild = GetElement(objTemp, gItem)
        for iIndex, objNode in enumerate(list(objTemp)):
            if objNode is objChild:
                break
        if isinstance(objTemp, ElementTree.Element): #XML sub-element!
            if isinstance(gValue, ElementTree.Element):
                objTemp.remove(objChild)
                del objChild
                objTemp.insert(iIndex, gValue)
            else:
                raise TypeError(strError)
        else: #element of sequence
            try:
                objTemp[iIndex] = gValue
            except TypeError: #immutable sequence
                raise TypeError(strError)

def DeleteElement(objTarget, glstPath):
    """
    Deletes an arbitrary level deep nested element of an object if such element
    is found within the object
    
    Flattens and unifies the path to an element / attribute of an object by
    converting it into a a flat list (without nesting) with each element being
    either a number or a string or a dictionary of string keys and numeric /
    boolean / string values. A string containg a dot notation path to an element
    / attribute is converted into a list of strings with each consecutive
    element referencing the corresponding level of the nesting.
    
    After that attempts to find the corresponding element of the object by
    walking along the flattened / unified path. If the corresponding element is
    found the new value is assigned to it. If any of the nested elements along
    the path does not exist, the AttributeError exception is raised.
    
    Specifically for the xml.etree.ElementTree.Element instance objects:
    
    * Resolution order by the name (string path element)
        - Special attributes: "tag", "text" and "tail"
        - Children sub-elements by their tags
        - Normal attributes of the node itself by their names
    * When looking by an integer index or properties ("choice") dictionary only
        the direct children sub-elements are concerned
    * The 'text' and 'tail' attributes are not deleted, but set to None
    * The 'tag' of the node is not deleted but set to 'def_node', i.e. the node
        is simply renamed to the 'def_node'; whereas the path ending in the name
        (tag) of a node but not in the string 'tag' results in the complete
        deletion of this node
    
    Signature:
        type A, type B -> None
    
    Args:
        objTarget: type A, the target object, from which the an element is to be
            deleted, supposedly C-struct like object or a sequence (container),
            or a dictionary (mapping type), or an XML file content
            representation (xml.etree.ElementTree.Element)
        glstPath: type B, a path or a single element of a path to be flatten and
            unified, can be an integer or string or a dictionary of string keys
            and numeric / boolean / string values or a (nested) sequence of
            these types
    
    Raises:
        TypeError: the second input argument is not of the allowed type
        ValueError: the second input argument is not of the allowed values
        AttributeError: any of the (nested) elements along the path is not found
            in the object
    
    Version 0.1.0.0
    """
    _glstPath = FlattenPath(glstPath)
    GetElement(objTarget, _glstPath) #as sanity check on the path and elements
    if len(_glstPath) > 1:
        objTemp = GetElement(objTarget, _glstPath[:-1])
    else:
        objTemp = objTarget
    gItem = _glstPath[-1]
    if isinstance(objTemp, ElementTree.Element):
        if isinstance(gItem, basestring):
            if gItem in ['text', 'tail']:
                setattr(objTemp, gItem, None)
            elif gItem == 'tag':
                setattr(objTemp, gItem, 'def_node')
            elif gItem in [objItem.tag for objItem in list(objTemp)]:
                objChild = objTemp.find(gItem)
                objTemp.remove(objChild)
                del objChild
            else:
                objTemp.attrib.pop(gItem, None)
        elif isinstance(gItem, (int, long)):
            objChild = list(objTemp)[gItem]
            objTemp.remove(objChild)
            del objChild
        else:
            objChild = GetElement(objTemp, gItem)
            objTemp.remove(objChild)
            del objChild
    elif isinstance(objTemp, (collections.Mapping, collections.Sequence)):
        #due to the sanity check above, for mapping type the last element can
        #+ be only a proper key, and for sequence - the proper index; the
        #+ objects can be immutable, so the TypeError can be raised
        if isinstance(gItem, (basestring, int, long)):
            del objTemp[gItem]
        else: #dictionary -> only for sequences!
            objChild = GetElement(objTemp, gItem)
            iIndex = objTemp.index(objChild)
            del objTemp[iIndex]
    else:
        delattr(objTemp, gItem)

def AddElement(objTarget, glstPath, gValue):
    """
    Assigns a value to an arbitrary level deep nested element of an object if
    such element is found within the object (overwrites) or attempts to create
    a new nested element with all missing 'parent' nodes along the path as well.
    
    Flattens and unifies the path to an element / attribute of an object by
    converting it into a a flat list (without nesting) with each element being
    either a number or a string or a dictionary of string keys and numeric /
    boolean / string values. A string containg a dot notation path to an element
    / attribute is converted into a list of strings with each consecutive
    element referencing the corresponding level of the nesting.
    
    An empty path ('', [], etc. OR None) is acceptable only for the XML node
    target object with the new value also being an XML node.
    
    After that attempts to find the corresponding element of the object by
    walking along the flattened / unified path. If the corresponding element is
    found the new value is assigned to it. If any of the 'parent' node is
    missing along the path, the function attempts to create the missing nodes
    based on the type of the target object and the structure of the path.
    
    The general rules applied are:
    
    * The path may refer to an excisting element, in which case its value is
        overwritten using SetElement() function
    * The path may refer to a not yet existing element, but at least part of it
        (the first one or several elements) may refer to an existing
        intermediate element, to which a new branch will be attached
    * The existing elements / levels part of the path may include numeric
        indexes and 'choice' dictionaries up to the 'branching' point, but not
        after the 'branching' point -  only the string names; otherwise, the
        AttributeError exception is raised
    * For non XML target objects: all but the last missing elements / levels are
        created as nested dictionaries paired to as values to the keys with the
        names taken from the 'missing' path elements (strings); whereas the last
        element in the 'missing' path is used as the key in the deepest nested
        dictionary and the passed value as its paired value
        - Inability to attach the created branch results in the AttributeError
    * For the XML target objects: all but the last missing elements / levels are
        created as nested XML nodes using the names taken from the 'missing'
        path elements (strings) as their tags, and
        - if the passed value is an XML node itself, an extra nesting level
            node is added with the tag being the last element in the 'missing'
            path, and the passed value is attached as a node to this deepest
            nested created node
        - if the passed value is not an XML node, the value of the element in
            the 'missing' path is used as the attribute name, and the passed
            value converted to string as its value, and this attribute is
            attached to the deepest nested created node
    
    Specifically for the xml.etree.ElementTree.Element instance objects:
    
    * Resolution order by the name (string path element)
        - Special attributes: "tag", "text" and "tail"
        - Children sub-elements by their tags
        - Normal attributes of the node itself by their names
    * When looking by an integer index or properties ("choice") dictionary only
        the direct children sub-elements are concerned
    * An XML node object can be directly attached to another XML node (as root)
        using the 'empty' path (empty string, empty sequence or None) - this is
        the only exception of the general rule on the values of the path
        elements
    * A special or normal attribute can be added only to a node
    * If the 'branching' point (deepest exisiting element along the path) is not
        a node - the AttributeError exception is raised
    
    Signature:
        type A, type B, type C -> None
    
    Args:
        objTarget: type A, the target object, supposedly C-struct like object or
            a sequence (container), or a dictionary (mapping type), or an XML
            file content representation (xml.etree.ElementTree.Element)
        glstPath: type B, a path or a single element of a path to be flatten and
            unified, can be an integer or string or a dictionary of string keys
            and numeric / boolean / string values or a (nested) sequence of
            these types
        gValue: type C, the value to be assigned to the end-path element
    
    Raises:
        TypeError: the second input argument (path)is not of the allowed type,
            or an XML node object is attempted to be assigned as an attribute of
            another XML node object (not as a sub-element), or a non XML node is
            attempted to be assigned to a sub-element of an XML node, or an
            immutable object is attempted to be modified - in case of the
            existing end-element being overwritten
        ValueError: the second input argument (path) is not of the allowed
            values, or an 'empty' path is used not with the target object and
            new values both being XML nodes
        AttributeError: the 'missing' part of the path after the 'branching'
            point contains integer indexes or 'choice' dictionaries, or the
            'branching' point is an immutable object / not XML node (attribute)
    
    Version 0.1.0.0
    """
    bCond1 = isinstance(glstPath, collections.Sequence) and (not len(glstPath))
    if bCond1 or (glstPath is None):
        if (isinstance(objTarget, ElementTree.Element)
                                and isinstance(gValue, ElementTree.Element)):
            objTarget.append(gValue)
        else:
            strError = 'Only XML node can be added to an XML node without path'
            raise ValueError(strError)
    else:
        glstPath = FlattenPath(glstPath) #also as a sanity check on the path!
        try:
            SetElement(objTarget, glstPath, gValue) #overwrite existing
        except AttributeError: #or create along the path!
            objCurrentLevel = objTarget
            iCurrentIndex = 0
            while iCurrentIndex < len(glstPath) - 1:
                gCurrentPathItem = glstPath[iCurrentIndex]
                try:
                    objCurrentLevel = GetElement(objCurrentLevel,
                                                            gCurrentPathItem)
                    #existing level -> go to the next
                    iCurrentIndex += 1
                except AttributeError: #missing level - create from here!
                    break
            #found the deepest existing 
            glstRemainingPath = glstPath[iCurrentIndex:]
            if any(map(lambda x: not isinstance(x, basestring),
                                                            glstRemainingPath)):
                strError = 'Not a name in the path {}, full path {}'.format(
                                                    glstRemainingPath, glstPath)
                raise AttributeError(strError)
            #only names remain in the missing part of the path
            #build-down the branch from the last existing element and attach
            if isinstance(objTarget, ElementTree.Element): #XML
                if not isinstance(objCurrentLevel, ElementTree.Element):
                    strError = 'Not a node at {} in {}'.format(
                                            glstPath[:iCurrentIndex], objTarget)
                    raise AttributeError(strError)
                for strName in glstRemainingPath[:-1]:
                    objCurrentLevel = ElementTree.SubElement(objCurrentLevel,
                                                                        strName)
                strName = glstRemainingPath[-1]
                if isinstance(gValue, ElementTree.Element):
                    objCurrentLevel = ElementTree.SubElement(objCurrentLevel,
                                                                        strName)
                    objCurrentLevel.append(gValue)
                else:
                    if gValue is ['text', 'tail', 'tag']:
                        setattr(objCurrentLevel, strName, str(gValue))
                    else:
                        objCurrentLevel.set(strName, str(gValue))
            else: #non XML
                bIsSequence = (isinstance(objCurrentLevel, collections.Sequence)
                            and (not isinstance(objCurrentLevel, basestring)))
                if bIsSequence:
                    iStartIndex = 0
                else:
                    iStartIndex = 1
                if iStartIndex < len(glstRemainingPath):
                    objBranch = dict()
                    objCurrentNode = objBranch
                    for strName in glstRemainingPath[iStartIndex:-1]:
                        objCurrentNode[strName] = dict()
                        objCurrentNode = objCurrentNode[strName]
                    objCurrentNode[glstRemainingPath[-1]] = gValue
                else:
                    objBranch = gValue
                strError = 'Immutable element at {} in {}'.format(
                                            glstPath[:iCurrentIndex], objTarget)
                try:
                    if iStartIndex:
                        if isinstance(objCurrentLevel, collections.Mapping):
                            objCurrentLevel[glstRemainingPath[0]] = objBranch
                        else:
                            setattr(objCurrentLevel, glstRemainingPath[0],
                                                                    objBranch)
                    else:
                        objCurrentLevel.append(objBranch)
                except (TypeError, AttributeError): #immutable object
                    raise AttributeError(strError)

#+ 'private' helper functions -> should not be visible of import *

def _IsIdentifier(gValue):
    """
    Checks if the passed argument is a string and a proper Python identifier,
    except for a sole underscore ('_').
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    strFirstChar = '_' + string.lowercase + string.uppercase
    strNextChar = strFirstChar + string.digits
    if isinstance(gValue, basestring):
        if gValue == '' or gValue == '_':
            bResult = False
        else:
            bResult = gValue[0] in strFirstChar
            if len(gValue) > 1:
                bResult = bResult and all(strChar in strNextChar
                                                    for strChar in gValue[1:])
    else:
        bResult = False
    return bResult

def _IsNumberString(gValue):
    """
    Checks if the passed argument is a non-negative integer number wrapped in a
    string.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    return (isinstance(gValue, basestring) and gValue.isdigit())

def _IsProperKey(gValue):
    """
    Checks if the passed argument is a proper key for an entry in the mapping
    definition dictionary (not the top level / extras) according to DSL, i.e.
    either a proper Python identifier (except for '_') or a non-negative integer
    number wrapped in a string.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    return (_IsIdentifier(gValue) or _IsNumberString(gValue))

def _IsPathKey(gValue):
    """
    Checks if the passed argument is a proper key for an entry in the path
    substitution definitions dictionary, i.e. a string > 1 character long and
    with the first character '$'.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    bResult = (isinstance(gValue, basestring) and len(gValue) > 1
                                                    and gValue.startswith('$'))
    return bResult

def _IsIncludeKey(gValue):
    """
    Checks if the passed argument is a proper key for an entry in the value
    substitution definitions dictionary, i.e. a string > 1 character long and
    with the first character '#'.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    bResult = (isinstance(gValue, basestring) and len(gValue) > 1
                                                    and gValue.startswith('#'))
    return bResult

def _IsAdditionKey(gValue):
    """
    Checks if the passed argument is a proper key for an entry in the
    incremental addition definition, i.e. a string > 1 character long and with
    the first character '+'.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    bResult = (isinstance(gValue, basestring) and len(gValue) > 1
                                                    and gValue.startswith('+'))
    return bResult

def _IsRemovalKey(gValue):
    """
    Checks if the passed argument is a proper key for an entry in the
    incremental removal definition, i.e. a string > 1 character long and with
    the first character '-'.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    bResult = (isinstance(gValue, basestring) and len(gValue) > 1
                                                    and gValue.startswith('-'))
    return bResult

def _IsRuleName(gValue):
    """
    Checks if the passed argument is a proper key for the top level entry in the
    mapping definition, i.e. a string >= 1 character long and not a key for the
    path / value substitution definitions or incremental addition / deletion.
    
    Signature:
        type A -> bool
    
    Args:
        gValue: type A, the value to check
    
    Returns:
        bool: result of the check True / False
    
    Version 0.1.0.0
    """
    bResult = (isinstance(gValue, basestring) and len(gValue) >= 1 and
                gValue != '_' and (not _IsAdditionKey(gValue))
                    and (not _IsRemovalKey(gValue))
                        and (not _IsIncludeKey(gValue))
                            and (not _IsPathKey(gValue))
                                and (not gValue in ['PATHS', 'INCLUDES']))
    return bResult

def _LogAndRaise(strMessage, clsException, objLogger= None, objOriginal= None):
    """
    Helper function to (re-) raise an exception of specific class with the
    provided error message. If a logger object is provided, the raised exception
    is logged with its help before the exception is raised. If the instance of
    the 'original' (caught) exception is provided, its type (class name) and
    message are also included into the error message.
    
    Signature:
        str, class 'Exception/, logging.Logger OR 'LoggingFSIO.ConsoleLogger,
            'Exception/ -> None
    
    Args:
        strMessage: str, the customer provided error message
        clsException: class 'Exception, type (class) of the exception to be
            raised
        objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
            instance of, the logger object with standard API
        objOriginal: (optional) 'Exception, an instance of any exception class,
            the originally raised and caught exception
    
    Raises:
        'Exception: the required exception class instance
    
    Version 0.1.0.0
    """
    strExtra = ''
    if not (objOriginal is None):
        if isinstance(objOriginal, (IOError, OSError)):
            strExtra = '({}: {} {}) => '.format(objOriginal.__class__.__name__,
                                        objOriginal.errno, objOriginal.strerror)
        elif isinstance(objOriginal, Exception):
            strExtra = '({}: {}) => '.format(objOriginal.__class__.__name__,
                                                            objOriginal.message)
    strErrorMessage = '{}{}'.format(strExtra, strMessage)
    if not (objLogger is None):
        strLogMessage = '{}: {}'.format(clsException.__name__, strErrorMessage)
        objLogger.error(strLogMessage)
    raise clsException(strErrorMessage)

def _ExtractPathSubstitutions(dictBuffer):
    """
    Extracts the path substitions dictionary from the dictionary data loaded
    from a file - the entry is removed! Resolves all path substitution
    definitions into the proper flattend paths to an attribute, and returns them
    as a plain dictionary using the function ResolvePathSubstitutions(). Note,
    the returned dicitonary is empty if there was no path substitutions
    dictionary in the passed dictionary (bound to the special key 'PATHS').
    
    Signature:
        dict(str : type A) ->
            dict(str:list(int OR str OR dict(str:int OR float OR str OR bool)))
    
    Args:
        dictBuffer: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
    
    Returns:
        dict(): dictionary of the string keys and values being fully resolved
            and flattened paths to elements / attributes - the path substituions
    
    Raises:
        TypeError: either at least one key is not a string or at least one value
            of the paths dictionary is not a proper path definition, or the
            paths entry is not a dictionary
        ValueError: at least one element of at least one path definition is a
            negative index (integer path element) or an empty string, (nested)
            sequence or choice dictionary or part of the dot notation path
            reference is found to be empty; or there is a circular definition 
            of patterns, or a missing pattern definition
    
    Version 0.1.0.0
    """
    dictPaths = dictBuffer.get('PATHS', None)
    if not (dictPaths is None):
        dictSubstitutions = ResolvePathSubstitutions(dictPaths)
        del dictBuffer['PATHS']
    else:
        dictSubstitutions = dict()
    return dictSubstitutions

def _ExtractValueSubstitutions(dictBuffer, strFile, objLogger = None):
    """
    Extracts the value substitions dictionary from the dictionary data loaded
    from a file - the entry is removed! Loads the data from all referenced files
    and converts it into the proper mapping dictionaries by calling back the
    function LoadDefinition(). Since this function itself is called from the
    LoadDefinition(), the call chain is recursive. Returns a plain dictionary of
    the pattern names and their resolved values. Note, the returned dicitonary
    is empty if there was no value substitutions dictionary in the passed
    dictionary (bound to the special key 'INCLUDES').
    
    All entries loaded as 'extras' in the included files are converted into
    paths - mapping entries.
    
    Signature:
        dict(str : type A), str/, logging.Logger OR 'LoggingFSIO.ConsoleLogger/
            -> dict(str : type B)
    
    Args:
        dictBuffer: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
        strFile: str, path to the original file, which includes definitions from
            other files to be loaded
        objLogger: (optional) logging.Logger or 'LoggingFSIO.ConsoleLogger,
            instance of, a logger object compatible with the standard logger
            interface
    
    Returns:
        dict: the mapping rules dictionary conforming the DE001 DSL specs
    
    Raises:
        IOError: re-raised, some file I/O related problems
        OSError: re-raised, some file I/O related problems
        ValueError: the file is found, but it is not of a proper JSON format; OR
            the data read is not a dictionary; OR it does not comply with the
            mapping DSL specifications
    
    Version 0.1.0.0
    """
    dictIncludes = dictBuffer.get('INCLUDES', None)
    if not (dictIncludes is None):
        if not isinstance(dictIncludes, collections.Mapping):
            strError = ' '.join(['Improper type {}'.format(type(dictIncludes)),
                'for the values substitution entry in file {}'.format(strFile)])
            _LogAndRaise(strError, ValueError, objLogger)
        strFolder = os.path.dirname(os.path.abspath(strFile))
        dictSubstitutions = dict()
        for strKey, gValue in dictIncludes.items():
            if _IsIncludeKey(strKey):
                if isinstance(gValue, basestring):
                    dictTemp = LoadDefinition(os.path.join(strFolder, gValue),
                                                        objLogger = objLogger)
                    try:
                        if isinstance(dictTemp, collections.Mapping):
                            _WalkDict(dictTemp, {}, strFile,
                                                        objLogger = objLogger)
                        else:
                            dictTemp = FlattenPath(dictTemp)
                        dictSubstitutions[strKey] = dictTemp
                    except Exception as err:
                        strError  = ' '.join(['Not a proper value',
                            'substitution definition',
                            '{} : {} in file {}'.format(strKey,gValue,strFile)])
                        _LogAndRaise(strError, ValueError, objLogger, err)
                elif (isinstance(gValue, collections.Sequence) and
                                                            len(gValue) == 2):
                    dictTemp =LoadDefinition(os.path.join(strFolder, gValue[0]),
                                                        objLogger = objLogger)
                    try:
                        dictTemp = GetElement(dictTemp, gValue[1])
                        if isinstance(dictTemp, collections.Mapping):
                            _WalkDict(dictTemp, {}, strFile,
                                                        objLogger = objLogger)
                        else:
                            dictTemp = FlattenPath(dictTemp)
                        dictSubstitutions[strKey] = dictTemp
                    except Exception as err:
                        strError  = ' '.join(['Not a proper value',
                            'substitution definition',
                            '{} : {} in file {}'.format(strKey,gValue,strFile)])
                        _LogAndRaise(strError, ValueError, objLogger, err)
                else:
                    strError  = ' '.join(['Not a proper value',
                        'substitution definition',
                        '{} : {} in file {}'.format(strKey, gValue, strFile)])
                    _LogAndRaise(strError, ValueError, objLogger)
            else:
                strError  = ' '.join(['Not a proper value substitution name',
                    '{} in {} in file {}'.format(strKey, dictBuffer, strFile)])
                _LogAndRaise(strError, ValueError, objLogger)
        del dictBuffer['INCLUDES']
    else:
        dictSubstitutions = dict()
    return dictSubstitutions

def _ExtractExtras(dictBuffer):
    """
    Extracts all entries, which are 'extras', i.e. no substitutions are required
    - and removes the corresponding entries from the original dictionary.
    
    Signature:
        dict(str : type A) -> dict(str : real OR str)
    
    Args:
        dictBuffer: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
    
    Returns:
        dict: flat dictionary of string keys and numeric / string values
    
    Version 0.1.0.0
    """
    dictResult = dict()
    for Key, Value in dictBuffer.items():
        bCond1 = isinstance(Value, (int, long, float))
        bCond2 = (isinstance(Value, basestring) and len(Value) and
                            (not (_IsPathKey(Value) or _IsIncludeKey(Value))))
        bCond3 = _IsRuleName(Key)
        if (bCond1 or bCond2) and bCond3:
            dictResult[Key] = Value
    for strKey in dictResult:
        del dictBuffer[strKey]
    return dictResult

def _SelectDirectRules(dictBuffer):
    """
    Extracts all entries, which are considered to be mapping rules, but not the
    incremental changes to the rules. The extracted entries are removed from the
    original dictionary.
    
    Signature:
        dict(str : type A) -> dict(str : str OR dict)
    
    Args:
        dictBuffer: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
    
    Returns:
        dict: dictionary of string keys and string or dictionary values
    
    Version 0.1.0.0
    """
    dictResult = dict()
    for Key, Value in dictBuffer.items():
        bCond1 = (isinstance(Key, basestring) and len(Key) and
                    (not (_IsPathKey(Key) or _IsIncludeKey(Key) or
                            _IsAdditionKey(Key) or _IsRemovalKey(Key))))
        bCond2 = isinstance(Value, collections.Mapping)
        bCond3 = _IsIncludeKey(Value)
        if (bCond2 or bCond3) and bCond1:
            dictResult[Key] = Value
    for strKey in dictResult:
        del dictBuffer[strKey]
    return dictResult

def _SelectAdditionRules(dictBuffer, dictDirect):
    """
    Extracts all entries, which are considered to be the incremental additions
    to the already found 'direct' mapping rules. The extracted entries are
    removed from the original dictionary.
    
    Signature:
        dict(str : type A), dict(str : str OR dict) -> dict(str : str OR dict)
    
    Args:
        dictBuffer: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
        dictDirect: dict(str : str OR dict), dictionary of the already extracted
            'direct' mapping rules (for checks only)
    
    Returns:
        dict: dictionary of string keys and string or dictionary values
    
    Raises:
        ValueError: improper definition of an incremental addition
    
    Version 0.1.0.0
    """
    dictResult = dict()
    for Key, Value in dictBuffer.items():
        strError = 'Improper addition definition "{} : {}"'.format(Key, Value)
        bCond1 = _IsAdditionKey(Key) and Key[1:] in dictDirect
        bCond2 = isinstance(Value, collections.Mapping)
        if bCond1 and bCond2:
            bCond3 = all(map(lambda x: isinstance(x, collections.Mapping),
                                                                Value.values()))
            bCond4 = all(map(lambda x: _IsProperKey(x)
                    or (isinstance(x, (int, long))) and x >= 0, Value.keys()))
            if bCond3 and bCond4:
                dictResult[Key] = Value
            else:
                raise ValueError(strError)
        elif bCond1:
            raise ValueError(strError)
    for strKey in dictResult:
        del dictBuffer[strKey]
    return dictResult

def _SelectRemovalRules(dictBuffer, dictDirect):
    """
    Extracts all entries, which are considered to be the incremental removals
    from the already found 'direct' mapping rules. The extracted entries are
    removed from the original dictionary.
    
    Signature:
        dict(str : type A), dict(str : str OR dict) -> dict(str : list(type B))
    
    Args:
        dictBuffer: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
        dictDirect: dict(str : str OR dict), dictionary of the already extracted
            'direct' mapping rules (for checks only)
    
    Returns:
        dict: dictionary of string keys and entires defining a path according to
            the DE001 DSL specification as a list of allowed elements
    
    Raises:
        ValueError: improper definition of an incremental deletion
    
    Version 0.1.0.0
    """
    dictResult = dict()
    for Key, Value in dictBuffer.items():
        bCond1 = _IsRemovalKey(Key) and Key[1:] in dictDirect
        bCond2 = isinstance(Value, collections.Sequence)
        bCond3 = not isinstance(Value, basestring)
        strError = 'Not proper removal path "{} : {}"'.format(Key, Value)
        if bCond1 and bCond2 and bCond3:
            try:
                lstPath = FlattenPath(Value)
            except (TypeError, ValueError) as Err:
                strError = '{} - {}'.format(Err.message, strError)
                raise ValueError(strError)
            for gItem in lstPath:
                bCond1 = not _IsIdentifier(gItem)
                bCond2 = (not isinstance(gItem, (int, long)) or gItem < 0)
                if bCond1 and bCond2:
                    strError = " ".join(['Not proper element {}'.format(gItem),
                            'in removal path "{} : {}"'.format(Key, Value)])
                    raise ValueError(strError)
            dictResult[Key] = Value
        elif bCond1:
            raise ValueError(strError)
    for strKey in dictResult:
        del dictBuffer[strKey]
    return dictResult

def _WalkDict(dictTarget, dictSubstitutions, strFile, objLogger = None):
    """
    Recursive helper function, which walks ('depth first') the nested dictionary
    and at each level replaces the 'number in string' keys by their numeric
    representation, applies the path / value substitution patterns to the values
    of the 'end nodes', and converts them into proper paths.
    
    Signature:
        dict(str : type A), dict(str : type B),
            str/, logging.Logger OR 'LoggingFSIO.ConsoleLogger/
                -> dict(str : type C)
    
    Args:
        dictTarget: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
        dictSubstitutions: dict(str : type B), dictionary of the substitution
            rules with the pattern names as the string keys, and the actual
            substitutions - as the bound values
        strFile: str, path to the original file, which includes definitions from
            other files to be loaded
        objLogger: (optional) logging.Logger or 'LoggingFSIO.ConsoleLogger,
            instance of, a logger object compatible with the standard logger
            interface
    
    Returns:
        dict: the mapping rules dictionary conforming the DE001 DSL specs
    
    Raises:
        ValueError: improper input, not conforming mapping DSL
    
    Version 0.1.0.0
    """
    #replace str(int) -> int keys
    lstKeys = dictTarget.keys()
    for gKey in lstKeys:
        strError = 'Improper key {} in {} in file {}'.format(gKey, dictTarget,
                                                                        strFile)
        if not isinstance(gKey, (basestring, int, long)):
            _LogAndRaise(strError, ValueError, objLogger)
        elif isinstance(gKey, (int, long)) and gKey < 0:
            _LogAndRaise(strError, ValueError, objLogger)
        elif isinstance(gKey, basestring) and (not _IsProperKey(gKey)):
            _LogAndRaise(strError, ValueError, objLogger)
        elif _IsNumberString(gKey):
                iKey = int(gKey)
                Value = dictTarget[gKey]
                del dictTarget[gKey]
                dictTarget[iKey] = Value
    #loop through
    lstKeys = dictTarget.keys()
    for Key in lstKeys:
        Value = dictTarget[Key]
        if isinstance(Value, collections.Mapping):
            _WalkDict(Value, dictSubstitutions, strFile, objLogger = objLogger)
        elif isinstance(Value, basestring) and (Value in dictSubstitutions):
            dictTarget[Key] = dictSubstitutions[Value]
        else:
            try:
                lstPath = FlattenPath(Value)
                _lstPath = []
                for Item in lstPath:
                    if (isinstance(Item, basestring)
                                            and (Item in dictSubstitutions)):
                        _lstPath.append(dictSubstitutions[Item])
                    else:
                        _lstPath.append(Item)
                lstPath = FlattenPath(_lstPath)
                dictTarget[Key] = lstPath
            except Exception as Err:
                strError ='Improper path {} in {} in file {}'.format(Value,
                                                            dictTarget, strFile)
                _LogAndRaise(strError, ValueError, objLogger, Err)

def _ApplySubstitutions(dictBuffer, dictSubstitutions, strFile,
                                                            objLogger = None):
    """
    Selects the 'direct' mapping rules as well as the incremental addition rules
    and applies all path and value substitution rules to them.
    
    Signature:
        dict(str : type A), dict(str : type B),
            str/, logging.Logger OR 'LoggingFSIO.ConsoleLogger/
                -> dict(str : type C)
    
    Args:
        dictTarget: dict(str : type A), dictionary of string keys (pattern
            names) and any proper JSON values, the data loaded from a file
        dictSubstitutions: dict(str : type B), dictionary of the substitution
            rules with the pattern names as the string keys, and the actual
            substitutions - as the bound values
        strFile: str, path to the original file, which includes definitions from
            other files to be loaded
        objLogger: (optional) logging.Logger or 'LoggingFSIO.ConsoleLogger,
            instance of, a logger object compatible with the standard logger
            interface
    
    Returns:
        dict: the mapping rules dictionary conforming the DE001 DSL specs,
            includes 'direct' rules and the incremental additions.
    
    Raises:
        ValueError: improper input, not conforming mapping DSL
    
    Version 0.1.0.0
    """
    dictResult = dict()
    dictTemp = _SelectDirectRules(dictBuffer)
    try:
        for Key, Value in _SelectAdditionRules(dictBuffer, dictTemp).items():
            dictTemp[Key] = Value
    except (TypeError, ValueError) as Err:
        strError = 'improper addition rule in file {}'.format(strFile)
        _LogAndRaise(strError, ValueError, objLogger, Err)
    for Key, Value in dictTemp.items():
        if isinstance(Value, basestring) and (Value in dictSubstitutions):
            #entire path = substitution
            dictResult[Key] = dictSubstitutions[Value]
        elif isinstance(Value, collections.Mapping): #nested definition
            _WalkDict(Value, dictSubstitutions, strFile, objLogger = objLogger)
            dictResult[Key] = Value
        else: #substritution may be a part of the path
            try:
                Path = FlattenPath(Value)
                ResolvedPath = []
                for Item in ResolvedPath:
                    if (isinstance(Item, basestring)
                                            and (Item in dictSubstitutions)):
                        ResolvedPath.append(dictSubstitutions[Item])
                    else:
                        ResolvedPath = Item
                ResolvedPath = FlattenPath(ResolvedPath)
                dictResult[Key] = ResolvedPath
            except Exception as Err:
                strError = 'improper rule "{} : {}" in {} in file {}'.format(
                                                Key, Value, dictBuffer, strFile)
                _LogAndRaise(strError, ValueError, objLogger, Err)
    return dictResult

def _GetPathsPairs(dictRules, lstPath = None):
    """
    Recursive function to 'flatten' the mapping rules dictionary. The nested
    dictionaries definitions of the paths to the target object`s attributes /
    elements with the 'end node' values being paths to the source object`s 
    attributes / elements are converted into a flat list of 2-elements tuples.
    
    In each tuple the first element is the 'flattened' path (list) within the
    target object, and the second - is the 'flattened' path (list) within the
    source object.
    
    Signature:
        dict/, list OR None/ -> list(tuple(list, list))
    
    Args:
        dictRules: dictionary, the mapping rules
        lstPath: (optional) list, the already walked path within the target
            object; do not use it with the normal call! - it is only for the
            internal recursion implementation
    
    Returns:
        list: a list of 2-elements tuples, with both elements of any tuple being
            lists - proper paths to the target and source objects elements
    
    Raises:
        TypeError: source or target paths are not mapping DSL conforming, see
            FlattenPath()
        ValueError: source or target paths are not mapping DSL conforming, see
            FlattenPath()
    
    Version 0.1.0.0
    """
    if lstPath is None:
        lstTargetPath = []
    else:
        lstTargetPath = list(lstPath)
    tuplstResult = []
    for gKey, gValue in dictRules.items():
        if not (_IsProperKey(gKey) or
                                (isinstance(gKey, (int, long)) and gKey >= 0)):
            strError = 'Not proper key {} of {} in rules {}'.format(
                                                    gKey, type(gKey), dictRules)
            raise ValueError(strError)
        lstTempPath = list(lstTargetPath)
        if _IsNumberString(gKey):
                iKey = int(gKey)
                lstTempPath.append(iKey)
        else:
            lstTempPath.append(gKey)
        if isinstance(gValue, collections.Mapping):
            tuplstResult.extend(_GetPathsPairs(gValue, lstTempPath))
        else:
            tuplstResult.append((FlattenPath(lstTempPath),
                                                        FlattenPath(gValue)))
    return tuplstResult

def _ApplyAdditions(dictRules):
    """
    Adds entries into the mapping definitions dictionaries using the incremental
    addition entries. Each such incremental addition entry must be defined by
    the string key starting with '+' followed by the sub-string value of a key
    in the same dictionary (without '+' - the 'direct' rule). All incremental
    addition entries are removed from the passed dictionary afterwards.
    
    Signature:
        dict(str : dict) -> None
    
    Args:
        dictRules: dict(str : dict), dictionary of the direct mapping rules
    
    Raises:
        TypeError: source or target paths are not mapping DSL conforming, see
            _GetPathsPairs()
        ValueError: source or target paths are not mapping DSL conforming, see
            _GetPathsPairs()
    
    Version 0.1.0.0
    """
    strAdditionKeys = filter(_IsAdditionKey, dictRules.keys())
    for strKey in strAdditionKeys:
        tuplstTemp = _GetPathsPairs(dictRules[strKey])
        for lstTargetPath, lstSourcePath in tuplstTemp:
            objTarget = dictRules[strKey[1:]]
            for gItem in lstTargetPath[:-1]:
                if not (gItem in objTarget):
                    objTarget[gItem] = dict()
                objTarget = objTarget[gItem]
            objTarget[lstTargetPath[-1]] = lstSourcePath
    for strKey in strAdditionKeys:
        del dictRules[strKey]

def _ApplyRemovals(dictRules, dictRemovals):
    """
    Deletes the entries in the already resolved mapping definitions using the
    incremental removal entries. If the removal of the 'end node' target`s path
    results in the 'dead' (sub-) branch (no 'leaves' / 'end nodes' from a
    specific point in the path and down), such 'dead' (sub-) branch is entirely
    deleted. All keys in the second dictionary argument are suppossed to start
    with '-' followed by the sub-string value of a key in the first dictionary
    argument.
    
    Signature:
        dict(str : dict), dict(str : list(type B)) -> None
    
    Args:
        dictRules: dict(str : dict), dictionary of the direct mapping rules
        dictRemovals: dict(str : list(type B)), dictionary of the incremental
            removals
    
    Raises:
        ValueError: improper definition of the removal path with respect to the
            mapping dictionary objects
    
    Version 0.1.0.0
    """
    for strKey, lstValue in dictRemovals.items():
        objTarget = dictRules[strKey[1:]]
        for gItem in lstValue:
            try:
                lstTargetPath = FlattenPath(gItem)
            except (TypeError, ValueError) as Err:
                strError = '{} - improper deletion defintion "{} :{}"'.format(
                                                Err.message, strKey, lstValue)
                raise ValueError(strError)
            objTemp = objTarget
            tuplstChain = []
            #delete the end element
            for iIndex, gElement in enumerate(lstTargetPath):
                if _IsNumberString(gElement):
                    _gItem = int(gElement)
                elif _IsIdentifier(gElement) or (
                        isinstance(gElement, (int, long)) and gElement >= 0):
                    _gItem = gElement
                else:
                    strError = ' '.join(['Improper key {}'.format(gElement),
                        'in path {} for deletion from {}'.format(lstTargetPath,
                                                                strKey[1:])])
                    raise ValueError(strError)
                strError = '{} has no node {} in path {}'.format(strKey[1:],
                                                        _gItem, lstTargetPath)
                if not (_gItem in objTemp):
                    raise ValueError(strError)
                if iIndex < (len(lstTargetPath) - 1):
                    tuplstChain.append((objTemp, _gItem))
                    objTemp = objTemp[_gItem]
                else:
                    del objTemp[_gItem]
            for dictItem, _gItem in reversed(tuplstChain):
                #print dictItem, _gItem
                if not len(dictItem[_gItem]):
                    del dictItem[_gItem]
        #delete 'dead' rules
        if not len(objTarget):
            del dictRules[strKey[1:]]
        del dictRemovals[strKey]

#+ main functions

def LoadDefinition(strFile, objLogger = None):
    """
    'Main' function to load a JSON file and to parse the content into a mapping
    rules dictionary according to the DE001 DSL specifications.
    
    Signature:
        str/, logging.Logger OR 'LoggingFSIO.ConsoleLogger/ -> dict
    
    Args:
        strFile: str, path to the definition file to load
        objLogger: (optional) logging.Logger or 'LoggingFSIO.ConsoleLogger,
            instance of, a logger object compatible with the standard logger
            interface
    
    Returns:
        dict: the mapping rules dictionary conforming the DE001 DSL specs
    
    Raises:
        IOError: re-raised, some file I/O related problems
        OSError: re-raised, some file I/O related problems
        ValueError: the file is found, but it is not of a proper JSON format; OR
            the data read is not a dictionary; OR it does not comply with the
            mapping DSL specifications
    
    Version 0.1.0.0
    """
    try:
        with open(strFile, 'rt') as fFile:
            dictBuffer = json.load(fFile)
    except Exception as err:
        strMessage = 'in file {}'.format(strFile)
        _LogAndRaise(strMessage, err.__class__, objLogger, err)
    if not isinstance(dictBuffer, collections.Mapping):
        strError = 'Data {} read from {} is not a dictionary'.format(dictBuffer,
                                                                        strFile)
        _LogAndRaise(strError, ValueError, objLogger)
    #form the substituions table
    #+ import other  - includes!
    dictSubstitutions = {}
    for strKey, gValue in _ExtractValueSubstitutions(dictBuffer, strFile,
                                                objLogger = objLogger).items():
        dictSubstitutions[strKey] = gValue
    #+ resolve path substitutions
    try:
        dictPathSubstitutions = _ExtractPathSubstitutions(dictBuffer)
    except (TypeError, ValueError) as err:
        strError = 'path substitions in file {}'.format(strFile)
        _LogAndRaise(strError, ValueError, objLogger, err)
    for Key, Value in dictPathSubstitutions.items():
        dictSubstitutions[Key] = Value
    #move all extras into the returned dictionary - no need for substitutions
    dictResult = _ExtractExtras(dictBuffer)
    #resolve and move actual definitions
    #+ direct and addition rules
    dictDirect = dict()
    for strKey, Value in _ApplySubstitutions(dictBuffer, dictSubstitutions,
                                        strFile, objLogger = objLogger).items():
        dictDirect[strKey] = Value
    try:
        _ApplyAdditions(dictDirect)
        dictRemovals = _SelectRemovalRules(dictBuffer,dictDirect)
        _ApplyRemovals(dictDirect, dictRemovals)
        del dictRemovals
    except (ValueError, TypeError, AttributeError) as err:
        strError = 'mapping rules in file {}'.format(strFile)
        _LogAndRaise(strError, ValueError, objLogger, err)
    for Key, Value in dictDirect.items():
        dictResult[Key] = Value
    del dictDirect
    #check that all substitutions are resolved - otherwise, an error
    for _, lstPath in _GetPathsPairs(dictResult):
        for gItem in lstPath:
            if (_IsIncludeKey(gItem) or _IsPathKey(gItem)
                                                    or (gItem in ['#', '$'])):
                strError = 'Undefined substitution {} in {} in {}'.format(gItem,
                                                            dictResult, strFile)
                _LogAndRaise(strError, ValueError, objLogger)
    #check, that nothing remains in the buffer - otherwise, an error
    strError = None
    for Key, Value in dictBuffer.items():
        bCond1 = isinstance(Key, basestring) and (Key == '' or 
                                                        Key[0] in ['#', '$'])
        bCond2 = isinstance(Value, basestring) and (Value == ''
                                                    or Value.startswith('$'))
        if bCond1 or bCond2:
            strError = " ".join(['Wrong entry "{}" : {}'.format(Key, Value),
                    'in the mapping definitions in file {}'.format(strFile)])
            _LogAndRaise(strError, ValueError, objLogger)
    if len(dictBuffer):
        strError = " ".join(['Unused entries {}'.format(dictBuffer),
                    'in the mapping definitions in file {}'.format(strFile)])
        _LogAndRaise(strError, ValueError, objLogger)
    return dictResult

def MapValues(gTarget, gSource, dictMap, objLogger = None,
            bStrictTarget = True, bStrictSource = True, bForceTarget = False):
    """
    A function to copy the values of some attributes or keys or sequence
    elements from a (nested) C struct (Pascal record), dictionary, sequence or
    xml.etree.ElementTree.Element object (source) into another object of one of
    these types.
    
    The mapping rules should be a (nested) dictionary with keys at each level
    being strings (names) or non-negative integers (indexes) referring to an
    element of the target object at the same level. The values not being
    dictionaries themselves in the mapping rules dictionary are interpreted as
    paths to a certain element in the source object. Such paths
    can be an integer (index of a sequence), a string (name of an attribute or
    a key), a 'choice' dictionray (required sub-elements and their values for an
    unnamed elements in a sequence) or a (nested) sequence of there types.
    
    The absence of the expected elements in the source or target elements is
    treated depending on the values of the default parameters (boolean flags),
    which values can be passed as the optional positional or keyword arguments.
    
    * bStrictTarget is True (default) the absence of an expected element in the
        target object is an error, the AttributeError is raised, the value of
        the flag bForceTarget is ignored; it is False - the warning is issued
        (if a logger is provided) and the required element (with all missing
        intermediate element along the path) is created, if possible and the
        flag bForceTarget is True (default is False)
    * bStrictSource is True (default) the absence of an expected element in the
        source object is an error, the AttributeError is raised; it is False -
        the warning is issued (if a logger is provided)
    
    If an optional logger object with the standard API is provided, all raised
    exceptions and warnings are logged.
    
    Signature:
        type A, type B, dict/, logging.Logger OR
            'fsio_lib.LoggingFSIO.ConsoleLogger, bool, bool, bool/ -> None
    
    Args:
        gTarget: type A, the target object, into which the data is to be copied
        gSource: type B, the source object, from which the data is to be taken
        dictMap: the mapping rules dictionary, see DE001 DSL specifications
        objLogger: (optional) logging.Logger OR 'LoggingFSIO.ConsoleLogger,
            instance of, the logger object, by default is None (not provided)
        bStrictTarget: (optional) bool, flag if the target object MUST have all
            expected elements, default value is True
        bStrictSource: (optional) bool, flag if the source object MUST have all
            expected elements, default value is True
        bForceTarget: (optional) bool, flag is the missing elements / paths are
            to be created in the target object, has an effect only if the value
            of bStrictTarget is False, the default value for bForceTarget False
    
    Raises:
        TypeError: wrong mapping dictionary format or missmatch between the
            structure of the target and source objects and the mapping rules
        ValueError: wrong mapping dictionary format or missmatch between the
            structure of the target and source objects and the mapping rules
        AttributeError: missing element of the target or source object if the
            corresponding flags are set to True, or an immutable element in the
            target object
    """
    #get source -> target paths pairs
    strMessage = ' '.join(['wrong type of the mapping rules object',
                '{} of {} - not a dictionary'.format(dictMap, type(dictMap))])
    if not isinstance(dictMap, collections.Mapping):
        _LogAndRaise(strMessage, TypeError, objLogger)
    strMessage = 'wrong format of the mapping dictionary {}'.format(dictMap)
    try:
        tuplstPaths = _GetPathsPairs(dictMap)
    except Exception as Err:
        _LogAndRaise(strMessage, Err.__class__, objLogger, Err)
    #iterate through pairs
    for lstTargetPath, lstSourcePath in tuplstPaths:
        #get value
        strMessage = ' '.join(['Unable to get value of an element at',
                            '{} in object {}'.format(lstSourcePath, gSource)])
        bFound = False
        try:
            gSourceValue = GetElement(gSource, lstSourcePath)
            bFound = True
        except (TypeError, ValueError) as Err:
            _LogAndRaise(strMessage, Err.__class__, objLogger, Err)
        except AttributeError as Err:
            if bStrictSource:
                _LogAndRaise(strMessage, Err.__class__, objLogger, Err)
            else:
                if not (objLogger is None):
                    strLogMessage = "({}: {}) => {}".format(
                                Err.__class__.__name__, Err.message, strMessage)
                    objLogger.warning(strLogMessage)
        if bFound:
        #set value
            strMessage =' '.join(['Unable to set {} value'.format(gSourceValue),
                        'to an element at {} in object {}'.format(lstTargetPath,
                                                                    gTarget)])
            try:
                SetElement(gTarget, lstTargetPath, gSourceValue)
            except (TypeError, ValueError) as Err:
                _LogAndRaise(strMessage, Err.__class__, objLogger, Err)
            except AttributeError as Err:
                if (not bStrictTarget):
                    if not (objLogger is None):
                        strLogMessage = "({}: {}) => {}".format(
                                Err.__class__.__name__, Err.message, strMessage)
                        objLogger.warning(strLogMessage)
                    if bForceTarget:
                        try:
                            if (not bStrictTarget):
                                objLogger.warning('Attempting to insert...')
                                AddElement(gTarget, lstTargetPath, gSourceValue)
                                objLogger.warning('Inserted -> target modified')
                            else:
                                AddElement(gTarget, lstTargetPath, gSourceValue)
                        except Exception as NewErr:
                            _LogAndRaise(strMessage, NewErr.__class__,
                                                            objLogger, NewErr)
                else:
                    _LogAndRaise(strMessage, Err.__class__, objLogger, Err)
