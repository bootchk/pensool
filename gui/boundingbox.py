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
  
  # __init__ inherited
  
  def put_path_to(self, context):
    '''
    Bounding box is a rectangle aligned with the display edges.
    !!! Not rotated.
    '''
    context.rectangle(self.dimensions)


  def invalidate(self):
    # TODO the bounding box transforms to device space
    self.viewport.surface.invalidate_rect( self.dimensions, True )

    
  @dump_event
  def activate(self, rect):
    '''
    Activate: make visible at given rect.  Does not receive events.
    '''
    self.dimensions = rect
    self.invalidate()
    # While the bounding box is visible, user cannot change viewport
    # so bounding box is not a transformed drawable.
    scheme.transformed_controls.append(self)

    
  def deactivate(self, rect):
    '''
    Deactivate: make invisible.
    '''
    delete(scheme.transformed_controls[0])
    
    
    
# Singleton is in scheme
