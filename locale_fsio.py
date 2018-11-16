#!/usr/bin/python
"""
Module fsio_lib.locale_fsio

Implements functions for locale independent writing of tabulated data ASCII
text files (TSV format) concerning the new line, decimal separator and delimiter
conventions as well as use of usual spaces instead of TABs for the columns
separation. Also implements function, which forces specific new line convention.

Functions:
    SaveForcedNewLine()
        str, seq(str)/, str = '\r\n'/ -> None
    LoadLines()
        str/, int >= 0/ -> list(str)
    SplitLine()
        str -> list(str)
    DetectNotation()
        seq(str) -> int
    ConvertFromString()
        str, int -> int OR float OR str
    LoadTable()
        str/, int >= 0/ -> list(list(int OR float OR str))
"""

__version__ = "0.1.0.0"
__date__ = "31-10-2018"
__status__ = "Production"

#imports

#+ standard libraries

import re

# globals

#+ definitely dutch number representation regular patters

RE_NL1 = re.compile(r'(^|\D)(\+|-)?\d+,\d*(E|e)(\+|-)?\d*($|\D)')
RE_NL2 = re.compile(r'(^|\D)(\+|-)?\d{1,3}\.\d{3}(\.\d{3})+($|\D)')
RE_NL3 = re.compile(r'(^|\D)(\+|-)?\d{1,3}(\.\d{3})+,\d*($|\D)')
RE_NL4 = re.compile(r'(^|\D)\d+,(\d{1,2}|\d{4}\d*)($|D)')

#+ possibly dutch number representation regular patters

RE_NL5 = re.compile(r'(^|\D)\d+,\d*($|D)')

#+ definitely international number representation regular patters

RE_INT1 = re.compile(r'(^|\D)(\+|-)?\d+\.\d*(E|e)(\+|-)?\d*($|\D)')
RE_INT2 = re.compile(r'(^|\D)(\+|-)?\d{1,3},\d{3}(,\d{3})+($|\D)')
RE_INT3 = re.compile(r'(^|\D)(\+|-)?\d{1,3}(,\d{3})+\.\d*($|\D)')
RE_INT4 = re.compile(r'(^|\D)\d+\.(\d{0,2}|\d{4}\d*)($|D)')

#functions

def SaveForcedNewLine(strFileName, strseqLines, strNewLine = '\r\n'):
    """
    Saves the passed sequence of strings as lines in a text files and enforces
    the specific line ending.
    
    Signature:
        str, seq(str)/, str = '\r\n'/ -> None
    
    Args:
        strFileName: str, name of the file to write into (creates / re-writes)
        strseqLines: seq(str), any sequence of the strings (ASCII supposed) to
            be saved into the file
        strNewLine: (optional) str, the line ending style, e.g. '\n' (LF) or
            '\r\n' (CRLF). Defaults to the Windows convention CRLF
    
    Version 0.1.0.0
    """
    with open(strFileName, 'wb') as fFile:
        for strLine in strseqLines:
            fFile.write(strLine)
            fFile.write(strNewLine)

def LoadLines(strFileName, iSkipLines = 0):
    """
    Loads a file, splits it into lines (as strings), strips the end line
    characters (CR and LF - alone or in CRLF combination), (optionally) skips
    the first iSkipLines, and returns the result as a list of strings.
    
    Signature:
        str/, int >= 0/ -> list(str)
    
    Args:
        strFileName: str, name of (path to) the file to read
        iSkipLines: (optional) int, not negative, the number of the first lines
            to skip, defaults to 0; non-integer or negative values are ignored
    
    Version 0.1.0.0
    """
    with open(strFileName, 'rb') as fFile:
        strBuffer = fFile.read()
    strlstBuffer = []
    strTemp = ''
    bNewLine = False
    for strChar in strBuffer:
        if strChar == '\r':
            if bNewLine:
                strlstBuffer.append(strTemp)
                strTemp = ''
            else:
                bNewLine = True
        elif strChar == '\n':
            bNewLine = False
            strlstBuffer.append(strTemp)
            strTemp = ''
        else:
            if not bNewLine:
                strTemp += strChar
            else:
                strlstBuffer.append(strTemp)
                bNewLine = False
                strTemp = strChar
    if len(strTemp) or bNewLine:
        strlstBuffer.append(strTemp)
    if isinstance(iSkipLines, (int, long)) and iSkipLines >= 0:
        strlstBuffer = strlstBuffer[iSkipLines:]
    return strlstBuffer

