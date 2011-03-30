'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''
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

# lkk Mar. 2011
# This is sensitive.  Beware of float event coords versus int pixel positions,
# sloppy math, conversions and rounding,
# and when using Pyusecase which might introduce more inaccuracies.
# I experienced difficulty with Pyusecase using a value of 3.
PENSOOL_PICK_PEN_WIDTH = 4  # width of pen in pixels for picking
PENSOOL_LINE_CAP_SQUARE = cairo.LINE_CAP_SQUARE

# gui.manager.fade
GUI_FADE_TIME = 500 # mSec delay before handles dissappear from recently focused morph

# gui.manager.pointer
GUI_MOVING_POPUP_TIME = 1000 # mSec delay after pointer stops before handle menu appears in background
GUI_MOVING_SLOWING_THRESHOLD = 0.1  # pixels per mSec below which pointer is considered stopped



