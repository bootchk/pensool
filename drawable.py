#!/usr/bin/env python

import coordinates
import base.bounds as bounds
import style
from decorators import *
import base.vector as vector





class Drawable(object):
  '''
  Things that can be drawn (morphs, glyphs, and controls).
  (Dimensions: see transformer.py.  Style: see style.py) 
  
  DRAWING:
  See below draw()
  See below virtual method put_path_to() which distinguishes subclasses.
  
  SURFACES:
  Drawing is on a surface (device or file).
  Some of this is specific to a GUI surface (a display).
  Queries, such as is_inbounds() are for GUI's.
  
  CONTROL subclasses:
  Controls are specific to a GUI, but there is no reason
  controls could not be drawn to another surface.
  
  Some controls are not actually be drawn (the background manager), 
  but data is there to support it.
  
  COORDINATES:
  !!! Note these are all ideal coordinates, not inked coordinates.
  That is, model coordinates.
  FIXME
  '''
  
  def __init__(self, viewport):
    self._dimensions = coordinates.any_dims()
    self.viewport = viewport
    self.style = style.Style()
    # bounds is initially a zero size bounds: it is unioned with member bounds
    self.bounds = bounds.Bounds()
    self.parent = None
    
  
  @dump_return  # Uncomment this to see drawables drawn.
  def draw(self, context):
    '''
    Draw self using context.
    Return bounds in DCS for later use to invalidate.
    
    !!! This is the primitive draw.  See also composite.draw().
    
    !!! Transformation must already be in the context CTM.
    My parent transforms me.
    
    !!! Style is already in the context.
    I inherit my parent style, but I can override.
    '''
    self.put_path_to(context) # recursive
    self.style.put_to(context)
    # TODO is this right, or do need to save context?
    
    # Cache my drawn bounds
    self.bounds = self.get_path_bounds(context)
    assert not self.bounds.is_null()
    
    if self.style.is_filled():
      context.fill()  # Filled, up to path
    else:
      context.stroke()  # Outline, with line width
    # Assert fill or stroke clears paths from context
    
    return self.bounds.copy()   # Return reference to copy, not self
    
  '''
  Invalidate means queue a region to redraw at expose event.
  The region is rectangular, axis aligned, in DCS.
  GUI specific, not applicable to all surfaces.
  
  !!!
  Invalidate functions can be called outside a complete walk of model tree.
  Invalidate functions are NOT recursively called.
  Thus they fabricate a new context out of parent transform and style.
  And call a recursive function, put_path_to().
  '''
  
  @dump_return
  def invalidate_as_drawn(self):
    ''' 
    Invalidate as previously drawn.
    This is an optimization: caching drawn bounds.
    This is for composite and primitive drawables: every drawable has bounds.
    '''
    """
    OLD
    self.viewport.surface.invalidate_rect( 
      coordinates.integral_rect(self.drawn_dims), True )
    """
    self.viewport.surface.invalidate_rect(self.bounds.value, True)
    return self.bounds
   

  @dump_return
  def invalidate_will_draw(self):
    '''
    Invalidate as will be drawn (hasn't been drawn yet.)
    This walks a branch of model to determine bounds.
    '''
    context = self.viewport.user_context()
    # Put parent transform in new context, unless at top
    if self.parent:
      self.parent.style.put_to(context)
      self.parent.put_transform_to(context)
    self.put_path_to(context)   # recursive
    will_bounds_DCS = self.get_path_bounds(context) # inked
    self.viewport.surface.invalidate_rect( will_bounds_DCS.value, True )
    return will_bounds_DCS  # for debugging
    
    
  @dump_event
  @view_altering
  def highlight(self, direction):
    '''
    Cause self to be temporarily drawn in the highlight style.
    Highlighting is a GUI focus issue, not a user document issue.
    '''
    # TODO Assume highlight is same bounds, i.e. don't invalidate before and after?
    self.style.highlight(direction)
      
      
  def dump(self):
    return repr(self) + " " + repr(self._dimensions) 
    # print "Extents:", context.path_extents()
    
  """
  '''
  Dimensions: GdkRectangle of dimensions in user coordinates.
  !!! These are the dimensions, not the bounds.
  The bounds of compound drawables is computed.
  !!! Copy, not reference, in case parameters are mutable.
  '''
  @dump_event
  def set_dimensions(self, dimensions):
    '''
    Set the translation and scale of an object.
    For testing: ordinarily, transforms by user actions using other methods.
    '''
    assert dimensions.width > 0
    assert dimensions.height > 0
    
    # Should be a non-empty morph (a compound)
    assert len(self) > 0
    
    # Set a copy, not a reference
    self._dimensions = coordinates.copy(dimensions)
 
    
  def get_dimensions(self):
    # Return a copy, not a reference
    return coordinates.copy(self._dimensions)
  

  def set_origin(self, coords):
    '''
    Set the origin part of the dimensions.
    That is, move without changing shape or size.
    No redraw.
    Note the origin has different meanings for different subclasses:
    it might be the upper left or it might be a hotspot or a center.
    TODO property
    '''
    self._dimensions.x = coords.x
    self._dimensions.y = coords.y
  
  def get_origin(self):
    # don't return a reference, return a copy
    return vector.Vector(self._dimensions.x, self._dimensions.y)
  """
  
  def get_drawn_origin(self):
    ''' Return device coords of origin where drawn.'''
    return vector.Vector(self.bounds.x, self.bounds.y)
  
  
  def put_edge_to(self, context):
    '''
    Put my boundary in the context.
    For most drawables (e.g. circle), the path is the boundary.
    If NOT path is boundary, override.  E.G. text has a frame.
    This is used for hit detection.
    '''
    self.put_path_to(context)
    
    
  def is_inpath(self, user_coords):
    '''
    Does mouse hit this drawable?
    Are coords in my edge?
    
    Note user coords, not device coords.
    To hit path from a distance, ink the path wider: context.set_line_width(25)
    '''
    # TODO pass a context  .save() and restore()
    context = self.viewport.user_context()
    self.put_edge_to(context)
    hit = context.in_stroke(user_coords.x, user_coords.y)
    return hit
  
  
  @dump_return
  def is_inbounds(self, event):
    ''' 
    Is event in our bounding box?
    Intersect bounding rect with event point converted to rectangle of width one.
    '''
    return self.bounds.is_intersect(event)
  
  
  @dump_return
  def get_path_bounds(self, context):
    '''
    Compute bounding rect in DCS of path in context as inked.
    !!! Note not recursive, takes path from context.
    '''
    x1, y1, x2, y2 = context.stroke_extents()
    assert x2 - x1 >= 0
    assert y2 - y1 >= 0
    x1, y1 = context.user_to_device(x1, y1)
    x2, y2 = context.user_to_device(x2, y2)
    # !!! Note still floats and might be negative width
    a_bounds = bounds.Bounds().from_extents(x1, y1, x2, y2)
    ### bounds = coordinates.dimensions_from_float_extents(x1, y1, x2, y2)
    return a_bounds
    
    
  
 
    
   
      
  @dump_return
  def get_center(self):
    '''
    Compute center from components (not just center of self._dimensions!)
    Returns a dimensions! not a coordinates. ???
    Since objects may be laid out asymetrically,
    don't use this to get the origin !!!
    '''
    return  coordinates.center_of_dimensions(self.get_bounds())


  # Virtual methods
  
  '''
  Invalidate is virtual.
  Invalidate differs among subclasses:
  composite drawables: invalidate is aggregate
  primitive drawables: know their shape and may invalidate their shape, 
    but generally they invalidate a bounding box.

  Each subclass knows whether it is inked and transformed,
  and thus how to invalidate the proper rectangle in the viewport.
  !!! Note this is only a concern for the viewport and not other device ports.
  '''
  
  def is_in_control_area(self, event):
    '''
    Is the event in the hot area.
    Usually only for control subclass of drawable.
    '''
    raise NotImplementedError("Virtual")
    
    
  def put_path_to(self, context):
    '''
    Put path into context.
    Virtual: each subclass knows its own shape.
    '''
    raise NotImplementedError("Virtual")


  def get_orthogonal(self, point):
    '''
    Return an orthogonal unit vector at given point on boundary.
    
    Virtual: each subclass knows its own shape.
    '''
    print self
    raise NotImplementedError("Virtual")
    
    
    
    

  
      

