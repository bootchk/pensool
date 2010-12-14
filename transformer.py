#!/usr/bin/env python

'''
Transformer: drawable that transforms its members

Understands transforms and hierarchal modeling.

Note Transformer does NOT override draw(), but Composite does.
!!! But Composite.draw() can be overridden, for composites having both transformed and untransformed shapes.
'''

import drawable
import cairo
from decorators import *




class Transformer(drawable.Drawable):

  def __init__(self, viewport):
    drawable.Drawable.__init__(self, viewport)
    self.transform = cairo.Matrix() # initially identity transform
  
  
  # @dump_return
  def put_transform_to(self, context):
    '''
    and style?
    '''
    context.save()  # !!! caller must do a matching restore
    try:
      context.transform(self.transform)
    except cairo.Error:
      print self.transform
      raise
    self.style.put_to(context)
    return self.transform
  
  
  @dump_event
  def set_dimensions(self, dimensions):
    '''
    Set the translationg and scale of an object.
    For testing: ordinarily, transforms are set by user actions using other methods.
    '''
    assert dimensions.width > 0
    assert dimensions.height > 0
    
    # Should be a non-empty morph (a compound)
    assert len(self) > 0
    
    drawable.Drawable.set_dimensions(self, dimensions)  # Super
    
    self.transform = cairo.Matrix()
    # Standard sequence: rotate, scale, translate
    # TODO rotate
    self.transform.scale(dimensions.width/1.0, dimensions.height/1.0) 
    translation_matrix = cairo.Matrix(x0=dimensions.x, y0=dimensions.y) # Translate
    # Multiply in correct order. Note self.transform.translate() would not work??
    self.transform *= translation_matrix  
    
    
    
