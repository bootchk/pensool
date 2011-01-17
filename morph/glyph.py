#!/usr/bin/env python

'''
Glyph: drawable primitives.
Note glyphs are not just text characters as in cairo.
However glyphs are primitives as in cairo.
See morph.py for discussion of strategy for instantiating.
'''

import drawable
import math
import base.orthogonal as orthogonal
import coordinates
from decorators import *
import base.vector as vector
from config import *

    
    
class Glyph(drawable.Drawable):
  '''
  Symbols in the document or model.
  Subclasses of Glyph differ in path.
  
  API: virtual methods to be implemented by subclass:
    put_path_to()
    get_orthogonal()
  
  A Glyph is in user coordinate system.
  The primary difference from a drawable
  is that a glyph does coordinate transformation at invalidate. ????
  
  A Glyph is in "natural" coordinates, i.e. at the origin and unit dimensions.
  A Glyph is a Drawable, and has a transform, but it is NOT USED.
  !!! Makes no sense to call get_dimensions() or self.transform
  
  Prototype for get_orthogonal(self, point):
    Return some vector orthogonal to self at this point on self.
    Assert point is in DCS and is on self.
    Returned orthogonal can be any length; only angle matters.
    Returned orthogonal is in DCS (angle is to screen aligned axis.)
  '''
  # __init__ inherited
  
  def __repr__(self):
    #  Simplfied reprt.  Omit this to get address of instance.
    return self.__class__.__name__
  
  
  @dump_return
  def pick(self, context, point):
    self.put_path_to(context)
    # x, y = 
    if context.in_stroke(*context.device_to_user(point.x, point.y)):
      return self.parent  # !!! Don't return a glyph, return glyph's parent morph
    else:
      return None
    
  """
  OLD
  def _aligned_rect_orthogonal(self, point):
    '''
    Return orthogonal to object with rectangular bounds.
    
    Symbol itself need not be rectangular.
    '''
    # assert bounds and point in same coordinate system (DCS)
    # assert bounds aligned with axis of coordinate system
    # TODO more general for other CS?
    return coordinates.rectangle_orthogonal(self.bounds.value, point)
  """ 

  


class LineGlyph(Glyph):
  '''
  Unit line along the x-axis.
  '''
  def put_path_to(self, context):
    context.move_to(0, 0)
    context.rel_line_to(1.0, 0)
    return

    
  def get_orthogonal(self, point):
    '''
    Return unit orthogonal to self at this point on self.
    Assert point is in DCS and is on self.
    
    For a line, point is immaterial.
    The point is on (or near?) the line and so some ortho to the line
    MUST hit the point (the point can't be on the extension
    of a finite line.)
    For a line, there are two orthogonals to a point.
    TODO choose one?
    '''
    # FIXME orthogonal.line_..
    return coordinates.line_orthogonal(self.bounds.value, point)



class RectGlyph(Glyph):
  
  # @dump_event
  def put_path_to(self, context):
    context.rectangle(0,0,1.0,1.0)  # Unit rectangle at origin

 
  @dump_return
  def get_orthogonal(self, point):
    # FIXME, should be the rotated glyph?
    return orthogonal.rect_orthogonal(self.bounds, point)
      
    
class CircleGlyph(Glyph):
  '''
  Unit circle.
  Unit diameter.
  Bounding box origin at 0,0
  '''
  @dump_event
  def put_path_to(self, context):
    # x, y, radius, ?, radians
    ## context.arc(0, 0, 1.0, 0, 2.0*math.pi)
    context.arc(0.5, 0.5, 0.5, 0, 2.0*math.pi)
    return

  
  @dump_return
  def get_orthogonal(self, point):
    '''
    '''
    # Working in DCS
    # Assert the center of the bounds is the same as the center of the circle.
    return orthogonal.circle_orthogonal(self.bounds.center_of(),  point)
    """
    OLD
    centerx, centery, radius = coordinates.circle_from_dimensions(self.bounds())
    vect_to_center = vector.Vector(centerx, centery)
    """
    """
    OLD
    center_DCS = self.bounds.center_of()
    vect_to_center = vector.Vector(center_DCS.x, center_DCS.y)
    # vector from center to point on circle
    vect_center_to_point = vector.Vector(point.x, point.y) - vect_to_center
    return vect_center_to_point.normal()
    """



    
    
    
    
    
    
    

