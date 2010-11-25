#!/usr/bin/env python


'''
Geometry calculations.

Points, coordinates, vectors, rects.

Hides many ways to specify rectangles.

Note this is all in one coordinate system:
does NOT translate between different coordinate systems.

Coordinates: any object that has .x and .y attributes

Dimensions and Bounds: 
  gdk.Rectangle (upper left x, upper left y, width, height)
  The *origin* is the upper left point.
 
Extents:
  gdk.Rectangle (ulx, uly, lrx, lry)
  
Bounds:
  Here, the dimensions always bound the abstract components.
  In general, the bounds may differ:
    when inked, the line widths may increase the drawn bounds.
    for other designs, the components may extend outside the dimensions.

We always return a new gdk.Rectangle
because parameters might be mutable and we don't want references
to a parameter, we want a copy.
!!! Note a gdk.Rectangle is integer.
Cairo coordinate transformations often return floats.

There is no GTK Point object, we often use a gdk.Rectangle 
which has the API of a point (i.e. .x and .y attributes.)

This should be the only module that import gdk and uses gdk.Rectangle.
'''

from gtk import gdk
import math
import cairo
from decorators import *


class UserCoords(object):
  '''
  A simple class that takes a tuple 
  and returns a structure with named attributes.
  This type is only used for the user coordinate system.
  '''
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
class DeviceCoords(object):
  '''
  A simple class that takes a tuple 
  and returns a structure with named attributes.
  This type is only used for the device coordinate system.
  '''
  def __init__(self, x, y):
    self.x = x
    self.y = y


def copy(dim):
  return gdk.Rectangle(dim.x, dim.y, dim.width, dim.height)


def circle_from_dimensions(dim):
  '''
  Return parameters of a circle from a dimension rect.
  The circle must fit in the dimensions.
  Returns: center x, center y, radius
  '''
  #TODO make sure radius fits inside, min of width and height
  half_width = dim.width/2
  half_height = dim.height/2
  return dim.x + half_width, dim.y + half_height, half_width
  
  
def center_of_dimensions(dim):
  '''
  Returns a point (a rect) that is the center of the dimensions.
  '''
  rect = gdk.Rectangle(dim.x + dim.width/2, dim.y + dim.height/2, 1, 1)
  # print "coordinates.center_of_dimensions", rect
  return rect


def center_on_coords(dim, point):
  '''
  Returns dimensions with ul at point.
  Takes the width and height from the dimensions.
  '''
  rect = gdk.Rectangle(point.x - (dim.width/2), point.y - (dim.height/2),
    dim.width, dim.height)
  return rect
  

def center_on_origin(dim):
  '''
  Returns rect translated so its center is at the origin (0,0)
  '''
  center = center_of_dimensions(dim)
  # FIXME call center_on_coords(center)
  rect = gdk.Rectangle(dim.x-center.x, dim.y-center.y, dim.width, dim.height)
  return rect


def dimensions_from_extents(ulx, uly, lrx, lry):
  '''
  Convert extents to a dimensions rect
  '''
  width = lrx - ulx
  height = lry - uly
  return gdk.Rectangle(ulx, uly, width, height)
  
  
"""
def dimensions_to_bounds(dim):
  '''
  Convert a dimensions rect to a bounds rect
  '''
  return gdk.Rectangle(dim.x - dim.width/2,
    dim.x - dim.height/2,
    dim.width,
    dim.height)

def bounds_to_dimensions(bounds):
  return gdk.Rectangle(bounds.x + bounds.width/2,
    bounds.x + bounds.height/2,
    bounds.width,
    bounds.height)
"""

# TODO rename to dimensions??
def coords_to_bounds(coords):
  '''
  Create a bounds rect from a coordinates.
  One pixel width and height
  '''
  return gdk.Rectangle(coords.x, coords.y, 1, 1)

 
def dimensions(left_x, left_y, width, height):
  '''
  Create a dimensions rectangle from args.
  '''
  return gdk.Rectangle(left_x, left_y, width, height)


def intersect(bounds1, bounds2):
  '''
  Return intersection of two dimensions.
  bounds1 is a gdk.Rectangle, use its intersect() method.
  '''
  intersection = bounds1.intersect(bounds2)
  # if no intersection, all zeros
  result = not ( intersection.x == 0 and intersection.y == 0 \
    and intersection.width == 0 and intersection .height == 0 )
  # print "Intersect", result, bounds1, bounds2
  return result
  
  
# @dump_return
def union(bounds1, bounds2):
  '''
  Return union of two dimensions.
  bounds1 is a gdk.Rectangle, use its union() method.
  '''
  result = bounds1.union(bounds2)
  return result


# vectors



def vector_from_points(start_point, end_point):
  '''
  Vector subtraction ?
  Return vector (x,y) from start_point to end_point.
  '''
  return gdk.Rectangle(end_point.x - start_point.x, 
    end_point.y - start_point.y,
    0,0)
    
@dump_return
def vector_orthogonal(vect, handedness):
  '''
  Return a vector orthogonal to given.
  Swap x, y and negate one.
  Note that there are many orthogonal vectors to a line, 
  this is the orthogonal from the origin.
  Note also that there are two handednesses: right and left handed.
  Handeness negative is left, postive is right.
  Alternative implementation is to use rotate by an angle, +-
  '''
  if handedness < 0: # left
    return gdk.Rectangle(vect.y, -vect.x, 0, 0)
  else :
    return gdk.Rectangle(-vect.y, vect.x, 0, 0)
 
 
def vector_multiply_scalar(vect, scalar):
  '''
  Multiply a vector by scalar in place.
  '''
  vect.x = vect.x * scalar
  vect.y = vect.y * scalar
  
def vector_add(vector1, vector2):
  '''
  Add vector2 to vector1 in place.
  '''
  vector1.x += vector2.x 
  vector1.y += vector2.y
    
    
def normalize_vector_to_vector(vector1, vector2):
  '''
  Normalize first vector to second.
  Assert both vectors have same origin (0,0)?
  Transform (rotate) second vector to x-axis.
  Return second vector with same transform.
  '''
  # Make transform to normalize and align vector2 with x-axis
  # !!! atan2(y,x)
  angle = math.atan2(vector2.y, vector2.x)  # radians [-pi, pi]
  # inverse the angle.  Cairo's sign for angle is opposite of conventional.
  rotate_transform = cairo.Matrix().init_rotate(-angle)
  # Not scaled, but if would transform.scale, the scale done before rotation
  # Transform exit_vector
  (x,y) = rotate_transform.transform_point(vector1.x, vector1.y)
  rect = gdk.Rectangle(x, y, 0, 0)
  # print "Angle", angle, "Vect1", vector1, "Vect2", vector2, "Normalized:", rect
  return rect


def rectangle_orthogonal(rect, point):
  '''
  Return unit vect orthogonal to a rect aligned with axises of coordinate system.
  '''
  if point.x >= rect.x + rect.width:
    vect = dimensions(1,0, 0,0)
  elif point.x <= rect.x :
    vect = dimensions(-1,0, 0,0)
  elif point.y >= rect.y + rect.height:
    vect = dimensions(0,1, 0,0)
  else:
    vect = dimensions(0,-1, 0,0)
  return vect


def any_dims():
  '''
  Return an arbitrary Dimensions instance.
  '''
  return gdk.Rectangle(10, 10, 20, 20)
