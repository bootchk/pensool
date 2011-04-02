'''
Global configuration variables and constants.  

By convention, named config.py.

The viewport and model are global variables to avoid problems with circular import (epydoc doesn't like it) and to avoid passing parameters.
'''
'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

import cairo


def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name
  
  
# Global variables.  
viewport = None
scheme = None


PENSOOL_UNIT = 1
''' Scale.  Viewport scale is set to this; literals in pixel units are scaled by this.'''
# Possibly should be 1000 to put usual values into the middle of the range.

ITEM_SIZE = 20.0 / PENSOOL_UNIT
'''Default size of menu items.  Must be float, used as scale.'''


# lkk Mar. 2011
# This is sensitive.  Beware of float event coords versus int pixel positions,
# sloppy math, conversions and rounding,
# and when using Pyusecase which might introduce more inaccuracies.
# I experienced difficulty with Pyusecase using a value of 3.
PENSOOL_PICK_PEN_WIDTH = 4
'''width of pen in pixels for picking'''
PENSOOL_LINE_CAP_SQUARE = cairo.LINE_CAP_SQUARE
'''Synonym used in picking'''

# See gui.manager.fade
GUI_FADE_TIME = 500
''' mSec delay before handles dissappear from recently focused morph.'''

# See gui.manager.pointer
GUI_MOVING_POPUP_TIME = 1000
''' mSec delay after pointer stops before handle menu appears in background.'''
GUI_MOVING_SLOWING_THRESHOLD = 0.1 
''' pixels per mSec below which pointer is considered stopped. '''

ZOOM_RATE = 0.5
'''Ratio for zoom steps in and out'''

