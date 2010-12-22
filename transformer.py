#!/usr/bin/env python

'''
Transformer: drawable that transforms its members

Understands transforms and hierarchal modeling.

Note Transformer does NOT override draw(), but Composite does.
!!! But Composite.draw() can be overridden, for composites having both transformed and untransformed shapes.
'''

import drawable
import cairo
import base.vector as vector
from decorators import *




class Transformer(drawable.Drawable):

  def __init__(self, viewport):
    drawable.Drawable.__init__(self, viewport)
    self.transform = cairo.Matrix() # initially identity transform
    
    self.translation = vector.Vector(0, 0)
    self.scale = vector.Vector(1.0, 1.0)
    self.rotation = 0.0
  
  
  @dump_return
  def put_transform_to(self, context):
    '''
    Apply my transform to the current transform in the context.
    and style?
    '''
    context.save()  # !!! caller must do a matching restore
    try:
      context.transform(self.transform)
    except cairo.Error:
      print self.transform
      raise
    self.style.put_to(context)
    print "CTM", context.get_matrix()
    return self.transform
  
  
  @dump_event
  def derive_transform(self):
    '''
    Calculate my transform from my drawing specs.
    '''
    self.transform = cairo.Matrix()
    # Standard sequence: rotate, scale, translate
    # TODO rotate
    self.transform.scale(self.scale.x, self.scale.y)  # Scale
    translation_matrix = cairo.Matrix(x0=self.translation.x, 
      y0=self.translation.y) # Translate
    # Multiply in correct order. Note self.transform.translate() would not work??
    self.transform *= translation_matrix  
    
  
  @dump_event
  def set_dimensions(self, dimensions):
    '''
    Set the translation and scale of an object.
    For testing: ordinarily, transforms are set by user actions using other methods.
    '''
    assert dimensions.width > 0
    assert dimensions.height > 0
    
    # Should be a non-empty morph (a compound)
    assert len(self) > 0
    
    drawable.Drawable.set_dimensions(self, dimensions)  # Super
    self.translation = vector.Vector(dimensions.x, dimensions.y)
    self.scale = vector.Vector(dimensions.width/1.0, dimensions.height/1.0)
    self.derive_transform()
    
    
    
  @dump_event
  def move_relative(self, event, offset):
    '''
    Move origin by offset in device CS.  Offset is a delta.
    '''
    self.invalidate()
    # TODO calculate local coordinates by using parent transform.
    self.translation += offset
    self.derive_transform()
    self.invalidate()
    
 
  def device_to_user(self, x, y):
    # TODO do I need the model context?
    context = self.viewport.da.window.cairo_create()
    ### context.set_matrix(self.matrix)
    return vector.Vector(*context.device_to_user(x, y))
  
  
  def zoom(self, delta, event, context):
    '''
    Scale on point.
    Standard sequence of 3 transformations:
      translate
      scale
      inverse translation
    '''
    """
    When part of viewport was
    user_coords = self.device_to_user(event.x, event.y)
    self.transform.translate(user_coords.x, user_coords.y)
    self.transform.scale(delta, delta)
    self.transform.translate(-user_coords.x, -user_coords.y)
    """
    self.invalidate(context)
    self.scale *= delta
    print "Zoomed scale is", self.scale
    self.derive_transform()
    self.invalidate(context)
    
 
