#!/usr/bin/env python

'''
Miscellaneous transform and hierarchical modeling.

This helps hide (from the rest of the code) that we are using cairo.
'''

import cairo

def copy(transform):
  '''
  Return copy of transform.
  This is workaround since pycairo won't properly copy a Matrix().
  '''
  # Create identity matrix and multiply
  return cairo.Matrix()*transform
