#!/usr/bin/python
"""
Module fsio_lib.fs_maintenance

Implements a number of functions for the maintenance of a file system, including
recursive removal of the duplicating files, recursive folder's renaming,
recursive deletion of empty sub-folders, pulling of the non-present files from
another folder, etc.

Functions:
    SmartCopy(strSource, strTarget):
        str, str -> None
    TouchFolder(strFolder):
        str -> None
    RemoveEmptyFolders(strFolder):
        str -> None
    RenameSubFolders(strFolder, strNewName, lstPaterns = []):
        str, str/, list(str)/ -> None
    MakeFolderDictionary(strFolder):
        str -> dict(str -> dict(str -> list(tuple(str, str))))
    RemoveDuplicateFiles(strFolder, lstSearchOrder = []):
        str/, list(str)/ -> None
    RemoveFilesCopies(strFolder):
        str -> None
    CopyNonPresent(strTargetPath, strSourcePath):
        str, str -> None
    CopyMerge(strSource, strTarget):
        str, str -> None
"""

__version__ = "1.0.0.0"
__date__ = "17-03-2020"
__status__ = "Production"

#imports

#+ standard libraries

import sys
import os
import datetime
import hashlib
import shutil

#functions

def SmartCopy(strSource, strTarget):
    """
    Copies a specified file into a specified directory, unless there is already
    a file in the target folder with the same md5 check sum and base filename is
    the same, or it is constructed as 'name (copy).ext' or 'name (copy 1).ext',
    'name (copy 2).ext', etc., where 'name.ext' is the base filename with
    extention of the source file. The name conflicts for the files with
    identical base filenames but different content (by md5 sum) in the source
    and target folders is resolved by appending a ' (copy)' or ' (copy {num})'
    suffix just before the file's extention, where {num} is replaced by a
    positive integer (1, 2, 3, etc.).
    
    Signature:
        str, str -> None
    
    Args:
        strSource: str, full path to a file to be copied
        strTarget: str, path to a folder, where to copy
    
    Version 0.1.0.0
    """
    if not os.path.isdir(strTarget):
        os.makedirs(strTarget)
    strBaseName = os.path.basename(strSource)
    strNewPath = os.path.join(strTarget, strBaseName)
    if not os.path.isfile(strNewPath):
        shutil.copy2(strSource, strTarget)
    else:
        with open(strSource, 'r') as fFile:
            OldSum = hashlib.md5(fFile.read()).hexdigest()
        with open(strNewPath, 'r') as fFile:
            NewSum = hashlib.md5(fFile.read()).hexdigest()
        if OldSum != NewSum:
            iNumber = 1
            lstParts = strBaseName.split('.')
            if len(lstParts) == 1:
                strExt = ''
                strMainName = strBaseName
            else:
                strExt = '.{}'.format(lstParts[-1])
                strMainName = '.'.join(lstParts[:-1])
            strNewTarget = os.path.join(strTarget, '{} (copy){}'.format(
                                                        strMainName, strExt))
            while True:
                if not os.path.isfile(strNewTarget):
                    shutil.copy2(strSource, strNewTarget)
                    break
                else:
                    with open(strNewTarget, 'r') as fFile:
                        NewSum = hashlib.md5(fFile.read()).hexdigest()
                    if OldSum == NewSum:
                        break
                strNewTarget = os.path.join(strTarget, '{} (copy {}){}'.format(
                                                strMainName, iNumber, strExt))
                iNumber += 1

def TouchFolder(strFolder):
    """
    Checks is a folder exists; creates a folder with all missing 'parent' sub-
    folders if the requested folder does not exist.
    
    Signature:
        str -> None
    
    Args:
        strFolder: str, path to a folder to check or create
    
    Version 0.1.0.0
    """
    if not os.path.isdir(strFolder):
        os.makedirs(strFolder)

