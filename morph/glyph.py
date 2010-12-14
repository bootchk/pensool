#!/usr/bin/env python

'''
Glyph: drawable primitives.
Note glyphs are not just text characters as in cairo.
However glyphs are primitives as in cairo.
See morph.py for discussion of strategy for instantiating.
'''

import drawable
import math
import coordinates
from decorators import *
import base.vector



    
    
class Glyph(drawable.Drawable):
  '''
  Symbols in the document or model.
  Subclasses of Glyph differ in path.
  
  A Glyph is in user coordinate system.
  The primary difference from a drawable
  is that a glyph does coordinate transformation at invalidate. ????
  
  A Glyph is in "natural" coordinates, i.e. at the origin and unit dimensions.
  A Glyph is a Drawable, and has a transform, but it is NOT USED.
  !!! Makes not sense to call get_dimensions() or self.transform
  '''
  
  # __init__ inherited
  
  @dump_event
  def invalidate(self):
    ''' 
    Invalidate means queue a region to redraw at expose event.
    GUI specific, not applicable to all surfaces.
    '''
    user_bounds = self.get_inked_bounds()
    device_coords = self.viewport.user_to_device(user_bounds.x, user_bounds.y)
    device_distance = self.viewport.user_to_device_distance(user_bounds.width, user_bounds.height)
    device_bounds = coordinates.dimensions(device_coords.x, device_coords.y, 
      device_distance.x, device_distance.y)
    self.viewport.surface.invalidate_rect( device_bounds, True )


  def _aligned_rect_orthogonal(self, point):
    '''
    Return orthogonal to object with rectangular dimensions or bounding box.
    
    Symbol itself need not be rectangular.
    '''
    # assert rect is orthogonal to coordinate system
    rect = self.get_dimensions()
    return coordinates.rectangle_orthogonal(rect, point)
    

  '''
  API virtual methods to be implemented by subclass
    put_path_to()
    get_orthogonal()
  '''


class LineGlyph(Glyph):
  '''
  A straight line.
  
  Traditionally a line is defined by two points.
  Here a line is defined by a rect: 
  x,y is first point
  x+width, y+height is second point.
  '''
  def put_path_to(self, context):
    # unit line along x-axis
    context.move_to(0, 0)
    context.rel_line_to(1, 0)
    return
    
    rect = self.get_dimensions()
    context.move_to(rect.x, rect.y)
    context.rel_line_to(rect.width, rect.height)
    
  def get_orthogonal(self, point):
    return coordinates.line_orthogonal(self.get_dimensions(), point)



class RectGlyph(Glyph):
  def put_path_to(self, context):
    context.rectangle(0,0,1,1)  # Unit rectangle at origin
    return
    
    rect = self.get_dimensions()
    
    point = coordinates.center_of_dimensions(rect)
    cdims = coordinates.center_on_origin(rect)
    
    """
    # 1.  tr, rot, tr, the standard way
    context.save()
    context.translate(-point.x, -point.y)
    context.rotate(0.5)
    context.translate(point.x, point.y)
    context.rectangle(rect)
    context.restore()
    """
    # 2. paths in object coords (centered on origin)
    context.save()
    context.translate(point.x, point.y)
    context.rotate(0.0)   # TODO use rotation of glyph
    context.rectangle(cdims)
    context.restore()
    """
    context.transform(transformation)
    # context.set_matrix(transformation)
    context.rectangle(rect.x, rect.y, rect.width, rect.height)
    context.restore()
    """
    """
    context.save()
    context.translate(point.x, point.y)
    context.rotate(0.5)
    context.translate(point.x, point.y)
    context.rectangle(rect.x, rect.y, rect.width, rect.height)
    context.stroke()  # ???? Restore destroy the path?
    context.restore()
    """
    """
    context.save()
    transformation = cairo.Matrix()
    transformation.translate(-rect.x, -rect.y)
    transformation.rotate(0.5)
    transformation.translate(rect.x, rect.y)
    context.set_matrix(transformation)
    context.rectangle(rect.x, rect.y, rect.width, rect.height)
    context.restore()
    """
    """
    print "Rect", rect
    saved = context.get_matrix()
    print "Original matrix", saved
    transformation = cairo.Matrix()
    transformation.rotate(0.5)
    transformation.scale(rect.width, rect.height)
    transformation.translate(rect.x, rect.y)
    # context.transform(transformation)
    context.set_matrix(transformation)
    context.rectangle(-0.5, -0.5, 1, 1)
    #context.restore()
    context.set_matrix(saved)
    """
    """
    # OLD
    context.rectangle(rect.x, rect.y, rect.width, rect.height)
    """
  
  @dump_return
  def get_orthogonal(self, point):
    return self._aligned_rect_orthogonal(point)
      
    
class CircleGlyph(Glyph):
  def put_path_to(self, context):
    # Unit circle
    context.arc(0, 0, 1, 0, 2.0*math.pi)
    return
    
    centerx, centery, radius = coordinates.circle_from_dimensions(self.get_dimensions())
    context.arc(centerx, centery, radius, 0, 2.0*math.pi)
  
  @dump_return
  def get_orthogonal(self, point):
    centerx, centery, radius = coordinates.circle_from_dimensions(self.get_dimensions())
    vect_to_center = base.vector.Vector(centerx, centery)
    # vector from center to point on circle
    vect_center_to_point = base.vector.Vector(point.x, point.y) - vect_to_center
    return vect_center_to_point.normal()



    
    
    
    
    
    
    

