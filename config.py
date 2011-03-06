#!/usr/bin/env python
'''
config.py

Pythonic module of global configuration variables/constants.
'''

import cairo


def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name
  
  
# Singleton
# TODO other manager singletons similar to this
# import gui.manager.drop
# dropmgr = gui.manager.drop.DropManager()

# Scale.
# Viewport scale is set to this; literals in pixel units are scaled by this.
PENSOOL_UNIT = 1  # 1000

# Default size of menu items
# Must be float, used as scale
ITEM_SIZE = 20.0 / PENSOOL_UNIT

PENSOOL_PICK_PEN_WIDTH = 3  # width of pen in pixels for picking
PENSOOL_LINE_CAP_SQUARE = cairo.LINE_CAP_SQUARE

# gui.manager.fade
GUI_FADE_TIME = 500 # mSec delay before handles dissappear from recently focused morph

# gui.manager.pointer
GUI_MOVING_POPUP_TIME = 1000 # mSec delay after pointer stops before handle menu appears in background
GUI_MOVING_SLOWING_THRESHOLD = 0.1  # pixels per mSec below which pointer is considered stopped