def RemoveEmptyFolders(strFolder):
    """
    Recursively removes all empty sub-folders within the specified folder, i.e.
    those which do not contain files as the end-nodes of themselves or any of
    their sub-sub-folders.
    
    Signature:
        str -> None
    
    Args:
        strFolder: str, path to a folder to analyze
    
    Version 0.1.0.0
    """
    lstPaths = []
    for strPath, strlstFolders, strlstFiles in os.walk(strFolder):
        bCond1 = strPath != strFolder
        bCond2 = not len(strlstFolders)
        bCond3 = not len(strlstFiles)
        if bCond1 and bCond2 and bCond3:
            lstPaths.append(strPath)
    for strPath in lstPaths:
        if os.path.isdir(strPath):
            os.rmdir(strPath)
            strParent = os.path.dirname(strPath)
            while len(strParent) > len(strFolder):
                if not len(os.listdir(strParent)):
                    os.rmdir(strParent)
                    strParent = os.path.dirname(strParent)
                else:
                    break

def RenameSubFolders(strFolder, strNewName, lstPaterns = []):
    """
    Recursively renames all sub-folders matching the provided simple match
    patterns. The following rules are applied:
    
        * The sub-folder is renamed if its name matches the replacement name
            case-insensitive, but they are not equal case-sensitive
        * The sub-folder is renamed if its name matches any of the provided
            simple match patterns case-insensitive
        * If the parent folder of the sub-folder to be renamed already has a
            sub-folder with the requested replacement name the content of the
            sub-folder to be renamed is merged with the content of the already
            existing sub-folder
        * The files are copied using the function SmartCopy(), which prevents
            both duplication and replacement of the files with the same base
            names and md5 check sums
    
    Signature:
        str, str/, list(str)/ -> None
    
    Args:
        strFolder: str, path to a folder to analyze
        strNewName: str, the replacement name for the sub-folders
        lstPaterns: list(str), list of simple match patterns, names of the
            sub-folders, which base names must be replaced
    
    Version 0.1.0.0
    """
    lstCandidates = [strItem.lower() for strItem in lstPaterns]
    lstPaths = list(sorted([strPath for strPath, _, _ in os.walk(strFolder)
                            if strPath != strFolder],
                            key = lambda Entry: len(Entry), reverse = True))
    for strPath in lstPaths:
        if os.path.isdir(strPath):
            strEndFolder = os.path.basename(strPath)
            bCond1 = strEndFolder != strNewName
            bCond2 = strEndFolder.lower() == strNewName.lower()
            bCond3 = strEndFolder.lower() in lstCandidates
            if (bCond1 and bCond2) or bCond3:
                strNewPath = os.path.join(os.path.dirname(strPath), strNewName)
                if not os.path.isdir(strNewPath):
                    os.rename(strPath, strNewPath)
                else:
                    for strOldPath, _, lstFiles in os.walk(strPath):
                        if len(strOldPath) > len(strPath):
                            strSuffix = strOldPath[len(strPath) + 1 :]
                            strNewFolder = os.path.join(strNewPath, strSuffix)
                            TouchFolder(strNewFolder)
                        else:
                            strNewFolder = strNewPath
                        for strFile in lstFiles:
                            strFullPath = os.path.join(strOldPath, strFile)
                            SmartCopy(strFullPath, strNewFolder)
                            os.remove(strFullPath)
    RemoveEmptyFolders(strFolder)

