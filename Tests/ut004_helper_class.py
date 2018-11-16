#!/usr/bin/python
"""
Module ut004_helper_class

Defines a target class for testing the dynamic import within the UT004 test

suite.
"""

__version__ = "0.1.0.0"
__date__ = "06-11-2018"
__status__ = "Testing"

#classes

#+ helper class

class HelperClass(object):
    def __init__(self):
        self.report = {"id" : None, "type" : None}
        self.result = None