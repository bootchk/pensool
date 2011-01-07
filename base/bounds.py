#!/usr/bin/env python

"""
Bounding boxes (rectangles).

Wraps gdk.Rectangle.

Bounds are in device coords DCS.
Bounds are integers of pixel units.

Bounds x,y can be negative (outside the window upper left, clipped.)
Bounds width,height should not be negative.

"""

from gtk import gdk
import math
import base.vector as vector

class Bounds(object):
  """
  
  Examples:
  
  # Null bounds
  >>> Bounds()
  bounds:(0, 0, 0, 0)
  
  # is_null
  >>> Bounds().is_null()
  True

  # is_null
  >>> Bounds(0,0,1,1).is_null()
  False
  
  # Zero width and height is the null bounds
  >>> Bounds(0,0,0,0)
  bounds:(0, 0, 0, 0)
  
  # a bounds intersects a point
  >>> Bounds(0,0,1,1).is_intersect(vector.Vector(0,0))
  True
  
  # Two bounds sharing a point do NOT intersect
  # TODO bounds intersection >>> Bounds(0,0,1,1).is_intersect(vector.Vector(0,0))
  # True
  
  # a null bounds does not intersect a point
  >>> Bounds().is_intersect(vector.Vector(0,0))
  False
  
  # !!! Note null bounds is (0,0,0,0) union (0,0,1,1) does NOT adequately test union
  >>> Bounds().union(Bounds(0,0,1,1))
  bounds:(0, 0, 1, 1)
  
  # a null bounds union a non-null bounds is the non-null bounds
  >>> Bounds().union(Bounds(1,1,1,1))
  bounds:(1, 1, 1, 1)
  
  >>> Bounds(1,1,1,1).union(Bounds())
  bounds:(1, 1, 1, 1)
  
  # !!! Null bounds union null bounds is null bounds
  >>> Bounds().union(Bounds())
  bounds:(0, 0, 0, 0)
  
  # Union does NOT alter self
  >>> a = Bounds()
  >>> a.union(Bounds(1, 1, 1, 1))
  bounds:(1, 1, 1, 1)
  >>> a
  bounds:(0, 0, 0, 0)
  
  # create a bounds from extents
  >>> Bounds().from_extents(1,1,2,2)
  bounds:(1, 1, 1, 1)
  
  # calculate center
  >>> Bounds(0,0,2,2).center_of()
  (1.0,1.0)
  
  # center of unit bounds is (0,0)
  >>> Bounds(0,0,1,1).center_of()
  (0.0,0.0)
  
  # copy is not self
  >>> a = Bounds()
  >>> a is not a.copy()
  True
  
  # copy equals self
  >>> a = Bounds(1,1,1,1)
  >>> a.copy()
  bounds:(1, 1, 1, 1)
  
  TODO from_rect
  
  TODO negative width
  
  """
  
  def __init__(self, x=0, y=0, width=0, height=0):
    # !!! A negative or zero width gdk.Rectangle intersects and unions incorrectly.
    assert width >= 0
    assert height >= 0
    # A null bounds has zero width and height.  
    # It doesn't intersect with any other bounds but does union.
    self.value = gdk.Rectangle(x, y, width, height)
    """
    OLD
    if width > 0 and height > 0:
      self.value = gdk.Rectangle(x, y, width, height)
    else: # zero width or height
      self.value = None
    """
    
  def copy(self):
    if self.value is None:
      return None # FIXME error
    else:
      return Bounds(self.value.x, self.value.y, self.value.width, self.value.height)
  
  def __repr__(self):
    # repr by tuple
    if self.value is not None:
      return "bounds:" + str((self.value.x,self.value.y, self.value.width, self.value.height))
    else:
      return "bounds:None"  # FIXME error
    
    
  def union(self, bounds):
    '''
    Return union of self with another bounds.
    Unlike gdk.Rectangle, union with a null bounds is idempotent.
    
    Value attributes are gdk.Rectangles, use their union() method.
    Special case, union with null bounds.
    '''
    if self.is_null():
      return bounds.copy()  # !!! copy
    elif bounds.is_null():
      return self.copy()
    else: # both operands not null
      self.value = self.value.union(bounds.value)
      return self.copy()
  
  
  def is_null(self):
    ''' Any bounds with zero size is null '''
    return self.value.width == 0 and self.value.height == 0
    
  
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
    !!! ulx may be greater than lrx, etc.
    '''
    width = abs(lrx - ulx)
    height = abs(lry - uly)
    x = min(ulx, lrx)
    y = min(uly, lry)
    # expand float rect to outside integral pixel
    self.value = gdk.Rectangle(int(x), int(y), int(math.ceil(width)), int(math.ceil(height)))
    return self
    

  def from_rect(self, rect):
    '''
    Set bounds from a gdk.Rectangle.
    For drawables that are not drawn, i.e. invisible controls.
    Special case, should rarely be used.
    '''
    assert isinstance(rect, gdk.Rectangle)
    # TODO assert width >=0 etc
    self.value = gdk.Rectangle(rect.x, rect.y, rect.width, rect.height)
    
    
  def center_of(self):
    '''
    Return a point (an integer pixel) of center.
    TODO does this need to be floating point?
    '''
    return vector.Vector(self.value.x + self.value.width/2, self.value.y + self.value.height/2)
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    
