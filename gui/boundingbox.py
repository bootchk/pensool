#!/usr/bin/env python

'''
Bounding box

'''

import morph.morph
import scheme
from decorators import *

# Was Drawable
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
  
  def __init__(self, viewport):
    super(BoundingBox, self).__init__(viewport)
    self.activated = False

    
  @view_altering
  @dump_event
  def activate(self, direction, rect=None):
    '''
    Activate: make visible at given rect in DCS.  
    Does not receive events.
    '''
    if direction:
      # Set transform to make the DCS rect bounding box passed in.
      # TODO is this the correct call?
      self.set_dimensions(rect)
      # While the bounding box is visible, user cannot change viewport
      # so bounding box is not a transformed drawable.
      scheme.transformed_controls.append(self)
      self.activated = True
    elif self.activated:
      # Deactivate
      self.activated = False
      scheme.transformed_controls.remove(self)
    
    
    
    
# Singleton is in scheme
