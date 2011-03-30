'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

'''
Bounding box

'''

import morph.morph
import scheme
from decorators import *

# A singleton bounding box is in scheme

class BoundingBox(morph.morph.RectMorph):
  '''
  A drawable primitive.
  Bounding box is feedback only, part of highlighting the focus.
  Not a control, does not get events.
  Not in the model, does not get printed.
  Pointer near bounding box does not open a handle menu.
  A handle menu does slide along the bounding box,
  but a handle menu only opens on a component of a composite that a bounding box represents.
  Is in the scheme.
  '''
  
  def __init__(self):
    super(BoundingBox, self).__init__()
    self.style.color = (0, 40, 40)  # greenish blue
    self.activated = False

    
  @view_altering
  @dump_event
  def activate(self, direction, rect=None):
    '''
    Activate: make visible at given rect in DCS.  
    Does not receive events.
    Rect is given for direction == True.
    '''
    if direction:
      # Special case: if rect is zero, do nothing.
      # It wouldn't be visible and it gives assertion errors later.
      # This happens if the model is empty.
      if rect.width == 0 and rect.height == 0:
        return
      
      # Set transform to make the DCS rect bounding box passed in.
      # TODO is this the correct call?  Supposedly set_dimensions is only for testing.
      self.set_dimensions(rect)
      # While the bounding box is visible, user cannot change view
      # so bounding box need not be a transformed drawable.
      scheme.transformed_controls.append(self)
      self.activated = True
    elif self.activated:
      # Deactivate
      self.activated = False
      scheme.transformed_controls.remove(self)



