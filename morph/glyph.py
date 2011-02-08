#!/usr/bin/env python

'''
Glyph: drawable primitives.
Note glyphs are not just text characters as in cairo.
However glyphs are primitives as in cairo.
See morph.py for discussion of strategy for instantiating.
'''

import drawable
from math import pi as PI
import base.orthogonal as orthogonal
import base.vector as vector
from decorators import *

# import traceback
# traceback.print_stack()
    
    
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
  A Glyph is a Drawable, usually transformed, but not a Transformer.
  
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
  
  
  # @dump_return
  def pick(self, context, point):
    self.put_path_to(context)
    # x, y = 
    if context.in_stroke(*context.device_to_user(point.x, point.y)):
      return self.parent  # !!! Don't return a glyph, return glyph's parent morph
    else:
      return None
    
  def cleanse(self):
    # No transforms to cleanse
    return
  


class LineGlyph(Glyph):
  '''
  Unit line along the x-axis.
  '''
  def put_path_to(self, context):
    context.move_to(0, 0)
    context.line_to(1.0, 0)
    return

    
  def get_orthogonal(self, point):
    '''
    Return unit orthogonal to drawn self at this point on self.
    Assert point is in DCS and is on self.
    Note drawn self means in the DCS.
    Note the orthogonal does NOT necessarily pass through the point.
    TODO return one of two directional orthogonal vectors,
    the one that is in the direction of the mouse trail (not the point.)
    
    For a line, point is immaterial.
    The point is on (or near) the line and so some ortho to the line
    MUST hit the point (the point can't be on the extension
    of a finite line.)
    
    For a line, there are two orthogonals to a point.
    This is a somewhat arbitray one for now.
    '''
    x, y = self.parent.retained_transform.transform_point(0,0)
    point1 = vector.Vector(x,y)
    x, y = self.parent.retained_transform.transform_point(1.0,0)
    point2 = vector.Vector(x,y)
    return orthogonal.line_orthogonal(point1, point2)



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
  # @dump_event
  def put_path_to(self, context):
    # x, y, radius, ?, radians
    ## context.arc(0, 0, 1.0, 0, 2.0*PI)
    context.arc(0.5, 0.5, 0.5, 0, 2.0*PI)
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



    
    
    
    
    
    
    

