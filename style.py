#!/usr/bin/env python



class Style(object):
  
  def __init__(self):
    self.stroke_width = 1
    self.color = (0, 0, 0)
    self.previous = None
    
  def put_to(self, context):
    context.set_source_rgba(self.color[0], self.color[1], self.color[2], 0.5) # black pen, 50% opacity
    context.set_line_width(self.stroke_width)
    
  def highlight(self, direction):
    if direction:
      self.previous = self.color
      self.color = (50, 0, 0)
    else:
      # If unhilight without a prior highlight.
      # EG when you add a morph to a highlighted group.
      if self.previous is not None:
        self.color = self.previous
