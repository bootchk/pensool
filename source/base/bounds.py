#!/usr/bin/env python

"""
Bounding boxes (rectangles).

Bounds are in device coords DCS.
Bounds are integers of pixel units.

Bounds x,y can be negative (outside the window upper left, clipped.)
Bounds width,height should not be negative.

(Formerly a wrapper of gdk.Rectangle.)

To test:
python -m doctest -v base/bounds.py
"""
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

from gtk import gdk
import math
import base.vector as vector
import itertools

class Bounds(object):
  """
  Bounding box in device pixel units.
  
  Examples:
  
  # Null bounds
  >>> Bounds()
  (0, 0, 0, 0)
  
  # A new Bounds is is_null
  >>> Bounds().is_null()
  True

  # A non-empty Bounds is not is_null
  >>> Bounds(0,0,1,1).is_null()
  False
  
  # Zero width and height is the null bounds
  >>> Bounds(0,0,0,0).is_null()
  True
  
  # Assertion raised on float arguments
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
  
  # bounds DOES intersect a point at lower right of bounds
  >>> Bounds(0,0,1,1).is_intersect(vector.Vector(1, 1))
  True
  
  # TODO Two bounds sharing a point do NOT intersect
  
  # bounds DOES intersect a point at upper left of bounds
  >>> Bounds(0,0,1,1).is_intersect(vector.Vector(0,0))
  True
  
  # a null bounds does not intersect a point
  >>> Bounds().is_intersect(vector.Vector(0,0))
  False
  
  >>> Bounds(0,0,1,1).union(Bounds(1,1,2,2))
  (0, 0, 3, 3)
  
  # !!! Note null bounds is (0,0,0,0) union (0,0,1,1) does NOT adequately test union
  >>> Bounds().union(Bounds(0,0,1,1))
  (0, 0, 1, 1)
  
  # a null bounds union a non-null bounds is the non-null bounds
  >>> Bounds().union(Bounds(1,1,1,1))
  (1, 1, 1, 1)
  
  >>> Bounds(1,1,1,1).union(Bounds())
  (1, 1, 1, 1)
  
  # !!! Null bounds union null bounds is null bounds
  >>> Bounds().union(Bounds())
  (0, 0, 0, 0)
  
  # Union does NOT alter self
  >>> a = Bounds()
  >>> a.union(Bounds(1, 1, 1, 1))
  (1, 1, 1, 1)
  >>> a
  (0, 0, 0, 0)
  
  # create a bounds from extents
  >>> Bounds().from_extents(1,1,2,2)
  (1, 1, 1, 1)
  
  # bounds from extents snaps to outside pixel boundary
  >>> Bounds().from_extents(.75, .75, 1.2, 1.2)
  (0, 0, 2, 2)
  
  # bounds from extents snaps to outside pixel boundary on negative
  >>> Bounds().from_extents(-0.1, -0.1, 0.0, 0.0)
  (-1, -1, 1, 1)
  
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
  (1, 1, 1, 1)
  
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
    # self = gdk.Rectangle(x, y, width, height)
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    
    
  def __iter__(self):
    ''' 
    Iteration on Bounds returns the corner points. 
    !!! Don't mutate the bounds while iterating.
    '''
    return itertools.islice( [vector.Vector(self.x, self.y),
      vector.Vector(self.x + self.width, self.y),
      vector.Vector(self.x + self.width, self.y + self.height),
      vector.Vector(self.x, self.y + self.height)], None )

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
    return Bounds(self.x, self.y, self.width, self.height)
  
  def __repr__(self):
    # repr by tuple
    return str((self.x,self.y, self.width, self.height))
    
    
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
      ## self = self.union(bounds.value)
      ## return self.copy()
      r1 = self.to_rect()
      r2 = bounds.to_rect()
      r3 = r1.union(r2)
      return Bounds().from_rect(r3)
      
  
  
  def is_null(self):
    ''' Any bounds with zero size is null '''
    return self.width == 0 and self.height == 0
    
  
  def is_intersect(self, point):
    '''
    Return boolean whether point intersects self.
    Point can be float.
    '''
    """OLD
    Value attributes are gdk.Rectangles, use their intersect() method.
    bound = Bounds(int(point.x), int(point.y), 1, 1)  # single pixel bound
    # note gdk.Rectangle.intersect returns a new gdk.Rectangle
    intersection = self.intersect(bound.value)
    # if no intersection, all zeros
    result = not ( intersection.x == 0 and intersection.y == 0 \
    and intersection.width == 0 and intersection .height == 0 )
    return result
    """
    # A null bounds intersects no points
    if self.is_null():
      return False
    return point.x >= self.x \
      and point.x <= (self.x + self.width) \
      and point.y >= self.y \
      and point.y <= (self.y + self.height)
    
    
  def from_context_stroke(self, context):
    '''
    Get the DCS bounds of the path in the graphics context.
    Stroke, that is, as inked, not as ideal path.
    '''
    # extents of rect in UCS, aligned with axis
    ulx, uly, lrx, lry = context.stroke_extents() 
    # Two other corners of the rect
    llx = ulx
    lly = lry
    urx = lrx
    ury = uly
    # Four points in DCS, corners of rect NOT axis aligned,
    # and no relationships known between points in DCS
    p1xd, p1yd = context.user_to_device(ulx, uly)
    p2xd, p2yd = context.user_to_device(llx, lly)
    p3xd, p3yd = context.user_to_device(lrx, lry)
    p4xd, p4yd = context.user_to_device(urx, ury)
    # DCS bounds are min and max of device coords of all four points.
    # Snap to outside pixel using floor, ceiling.
    # Convert to int
    minxi = int(math.floor(min(p1xd, p3xd, p2xd, p4xd)))
    minyi = int(math.floor(min(p1yd, p3yd, p2yd, p4yd)))
    maxxi =  int(math.ceil(max(p1xd, p3xd, p2xd, p4xd)))
    maxyi =  int(math.ceil(max(p1yd, p3yd, p2yd, p4yd)))
    width = maxxi - minxi
    height = maxyi - minyi
    self = Bounds(minxi, minyi, width, height)
    # !!! Cannot assert not is_null: line width tiny or other factors
    # may yield empty stroke extents.
    return self
    
  
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
    # Snap to integer boundaries and order on the number line.
    # !!! Note int(floor()) not just int()
    minxi = int(math.floor(min(ulx, lrx)))
    minyi = int(math.floor(min(uly, lry)))
    maxxi = int(math.ceil(max(ulx, lrx)))
    maxyi = int(math.ceil(max(uly, lry)))
    width = maxxi - minxi
    height = maxyi - minyi
    # width or height or both can be zero, for example setting transform on empty model
    
    # snap float rect to outside integral pixel
    ## self = gdk.Rectangle(minxi, minyi, width, height)
    self = Bounds(minxi, minyi, width, height)
    # not assert x,y positive
    # assert self.width >= 0  # since abs used
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
    self = Bounds(rect.x, rect.y, rect.width, rect.height)
    return self
  
  
  def to_rect(self):
    return gdk.Rectangle(self.x, self.y, self.width, self.height)
    
    
  def center_of(self):
    '''
    Return a point (an integer pixel) of center.
    TODO does this need to be floating point?
    '''
    return vector.Vector(self.x + self.width/2, self.y + self.height/2)
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    
