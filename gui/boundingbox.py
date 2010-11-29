#!/usr/bin/env python

'''
Bounding box

'''

import drawable
import scheme
from decorators import *


class BoundingBox(drawable.Drawable):
  '''
  A drawable primitive.
  Bounding box is feedback only, part of highlighting the focus.
  Not a control, does not get events.
  Not a glyph in the model, does not get printed.
  Pointer near bounding box does not open a handle menu.
  A handle menu does slide along the bounding box,
  but a handle menu only opens on a component of a composite
  that the bounding box represents.
  Is in the scheme.
  '''
  
  def __init__(self, viewport):
    drawable.Drawable.__init__(self, viewport)
    self.activated = False
    
  def put_path_to(self, context):
    '''
    Bounding box is rectangle aligned with display (screen) edges.
    !!! Not rotated.
    '''
    context.rectangle(self.get_dimensions())


  # TODO invalidate inherited?
  # A bounding box is NOT a control since it doesn't receive events.
  # Drawables do NOT have an invalidate method.
  @dump_event
  def invalidate(self):
    device_bounds = self.get_inked_bounds()
    self.viewport.surface.invalidate_rect( device_bounds, True )
  
    
  @dump_event
  def activate(self, direction, rect=None):
    '''
    Activate: make visible at given rect.  Does not receive events.
    '''
    if direction:
      # !!! Dimensions of this drawable are the bounding box passed in.
      self.set_dimensions(rect)
      self.invalidate()
      # While the bounding box is visible, user cannot change viewport
      # so bounding box is not a transformed drawable.
      self.scheme_index = len(scheme.transformed_controls)
      scheme.transformed_controls.append(self)
      self.activated = True
    elif self.activated:
      # Deactivate
      self.activated = False
      self.invalidate()
      del(scheme.transformed_controls[self.scheme_index])
    
    
    
    
# Singleton is in scheme