def MakeFolderDictionary(strFolder):
    """
    Constructs a look-up table, as in a glossary, listing all found files in a
    folder including all its sub-folders. The files are grouped by their base
    filenames. For each unique base filename all found occurences are sub-
    grouped by the md5 check sum (unique file's content); and for each unique
    check sum the sub-path within the top folder and the last file's
    modification date-time stamp are stored.
    
    Signature:
        str -> dict(str -> dict(str -> list(tuple(str, str))))
    
    Args:
        strFolder: str, path to a folder to analyze
    
    Returns:
        dict(str -> list(dict(str -> str))): a dictionary implementing the
            following mapping: base filename -> md5 check sum -> [(sub-path,
            date-time stamp), ...]
    
    Version 0.1.0.0
    """
    iLength = len(strFolder)
    dictResult = dict()
    for strPath, _, strlstFiles in os.walk(strFolder):
        if len(strPath) == iLength:
            strSubPath = ''
        else:
            strSubPath = strPath[iLength + 1:]
        for strFile in strlstFiles :
            iTimeStamp = os.stat(os.path.join(strPath, strFile)).st_mtime
            strDateTime = datetime.datetime.fromtimestamp(iTimeStamp).strftime(
                                                            '%Y-%m-%d %H:%M:%S')
            dictTemp = dictResult.get(strFile, dict())
            strFullPath = os.path.join(strPath, strFile)
            with open(strFullPath, 'r') as fFile:
                strData = fFile.read()
                strCheckSum = hashlib.md5(strData).hexdigest()
            lstValue = dictTemp.get(strCheckSum, list())
            lstValue.append((strSubPath, strDateTime))
            dictTemp[strCheckSum] = lstValue
            dictResult[strFile] = dictTemp
    return dictResult

def RemoveDuplicateFiles(strFolder, lstSearchOrder = []):
    """
    Removes the fully duplicated files, i.e. those with the identical base
    filenames and md5 check sums (content) but placed into different subfolders,
    leaving only a single copy of each duplicated files. The copy to keep is
    chosen according to the following rules:
    
        * The first found sub-path amongst the provided list of preferred
            locations
        * If not provided or not found - the file with the latest date-time
            stamp
        * If several copies with the latest date-time stamp exist - the shortest
            sub-path is chosen
    
    Signature:
        str/, list(str)/ -> None
    
    Args:
        strFolder: str, path to a folder to analyze
        lstSearchOrder: (optional) list(str), list of sub-paths within this
            folder in the order of preference, where the copy of a duplicated
            file should remain; defaults to an empty list
    
    Version 0.1.0.0
    """
    dictTree = MakeFolderDictionary(strFolder)
    for strBaseName, dictIssues in dictTree.items():
        for _, lstCopies in dictIssues.items():
            if len(lstCopies) > 1: #duplicated files
                strLatestStamp = max(tupEntry[1] for tupEntry in lstCopies)
                tuplstCandidates = [(iIndex, tupEntry[0])
                                    for iIndex, tupEntry in enumerate(lstCopies)
                                        if tupEntry[1] == strLatestStamp]
                iIndex = sorted(tuplstCandidates,
                                        key = lambda Entry: len(Entry[1]))[0][0]
                strlstLocations = [tupEntry[0] for tupEntry in lstCopies]
                for strSubPath in lstSearchOrder:
                    if strSubPath in strlstLocations:
                        iIndex = strlstLocations.index(strSubPath)
                        break
                for iCurrentIndex, strSubPath in enumerate(strlstLocations):
                    if iCurrentIndex != iIndex:
                        strFullPath = os.path.join(strFolder, strSubPath,
                                                                    strBaseName)
                        os.remove(strFullPath)

def RemoveFilesCopies(strFolder):
    """
    Removes copies of the same file (same md5 check sum but different base
    filenames) situated in the same sub-folder. The copy with the shortest base
    filename is selected to remain, other copies are deleted. This process is
    recursively applied to all sub-folders within the specified path.
    
    Signature:
        str -> None
    
    Args:
        strFolder: str, path to a folder to analyze
    
    Version 0.1.0.0
    """
    lstFiles2Delete = []
    for strPath, _, lstFiles in os.walk(strFolder):
        dictTemp = dict()
        for strBaseName in lstFiles:
            strFullName = os.path.join(strPath, strBaseName)
            with open(strFullName, 'r') as fFile:
                CheckSum = hashlib.md5(fFile.read()).hexdigest()
            lstTemp = dictTemp.get(CheckSum, [])
            lstTemp.append(strFullName)
            dictTemp[CheckSum] = lstTemp
        for lstItem in dictTemp.values():
            if len(lstItem) > 1:
                lstFiles2Delete.extend(list(sorted(lstItem))[1:])
    for strPath in lstFiles2Delete:
        os.remove(strPath)

