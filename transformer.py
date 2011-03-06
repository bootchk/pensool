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
# TODO derive_transform part of view_altering?

import drawable
import cairo
import base.vector as vector
from decorators import *
import config




class Transformer(drawable.Drawable):
  '''
  A transformer (of coordinate systems) 
  '''

  #@dump_event
  def __init__(self):
    drawable.Drawable.__init__(self)
    
    # My transform.
    # Default to identity transform.
    self.transform = cairo.Matrix() # assert identity transform
    
    # Retained transform: saved cumulative transform from walking hierarchy.
    self.retained_transform = cairo.Matrix()  # Identity transform is benign
    
    # Specs for self.transform: identity transform
    self.translation = vector.Vector(0, 0)
    self.scale = vector.Vector(1.0, 1.0)
    self.rotation = 0.0
    
  '''
  Pickling.
  
  These must be defined because cairo.Matrix() is not picklable, throws exception when pickled.
  These are defined here, and not in Drawable.
  Drawables are picklable (including glyphs) but they aren't transformers (don't have Matrix())
  and pickle using built-in pickling functions.
  '''
  def __getstate__(self):
    """Return state values to be pickled."""
    # !!! Parent is state, but top parent must be severed to avoid pickling entire tree
    # as a forward and backward linked graph.
    return (self.translation, self.scale, self.rotation, self.style, self.parent)

  def __setstate__(self, state):
    """Restore state from the unpickled state values."""
    self.translation, self.scale, self.rotation, self.style, self.parent = state
    # Cached state recalculated now or at first tree walk.
    self.retained_transform = cairo.Matrix()  # Identity transform is benign until walk.
    self.derive_transform() # now
  
  
  # @dump_return
  def put_transform_to(self, context):
    '''
    Apply my transform to the current transform in the context.
    FIXME and style?
    '''
    try:
      context.transform(self.transform)
    except cairo.Error:
      print self.transform
      raise
    self.style.put_to(context)
    # print "CTM", self.transform, context.get_matrix()
    # Save a copy (!!!) of the CTM
    self.retained_transform = cairo.Matrix() * context.get_matrix()
    return self.retained_transform  # debugging
    
  
  
  # @dump_return
  def derive_transform(self):
    '''
    Set my transform from my drawing specs.
    !!! Afterwards, retained_transform doesn't correspond until walk model tree
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
   
  
  # @dump_return
  def device_to_local(self, point):
    '''
    Get local coordinates (group GCS) of DCS point.
    Uses parent retained transform: only works if previously model traversed and transforms derived.
    Will not work for the model (the top.)
    '''
    if self.parent:
      group_transform = cairo.Matrix() * self.parent.retained_transform
    else:
      # At the top, self is model.  Model's transform (viewing) transforms device to local.
      group_transform = cairo.Matrix() * self.transform
    group_transform.invert()
    # print group_transform
    return vector.Vector(*group_transform.transform_point(point.x, point.y))
    
    
  """
  def device_to_user(self, x, y):
    # TODO do I need the model context?
    context = self.view.da.window.cairo_create()
    ### context.set_matrix(self.matrix)
    return vector.Vector(*context.device_to_user(x, y))
  """
  
  '''
  Setters of transform.
  Differ by component set: all, translation, scale, rotation, and pairs of.
  '''  

  '''
  NOT @view_altering.  Caller must be view_altering.
  Because some callers are just initializing, e.g. menus and model top.
  '''
  #@dump_return
  def set_transform(self, translation, scaltion, rotation):
    '''
    Set the specs for transform, and derive transform from specs.
    '''
    # copy these vectors so correspond with transform
    self.translation = translation.copy()
    self.scale = scaltion.copy()
    self.rotation = rotation  # scalar
    self.derive_transform()
    return self.transform # debug
    
    
  # This will alter the view, but for now its broken on retained transform
  # @view_altering
  # @dump_return
  def set_dimensions(self, dimensions):
    '''
    Set the translation and scale (not rotation) of an object.
    For testing: ordinarily, transforms are set by user actions using other methods.
    !!! Not view altering
    '''
    assert dimensions.width > 0
    assert dimensions.height > 0
    
    # Should be a non-empty morph (a compound)
    assert len(self) > 0
    
    self.translation = vector.Vector(dimensions.x, dimensions.y)
    self.scale = vector.Vector(dimensions.width/1.0, dimensions.height/1.0)
    self.derive_transform()
    return self.transform # debug

  def set_translation(self, point):
    '''
    !!! Not view altering (can be called before view is established.)
    !!! point is not copied.
    '''
    self.translation = point
    self.derive_transform()
  
  @view_altering
  @dump_event
  def set_origin(self, event):
    ''' Set translation '''
    # FIXME floats?  CS conversions?
    self.translation = vector.Vector(event.x, event.y)
    self.derive_transform()
  
  
  def move_origin(self, offset):
    '''
    Move origin but keep other points fixed.
    '''
    raise RuntimeError("Not implemented")
    
    
  @view_altering
  # @dump_event
  def move_relative(self, offset):
    ''' 
    Translate.
    Move origin by offset.  Offset is a delta in LCS (any really). 
    '''
    # TODO calculate local coordinates by using parent transform.
    self.translation += offset
    self.derive_transform()
  
  @view_altering
  #@dump_event
  def move_absolute(self, offset):
    ''' Set translation by offset.'''
    self.translation = offset.copy()
    self.derive_transform()
    
  @view_altering
  @dump_event
  def scale_uniformly(self, delta):
    ''' Relative scale uniformly by the scalar delta'''
    self.scale *= delta
    self.derive_transform()
  
  @view_altering
  @dump_event
  def relative_scale(self, delta_x, delta_y):
    ''' Relative scale each dimension by the scalar tuple delta'''
    self.scale.x *= delta_x
    self.scale.y *= delta_y
    self.derive_transform()
  
  @view_altering
  @dump_event
  def rotate(self, angle):
    self.rotation = angle
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
    When part of view was
    user_coords = self.device_to_user(event.x, event.y)
    self.transform.translate(user_coords.x, user_coords.y)
    self.transform.scale(delta, delta)
    self.transform.translate(-user_coords.x, -user_coords.y)
    """
    self.scale *= delta
    print "Zoomed scale is", self.scale
    self.derive_transform()
    
  #@dump_event
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
 
