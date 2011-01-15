#!/usr/bin/env python


import base.vector as vector

class Style(object):
  
  def __init__(self):
    # attributes of style
    self.stroke_width = 1
    self.color = (0, 0, 0)  # black
    self.filled = False
    # other
    self.previous_color = None
    
  def put_to(self, context):
    context.set_source_rgba(self.color[0], self.color[1], self.color[2], 0.5) # color, 50% opacity
    # Line width is subject to transform CTM.
    # The spec in a style is in device coords (pixels.)
    # Convert to user distance. Params are a distance vector.
    ux, uy = context.device_to_user_distance (self.stroke_width, self.stroke_width)
    # 
    # Length of vector (not ux or uy, which can be zero)
    length = vector.Vector(ux, uy).length()
    assert length > 0 # otherwise, extents, bounds will not be correct!
    context.set_line_width(length)
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
        

