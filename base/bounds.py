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
import itertools

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
  >>> Bounds(0,0,0,0).is_null()
  True
  
  # Assertion raised on floats
  >>> Bounds(0,0,1.0,1)
  Traceback (most recent call last):
  ...
  AssertionError

  
  # a bounds intersects a point
  >>> Bounds(0,0,1,1).is_intersect(vector.Vector(0,0))
  True
  
  # a bounds intersects a floating point
  >>> Bounds(0,0,1,1).is_intersect(vector.Vector(0.1, 0.2))
  True
  
  # bounds NOT intersect a point at lower left of bounds
  >>> Bounds(0,0,1,1).is_intersect(vector.Vector(1, 1))
  False
  
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
  
  # bounds from extents snaps to outside pixel boundary
  >>> Bounds().from_extents(.75, .75, 1.2, 1.2)
  bounds:(0, 0, 2, 2)
  
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
  
  # iteration
  >>> for corner in Bounds(1,1,1,1): corner
  (1.0,1.0)
  (2.0,1.0)
  (2.0,2.0)
  (1.0,2.0)
  
  # generate sides
  >>> for side in Bounds(1,1,1,1).sides(): side
  ((1.0,1.0), (2.0,1.0))
  ((2.0,1.0), (2.0,2.0))
  ((2.0,2.0), (1.0,2.0))
  ((1.0,2.0), (1.0,1.0))

  TODO from_rect
  
  TODO negative width
  
  """
  
  def __init__(self, x=0, y=0, width=0, height=0):
    # !!! A negative or zero width gdk.Rectangle intersects and unions incorrectly.
    assert width >= 0
    assert height >= 0
    # A null bounds has zero width and height.  
    # It doesn't intersect with any other bounds but does union.
    assert isinstance(width, int)
    assert isinstance(height, int)
    assert isinstance(x, int)
    assert isinstance(y, int)
    self.value = gdk.Rectangle(x, y, width, height)
    """
    OLD
    if width > 0 and height > 0:
      self.value = gdk.Rectangle(x, y, width, height)
    else: # zero width or height
      self.value = None
    """
    
    
  def __iter__(self):
    ''' 
    Iteration on Bounds returns the corner points. 
    !!! Don't mutate the bounds while iterating.
    '''
    return itertools.islice( [vector.Vector(self.value.x, self.value.y),
      vector.Vector(self.value.x + self.value.width, self.value.y),
      vector.Vector(self.value.x + self.value.width, self.value.y + self.value.height),
      vector.Vector(self.value.x, self.value.y + self.value.height)], None )

  def sides(self):
    '''
    Generator of sides.
    '''
    # build list of sides
    previous_corner = None
    sides = []
    for corner in self:
      if previous_corner:
        sides.append((previous_corner, corner))
      else:
        first_corner = corner
      previous_corner = corner
    # last side
    sides.append((previous_corner, first_corner))
    
    for side in sides:
      yield side


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
    Point can be float.
    Value attributes are gdk.Rectangles, use their intersect() method.
    '''
    bound = Bounds(int(point.x), int(point.y), 1, 1)  # single pixel bound
    # note gdk.Rectangle.intersect returns a new gdk.Rectangle
    intersection = self.value.intersect(bound.value)
    # if no intersection, all zeros
    result = not ( intersection.x == 0 and intersection.y == 0 \
    and intersection.width == 0 and intersection .height == 0 )
    return result

  
  def from_extents(self, ulx, uly, lrx, lry):
    '''
    Set value from an extent tuple.
    For example, cairo extents, floats, inked, converted to DCS.
    
    !!! ulx may be greater than lrx, etc. due to transformations
    
    !!! Extents may be either path (ideal) or stroke (inked).
    The ideal extent of a line can have zero width or height.
    
    !!! User may zoom out enough that bounds approach zero,
    even equal zero?
    
    !!! Parameters are float i.e. fractional.
    Bounds are snapped to the outside pixel boundary.
    '''
    # Snap to integer boundaries and order on the number line
    minxi = int(min(ulx, lrx))
    minyi = int(min(uly, lry))
    maxxi = math.ceil(max(ulx, lrx))
    maxyi = math.ceil(max(uly, lry))
    width = maxxi - minxi
    height = maxyi - minyi
    # width or height or both can be zero, for example setting transform on empty model
    
    # snap float rect to outside integral pixel
    self.value = gdk.Rectangle(minxi, minyi, width, height)
    # not assert x,y positive
    # assert self.value.width >= 0  # since abs used
    if self.is_null():
      print "!!!!!!!!!!!! Null bounds", self
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

    
