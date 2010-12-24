#!/usr/bin/env python
'''
config.py

Pythonic module for global variables.
'''

import dropmanager


def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name
  
  
# Singleton
dropmgr = dropmanager.DropManager()
