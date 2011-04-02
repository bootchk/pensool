'''
Miscellaneous transform and hierarchical modeling.

This hides that we are using cairo: import cairo in only a few places.
'''

import cairo

def copy(transform):
  ''' Return copy of transform. This is workaround since pycairo won't properly copy a Matrix().'''
  return cairo.Matrix()*transform # Create identity matrix and multiply
  
def get_unit_matrix():
  return cairo.Matrix()
