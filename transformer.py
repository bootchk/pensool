#!/usr/bin/env python

'''
Transformer: transforms its members.

Transforms are part of hierarchal modeling.
Primitives are unit shapes and leaves in the hierarchy.
Composites are branches of the hierarchy and transformers of their members.

Drawables are transformers.
A view is also a transformer and the root of the hierarchy.

Note Transformer does NOT override draw(), but Composite does.
!!! But Composite.draw() can be overridden, for composites having both transformed and untransformed shapes.
'''

# TODO style part of transformation?

import drawable
import cairo
import base.vector as vector
from decorators import *
import config




class Transformer(drawable.Drawable):

  def __init__(self, viewport):
    drawable.Drawable.__init__(self, viewport)
    
    # A transformer defaults to the identity transform.
    self.transform = cairo.Matrix() # assert identity transform
    
    # Specs for identity transform
    self.translation = vector.Vector(0, 0)
    self.scale = vector.Vector(1.0, 1.0)
    self.rotation = 0.0
  
  
  # @dump_return
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
    # print "CTM", context.get_matrix()
    return self.transform
  
  
  @dump_return
  def derive_transform(self):
    '''
    Set my transform from my drawing specs.
    '''
    self.transform = cairo.Matrix()
    # Standard sequence: rotate, scale, translate
    self.transform.rotate(self.rotation)
    self.transform.scale(self.scale.x, self.scale.y)  # Scale
    translation_matrix = cairo.Matrix(x0=self.translation.x, 
      y0=self.translation.y) # Translate
    # Multiply in correct order. Note self.transform.translate() would not work??
    self.transform *= translation_matrix
    return self.transform
    
  
  '''
  Setters of transform.
  Differ by component set: all, translation, scale, rotation, and pairs of.
  '''  

  @dump_event
  @view_altering
  def set_transform(self, translation, scaltion, rotation):
    '''
    Set the specs for transform, and derive transform from specs.
    '''
    # assert no need to copy these vectors?
    self.translation = translation
    self.scale = scaltion
    self.rotation = rotation
    self.derive_transform()
    
    
  @dump_event
  @view_altering
  def set_dimensions(self, dimensions):
    '''
    Set the translation and scale (not rotation) of an object.
    For testing: ordinarily, transforms are set by user actions using other methods.
    '''
    assert dimensions.width > 0
    assert dimensions.height > 0
    
    # Should be a non-empty morph (a compound)
    assert len(self) > 0
    
    self.translation = vector.Vector(dimensions.x, dimensions.y)
    self.scale = vector.Vector(dimensions.width/1.0, dimensions.height/1.0)
    self.derive_transform()
    
    
  @dump_event
  @view_altering
  def set_origin(self, event):
    ''' Set translation '''
    # FIXME floats?  CS conversions?
    self.translation = vector.Vector(event.x, event.y)
    self.derive_transform()
    
    
  @dump_event
  @view_altering
  def move_relative(self, event, offset):
    ''' 
    Translate.
    Move origin by offset.  Offset is a delta DCS. 
    '''
    # TODO calculate local coordinates by using parent transform.
    self.translation += offset
    self.derive_transform()
  
  
  # TBD not used
  @dump_event
  @view_altering
  def move_absolute(self, event):
    ''' Move origin absolute to coords in DCS. '''
    print "drawable.move_absolute", repr(self), "to ", event.x, event.y
    self.center_at(event)
    
    
  def device_to_user(self, x, y):
    # TODO do I need the model context?
    context = self.viewport.da.window.cairo_create()
    ### context.set_matrix(self.matrix)
    return vector.Vector(*context.device_to_user(x, y))
  
  
  @dump_event
  @view_altering
  def scale_uniformly(self, delta):
    self.scale *= delta
    self.derive_transform()
  
  
  @dump_event
  @view_altering
  def zoom(self, delta, event, context):
    '''
    Scale on point.
    
    Currently, the user can only do this on the document
    (not on smaller morphs.)
    
    Standard sequence of 3 transformations:
      translate
      scale
      inverse translate
    '''
    """
    When part of viewport was
    user_coords = self.device_to_user(event.x, event.y)
    self.transform.translate(user_coords.x, user_coords.y)
    self.transform.scale(delta, delta)
    self.transform.translate(-user_coords.x, -user_coords.y)
    """
    self.scale *= delta
    print "Zoomed scale is", self.scale
    self.derive_transform()
    
  @dump_event
  def center_at(self, point):
    '''
    ??? This only works for controls,
    where the scale is equivalent to pixels in DCS.
    
    Currently, there is no user command to center a graphical morph.
    '''
    delta_x = self.scale.x / 2
    delta_y = self.scale.y / 2
    self.translation = vector.Vector(point.x - delta_x, point.y - delta_y )
    self.derive_transform()
    
    """
    OLD
    '''
    Set ul at event.
    Center the bounding box at event.
    Assert bounding box is a rectangle.
    ??? Dimensions might not be a rectangle? TODO
    (No redraws)
    '''
    self._dimensions = coordinates.center_on_coords(self.get_bounds(), event)
    return self._dimensions # return rect so it is dumped
    """
 
