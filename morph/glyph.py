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
import pango
import cairo
import coordinates
from decorators import *

class Glyph(drawable.Drawable):
  '''
  Symbols in the document or model.
  Subclasses of Glyph differ in path.
  
  A Glyph is in user coordinate system.
  The primary difference from a drawable
  is that a glyph does coordinate transformation at invalidate.
  '''
  
  # __init__ inherited
  
  def invalidate(self):
    ''' 
    Invalidate means queue a region to redraw at expose event.
    GUI specific, not applicable to all surfaces.
    '''
    print "drawable.invalidate", self.dump()
    user_bounds = self.get_inked_bounds()
    device_coords = self.viewport.user_to_device(user_bounds.x, user_bounds.y)
    device_distance = self.viewport.user_to_device_distance(user_bounds.width, user_bounds.height)
    device_bounds = coordinates.dimensions(device_coords.x, device_coords.y, 
      device_distance.x, device_distance.y)
    self.viewport.surface.invalidate_rect( device_bounds, True )

  '''
  API virtual methods to be implemented by base class
    put_path_to
    orthogonal
  '''

class LineGlyph(Glyph):
  def put_path_to(self, context):
    rect = self.dimensions
    context.move_to(rect.x, rect.y)
    context.rel_line_to(rect.width, rect.height)


class RectGlyph(Glyph):
  def put_path_to(self, context):
    rect = self.dimensions
    
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
  def orthogonal(self, point):
    # assert rect is orthogonal to coordinate system
    if point.x >= self.dimensions.x + self.dimensions.width:
      rect = coordinates.dimensions(1,0, 0,0)
    elif point.x <= self.dimensions.x :
      rect = coordinates.dimensions(-1,0, 0,0)
    elif point.y >= self.dimensions.y + self.dimensions.height:
      rect = coordinates.dimensions(0,1, 0,0)
    else:
      rect = coordinates.dimensions(0,-1, 0,0)
    # FIXME catch errors
    return rect
      
    
class CircleGlyph(Glyph):
  def put_path_to(self, context):
    centerx, centery, radius = coordinates.circle_from_dimensions(self.dimensions)
    context.arc(centerx, centery, radius, 0, 2.0*math.pi)
  
  def orthogonal(self, point):
    centerx, centery, radius = coordinates.circle_from_dimensions(self.dimensions)
    center_coords = coordinates.dimensions(centerx, centery, 0, 0)
    # vector from center to point on circle
    rect = coordinates.vector_from_points(center_coords, point)
    # unitize ??
    return rect

class TextGlyph(Glyph):
  
  # !!! Override
  def __init__(self, viewport):
    self.text = "Most relationships seem so transitory"
    drawable.Drawable.__init__(self, viewport) # super
    
    
  def put_path_to(self, context):
    """
    context.cairo_select_font_face( "Purisa",
      CAIRO_FONT_SLANT_NORMAL,
      CAIRO_FONT_WEIGHT_BOLD)
    """
    rect = self.dimensions
    context.move_to(rect.x, rect.y) # Position the text reference point
    
    """
    # TODO this is cairo toy API
    context.set_font_size(13)
    # Put paths instead of text so path_extents will be right.
    context.text_path(text)
    """
    
    layout = self._layout(context)
    context.layout_path(layout)
   
   
  def _layout(self, context):
    '''
    Pango layout, for sophisticated text layout.
    Note pycairo context already supports pango
    '''
    # TODO persistent layout?
    layout = context.create_layout()
    layout.set_text(self.text)
    layout.set_wrap(pango.WRAP_WORD)
    layout.set_width(20)
    return layout
    
    
  def insertion_position(self, context):
    '''
    Return user coords of insertion bar.
    '''
    
    rect = self.dimensions  # get origin
    layout = self._layout(context)  # layout the text
    x, y = layout.get_pixel_size()  # get size of layout in user coords
    # TODO more general
    # Add origin and size to get lower right corner
    rect2 = coordinates.dimensions(rect.x + x, rect.y + y, 0, 0)
    # print "IB cursor", layout.get_cursor_pos(15)
    return rect2
    
    
    
    
    
    
    
    

