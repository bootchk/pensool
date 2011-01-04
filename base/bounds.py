#!/usr/bin/env python

'''
Bounding rectangles.

Wraps gdk.Rectangle.

Bounds are in device coords DCS.
Bounds are integers of pixel units.
'''

from gtk import gdk
import base.vector as vector

class Bounds(object):
  
  def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
    # !!! A zero width gdk.Rectangle intersects and unions incorrectly.
    if width > 0 and height > 0:
      self.value = gdk.Rectangle(x, y, width, height)
    else:
      self.value = None
  
  def __repr__(self):
    # repr by tuple
    if self.value is not None:
      return "bounds:" + str((self.value.x,self.value.y, self.value.width, self.value.height))
    else:
      return "bounds:None"
    
  def union(self, bounds):
    '''
    Union self with another bounds.
    Value attributes are gdk.Rectangles, use their union() method.
    '''
    self.value = self.value.union(bounds.value)
    
  def is_intersect(self, point):
    '''
    Return boolean whether point intersects self.
    Value attributes are gdk.Rectangles, use their intersect() method.
    '''
    bound = Bounds(point.x, point.y, 1, 1)  # single pixel bound
    # note gdk.Rectangle.intersect returns a new gdk.Rectangle
    intersection = self.value.intersect(bound.value)
    # if no intersection, all zeros
    result = not ( intersection.x == 0 and intersection.y == 0 \
    and intersection.width == 0 and intersection .height == 0 )
    return result

  
  def from_extents(self, ulx, uly, lrx, lry):
    '''
    Set value from an extent tuple.
    Typically cairo extents, floats, inked, converted to DCS.
    '''
    width = lrx - ulx
    height = lry - uly
    # FIXME round the rect
    self.value = gdk.Rectangle(int(ulx), int(uly), int(width), int(height))
    

  def from_rect(self, rect):
    '''
    Set bounds from a gdk.Rectangle.
    For drawables that are not drawn, i.e. invisible controls.
    Special case, should rarely be used.
    '''
    assert isinstance(rect, gdk.Rectangle)
    self.value = gdk.Rectangle(rect.x, rect.y, rect.width, rect.height)
    
  def center_of(self):
    '''
    Return a point (an integer pixel) of center.
    TODO does this need to be floating point?
    '''
    return vector.Vector(self.value.x + self.value.width/2, self.value.y + self.value.height/2)
    