def SplitLine(strLine):
    """
    Splits the passed string into substrings, returned as a list of strings, by
    a single TAB or an arbitrary amount of spaces. Tailing and leading TABs or
    spaces are also converted into empty strings (columns). An empty string is
    converted into a list containg a single element - an empty string.
    
    Signature:
        str -> list(str)
    
    Version 0.1.0.0
    """
    if len(strLine):
        bSpaceRun = False
        strlstResult = []
        strTemp = ''
        for strChar in strLine:
            if strChar != ' ' and strChar != '\t':
                bSpaceRun = False
                strTemp += strChar
            elif strChar == '\t':
                bSpaceRun = False
                strlstResult.append(strTemp)
                strTemp = ''
            else:
                if not bSpaceRun:
                    bSpaceRun = True
                    strlstResult.append(strTemp)
                    strTemp = ''
        strlstResult.append(strTemp)
    else:
        strlstResult = ['']
    return strlstResult

def DetectNotation(strseqSamples):
    """
    Determines the number notation used in the input (file) by matching each
    string from the passed sequence against defined (as globals) regular
    expression patterns until a definite match is found, i.e. unambiguous case
    of the number notation. If no definite matches is found, tries more
    ambiguous pattern(s). If still no matches - assumes the default
    international notation.
    
    Signature:
        seq(str) -> int
    
    Args:
        strseqSamples: seq(str), any sequence of strings
    
    Returns:
        int: 0 for the international, 1 for Dutch notation
    
    Version 0.1.0.0
    """
    bDefInt = False
    bDefDutch = False
    bPosDutch = False
    for strSample in strseqSamples:
        bDefInt = any(map(lambda x: not (x.match(strSample) is None),
                                        [RE_INT1, RE_INT2, RE_INT3, RE_INT4]))
        if not bDefInt:
            bDefDutch = any(map(lambda x: not (x.match(strSample) is None),
                                        [RE_NL1, RE_NL2, RE_NL3, RE_NL4]))
            if not (bDefDutch or bPosDutch):
                bPosDutch = RE_NL5.match(strSample)
        if bDefDutch or bDefInt:
            break
    if bDefInt:
        bResult = 0
    elif bDefDutch or bPosDutch:
        bResult = 1
    else:
        bResult = 0
    return bResult

def ConvertFromString(strItem, iNotation):
    """
    Removes the decimal delimiters, replaces the decimal separator as ','
    (comma) by '.' (dot) and attempts to convert the resulting string into an
    integer or a float (if failed to int). If conversion to float also failed
    returns the original string.
    
    Signature:
        str, int -> int OR float OR str
    
    Args:
        strItem: str, string to be converted
        iNotation: int, 0 for international, 1 for dutch
    
    Returns:
        int: if conversion to int is successful
        float: if conversion to int is not successful but to the float is ok
        str: the original string if cannot into int or float
    
    Version 0.1.0.0
    """
    if iNotation == 1:
        strNewStr = strItem.replace('.', '').replace(',', '.')
    elif iNotation == 0:
        strNewStr = strItem.replace(',', '')
    else:
        strNewStr = strItem
    try:
        gResult = int(strNewStr)
    except (TypeError, ValueError):
        try:
            gResult = float(strNewStr)
        except (TypeError, ValueError):
            gResult = strItem
    return gResult

def LoadTable(strFileName, iSkipLines = 0):
    """
    Generic locale-independent loader of a data file saved in a TSV format with:
        * CR, LF or CRLF line endings
        * TABs or abitrary amount of spaces (as a single TAB) for the columns
            separation
        * proper treatment of the 'empty' columns in the beginning or end of a
            line (row)
        * proper treatment of the numbers notation in dutch and english notation
            (i.e. ',' or '.' as the decimal separator) with or without the
            decimal delimiters ('.' or ',' respectively)
    
    Signature:
    
        str/, int >= 0/ -> list(list(int OR float OR str))
    
    Args:
        strFileName: str, name of (path to) a file to load
        iSkipLines: (optional) int, non-negative, number of the first lines to
            skip, defaults to 0. Non-integer or negative value is ignored
    
    Returns:
        list(list(int OR float OR str)): the tabulated data converted into
            nested lists (equal number of columns is not guaranteed), with the
            values of the 'cells' converted into int or float when possible
    
    Version 0.1.0.0
    """
    strlstLines = LoadLines(strFileName, iSkipLines)
    strlstlstBuffer= map(SplitLine, strlstLines)
    strlstTemp = []
    for strlstItem in strlstlstBuffer:
        strlstTemp.extend(strlstItem)
    iNotation = DetectNotation(strlstTemp)
    glstlstResult = [map(lambda x: ConvertFromString(x, iNotation), strlstTemp)
                                            for strlstTemp in strlstlstBuffer]
    return glstlstResult