def CopyNonPresent(strTargetPath, strSourcePath):
    """
    Copies files found in any sub-folder of the source folder into the 'root'
    of the target folder if a file with the same base filename and md5 check sum
    is not found anywhere in the target folder (including sub-folders) matching
    the candidate file to be copied. In order to prevent possible name conflicts
    the name of the copied file is modified by adding a suffix consisting of an
    underscore ('_') and an integer number if a file with the same name exists
    anywhere in the target folder.
    
    Signature:
        str, str -> None
    
    Args:
        strTargetPath: str, path to the target folder
        strSourcePath: str, path to the source folder
    
    Version 0.1.0.0
    """
    dictMaster = MakeFolderDictionary(strTargetPath)
    dictMasterCS = dict()
    lstMasterNames = []
    for strBaseName, dictEntry in dictMaster.items():
        if not (strBaseName in lstMasterNames):
            lstMasterNames.append(strBaseName)
        for strCheckSum in dictEntry.keys():
            lstTemp = dictMasterCS.get(strCheckSum, [])
            lstTemp.append(strBaseName)
            dictMasterCS[strCheckSum] = lstTemp
    dictOther = MakeFolderDictionary(strSourcePath)
    for strBaseName, dictEntry in dictOther.items():
        for strCheckSum, lstItems in dictEntry.items():
            if not (strBaseName in dictMasterCS.get(strCheckSum, [])):
                strPath = list(sorted(lstItems, key = lambda x: x[1],
                                                        reverse = True))[0][0]
                lstParts = strBaseName.split('.')
                if len(lstParts) > 1:
                    strExt = '.{}'.format(lstParts[-1])
                    strName = '.'.join(lstParts[:-1])
                else:
                    strExt = ''
                    strName = strBaseName
                strNewName = '{}{}'.format(strName, strExt)
                iIndex = 1
                while strNewName in lstMasterNames:
                    strNewName = '{}_{}{}'.format(strName, iIndex, strExt)
                    iIndex += 1
                lstMasterNames.append(strNewName)
                lstTemp = dictMasterCS.get(strCheckSum, [])
                lstTemp.append(strNewName)
                dictMasterCS[strCheckSum] = lstTemp
                strOldPath = os.path.join(strSourcePath, strPath, strBaseName)
                strNewPath = os.path.join(strTargetPath, strNewName)
                shutil.copy2(strOldPath, strNewPath)

def CopyMerge(strSource, strTarget):
    """
    Merges the content, files and folders structure of the target folder with
    those of the source folder. Non-existing sub-folders are created,
    non-exisiting files are copied preserving the relative path with respect to
    the 'root' of the source / target folders. Existing files with the same
    relative paths including the base filenames are not overwritten: if the
    content is the same (by md5 check-sum) the source file is ignored, otherwise
    it is copied under a different name - adding '(copy)' or '(copy 1)', etc. to
    the name before the extension. Empty sub-folders are not copied: itself or
    any of its sub-sub-folders must contain, at least, one file.
    
    Signature:
        str, str -> None
    
    Args:
        strSource: str, path to the source folder
        strTarget: str, path to the target folder
    
    Version 0.1.0.0
    """
    strSourcePath = os.path.abspath(strSource)
    strTargetPath = os.path.abspath(strTarget)
    iSourceLen = len(strSourcePath)
    if not os.path.isdir(strTarget):
        shutil.copytree(strSource, strTarget)
    else:
        for strRoot, _, lstFiles in os.walk(strSource):
            strOldPath = os.path.abspath(strRoot)
            if strOldPath != strSourcePath:
                strNewPath = os.path.join(strTargetPath,
                                                    strOldPath[iSourceLen + 1:])
            else:
                strNewPath = strTargetPath
            if len(lstFiles):
                TouchFolder(strNewPath)
            for strFile in lstFiles:
                SmartCopy(os.path.join(strRoot, strFile), strNewPath)
        RemoveEmptyFolders(strTarget)