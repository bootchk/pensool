#!/usr/bin/env python

import base.bounds as bounds
import base.vector as vector
import base.transform as transform
import port
import style  # set_line_width
from decorators import *


def picking(func):
  '''
  Decorator: macro that prepares for drawable picking functions.
  !!! It hides the context parameter.
  '''
  def picking_func(self, point):
    # Fresh context since can be called outside a walk of model hierarchy
    context = port.view.user_context()
    if self.parent: # None if in background ctl
      context.set_matrix(transform.copy(self.parent.retained_transform))
    # !!! No style put to context, but insure black ink? TODO
    self.put_path_to(context) # recursive, with transforms
    # Transform point from DCS to UCS since Cairo in_foo() functions want UCS
    pointUCS = vector.Vector(*context.device_to_user(point.x, point.y))
    return func(self, context, pointUCS)
  return picking_func



class Drawable(object):
  '''
  Things that can be drawn (morphs, glyphs, and controls).
  
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
  
  COORDS:
  !!! Note these are all ideal coords, not inked coords.
  That is, model coords.
  FIXME
  '''
  
  def __init__(self):
    # bounds is initially a zero size bounds: it is unioned with member bounds
    self.bounds = bounds.Bounds()
    self.parent = None
    # !!! Not all Drawables have transform or style.
    
  # Feb. 16 dump_return here breaks sliding of handle menu???
  # @dump_return  # Uncomment to debug primitive draw().
  def draw(self, context):
    '''
    Draw self using context.
    Return bounds in DCS for later use to invalidate.
    
    !!! This is the primitive draw.  See also composite.draw().
    
    !!! Transform and style must already be in the context CTM.
    My parent transforms and styles me.
    '''
 
    self.put_path_to(context) # recursive, except this should be terminal!!!
    
    # Self is glyph.  Parent morph holds style.
    # Alters transform, so save
    context.save()
    style.set_line_width(context, self.parent.style.pen_width)
        
    self.bounds = self.get_stroke_bounds(context) # Cache drawn bounds
    
    # !!! Parent knows whether my style filled
    if self.parent.style.is_filled():
      context.fill()  # Filled, up to path
    else:
      context.stroke()  # Outline, with line width
    context.restore()
    # Assert fill or stroke clears paths from context
    # NOT assert context.restore() follows soon: may be one of siblings.
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
  
  # @dump_return
  def invalidate_as_drawn(self):
    ''' 
    Invalidate as previously drawn.
    Caching drawn bounds is an optimization; alternative is to walk model branch.
    This is for composite and primitive drawables: every drawable has bounds.
    '''
    port.view.surface.invalidate_rect(self.bounds.to_rect(), True)
    return self.bounds
   

  # @dump_return
  def invalidate_will_draw(self):
    '''
    Invalidate as will be drawn (hasn't been drawn yet.)
    This walks a branch of model to determine bounds.
    '''
    context = port.view.user_context()
    # Put parent retained_transform in new context, unless at top
    # !!! parent transform is inadequate, need retained_transform
    # which represents the accumulated transform from the top.
    if self.parent:
      self.parent.style.put_to(context)
      context.transform(self.parent.retained_transform)
      ##self.parent.put_transform_to(context)
    self.put_path_to(context)   # recursive
    # FIXME this is not right, the paths will have different transforms????
    will_bounds_DCS = self.get_stroke_bounds(context) # inked
    port.view.surface.invalidate_rect( will_bounds_DCS.to_rect(), True )
    return will_bounds_DCS  # for debugging
    
  """
  OLD
  @dump_event
  @view_altering
  def highlight(self, direction):
    '''
    Cause self to be temporarily drawn in the highlight style.
    Highlighting is a GUI focus issue, not a user document issue.
    '''
    # TODO Assume highlight is same bounds, i.e. don't invalidate before and after?
    self.style.highlight(direction)
  """   
      
  def dump(self):
    return repr(self) + " " + repr(self._dimensions) 
    # print "Extents:", context.path_extents()
    
  """
  '''
  Dimensions: GdkRectangle of dimensions in user coords.
  !!! These are the dimensions, not the bounds.
  The bounds of composite drawables is computed.
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
    
    # Should be a non-empty morph (a composite)
    assert len(self) > 0
    
    # Set a copy, not a reference
    self._dimensions = coordinats.copy(dimensions)
 
    
  def get_dimensions(self):
    # Return a copy, not a reference
    return coordinats.copy(self._dimensions)
  

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
    
  
  '''
  Picking.
  
  Three flavors:
    path  (ideal path as pen width approaches limit of zero.)
    stroke (inked path)
    fill
  Flavors correspond to Cairo, except we simulate in_path() which Cairo omits.
    
  These can be called outside of a walk, i.e. they set up a new context.
  !!! @picking decorator sets up the context and recursively put_path_to.
  So this is for composite and primitive drawables.
  '''
  
  @picking
  def in_path(self, context, coords):
    '''
    Does coords hit *ideal* edge of this drawable?
    Contrast to in_stroke.
    '''
    # !!! pen_width approaching zero
    style.set_line_width(context, 1)  # !!! After path
    # Cairo does not have in_path()
    return context.in_stroke(coords.x, coords.y)
    
  @picking
  def in_stroke(self, context, coords):
    '''
    Does coords hit edge of this drawable?
    Stroke: hit on inked, visible.
    Edge: not including possible interior features, just the hittable boundary.
    Distinguish from a bounding box, which is a rectangle in DCS.
    '''
    # Use actual pen width
    style.set_line_width(context, self.parent.style.pen_width)  # !!! After path
    return context.in_stroke(coords.x, coords.y)
  
  #@dump_return
  @picking
  def in_fill(self, context, coords):
    '''
    Is event in our filled shape?
    Bounding box is DCS axis aligned, drawn fill is NOT, so use in_fill().
    '''
    # Pen is immaterial to fill?
    # The fill is right up to the ideal path and the pen ink overlays fill.
    return context.in_fill(coords.x, coords.y)
    
  """
  OLD
  # @dump_return
  def in_fill(self, event):
    '''
    Is event in our filled shape?
    Bounding box is DCS axis aligned, drawn fill is NOT, so use in_fill().
    '''
    context = port.view.user_context()
    if self.parent: # None if in background ctl
      context.set_matrix(transform.copy(self.parent.retained_transform))
    self.put_path_to(context) # recursive, with transforms
    hit = context.in_fill(*context.device_to_user(event.x, event.y))
    # if not hit:
    #  print "OUT FILL", event.x, event.y, self.bounds.to_rect() # context.fill_extents(), parent_transform
    return hit
  """  
  
  @dump_return
  def is_inbounds(self, event):
    ''' 
    Is event in our bounding box?
    Intersect bounding rect with event point converted to rectangle of width one.
    '''
    return self.bounds.is_intersect(event)
    
  # @dump_return
  def get_stroke_bounds(self, context):
    '''
    Compute bounding rect in DCS of path in context as inked.
    !!! Note not recursive, takes path from context.
    '''
    return bounds.Bounds().from_context_stroke(context)

  """   
  @dump_return
  def get_center(self):
    '''
    Compute center from components (not just center of self._dimensions!)
    Returns a dimensions! not a coords. ???
    Since objects may be laid out asymetrically,
    don't use this to get the origin !!!
    '''
    return  coordinats.center_of_dimensions(self.get_bounds())
  """

  # Virtual methods
  
  '''
  Invalidate is virtual.
  Invalidate differs among subclasses:
  composite drawables: invalidate is aggregate
  primitive drawables: know their shape and may invalidate their shape, 
    but generally they invalidate a bounding box.

  Each subclass knows whether it is inked and transformed,
  and thus how to invalidate the proper rectangle in the view.
  !!! Note this is only a concern for the view and not other device ports.
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
    
    
    
    

  
      

