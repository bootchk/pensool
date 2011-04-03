'''
Miscellaneous transform and hierarchical modeling.

This hides that we are using cairo: import cairo in only a few places.
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

def copy(transform):
  ''' Return copy of transform. This is workaround since pycairo won't properly copy a Matrix().'''
  return cairo.Matrix()*transform # Create identity matrix and multiply
  
def get_unit_matrix():
  return cairo.Matrix()
