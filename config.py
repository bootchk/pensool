#!/usr/bin/env python
'''
config.py

Pythonic module for global configuration variables.
'''

import gui.manager.drop


def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name
  
  
# Singleton
# TODO other manager singletons similar to this
# dropmgr = gui.manager.drop.DropManager()

# Scale.
# Viewport scale is set to this, and literals in pixel units are scaled by this.
PENSOOL_UNIT = 1  # 1000

# Default size of menu items
# Must be float, used as scale
ITEM_SIZE = 20.0 / PENSOOL_UNIT
