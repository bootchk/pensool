''' Style class '''
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

import base.transform as transform
import config


def set_line_width(context, pen_width):
  '''
  Set pen width with uniform scaling so pen is not elliptical.
  style.pen_width is in DCS units.  
  Scale by the viewing transform scale so that line widths scale with viewing.
  (Note they might become invisible.)
  Note: cairo pen width is subject to the CTM (to subsequent transforms), 
  paths are NOT subject to subsequent transforms.
  setting the pen width is AFTER the path
  '''
  context.set_matrix(transform.get_unit_matrix())
  context.scale(config.scheme.model.scale.x, config.scheme.model.scale.y) # viewing transform
  context.set_line_width(pen_width)
  
"""
OLD not used
"""

def calculate_line_width(context, pen_width):
  '''
  Calculate parameter for set_line_width.
  '''
  # Line width is subject to transform CTM.
  # The spec in a style is in device coords (pixels.)
  # Convert to user distance. Params are a distance vector.
  ux, uy = context.device_to_user_distance (pen_width, pen_width)
  #
  """
  OLD
  # Length of vector (not ux or uy, which can be zero)
  length = vector.Vector(ux, uy).length()
  assert length > 0 # otherwise, extents, bounds will not be correct!
  """
  length = min(ux, uy)
  if length <= 0:
    print "Line width <=0 **********", ux, uy
    length = 0.1
  return length


class Style(object):
  ''' User changeable style for a morph. '''
  def __init__(self):
    # attributes of style
    self.pen_width = config.DEFAULT_PEN_WIDTH
    self.color = (0, 0, 0)  # black
    self.filled = False
    # other
    self.previous_color = None
    
  def put_to(self, context):
    context.set_source_rgba(self.color[0], self.color[1], self.color[2], 0.5) # color, 50% opacity
    # !!! Line width is set later.  See drawable.draw().
    ## OLD context.set_line_width(calculate_line_width(context, self.pen_width))
    # !!! The fill is special, separate from context.
    
  def is_filled(self):
    return self.filled
    
  def highlight(self, direction):
    if direction:
      self.previous_color = self.color
      self.color = (50, 0, 0)
    else:
      # If unhilight without a prior highlight.
      # EG when you add a morph to a highlighted group.
      if self.previous_color is not None:
        self.color = self.previous_color
        

