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
import base.vector as vector




def copy(dim):
  ''' Copy GDKRectangle.  TODO superfluous'''
  return gdk.Rectangle(dim.x, dim.y, dim.width, dim.height)


def round_rect(rect):
  '''
  Expand rect of postive floats to rect of ints.
  Most drawing math in floats.
  Round off to integral pixels.
  '''
  # LR ceiling to next pixel
  width = int(math.ceil(rect.width))
  height = int(math.ceil(rect.height))
  # UL floor to previous pixel
  x = int(rect.x)
  y = int(rect.y)
  return gdk.Rectangle(x, y, width, height)
  
  
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
  assert isinstance(ulx, int)
  width = lrx - ulx
  height = lry - uly
  return gdk.Rectangle(ulx, uly, width, height)


def dimensions_from_float_extents(ulx, uly, lrx, lry):
  '''
  Convert extents to a dimensions rect
  '''
  assert isinstance(ulx, float)
  width = math.ceil(lrx - ulx)
  height = math.ceil(lry - uly)
  # Rectangle() will convert to ints
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
  One pixel width and height.
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

def normalize_vector_to_vector(vector1, vector2):
  '''
  Normalize first vector to second.
  Assert both vectors have same origin (0,0)?
  Transform (rotate) second vector to x-axis.
  Return second vector with same transform.
  '''
  # Make transform to normalize and align vector2 with x-axis
  angle = vector2.angle()
  # inverse the angle.  Cairo's sign for angle is opposite of conventional.
  rotate_transform = cairo.Matrix().init_rotate(-angle)
  # Not scaled, but if would transform.scale, the scale done before rotation
  # Transform exit_vector
  (x,y) = rotate_transform.transform_point(vector1.x, vector1.y)
  rect = gdk.Rectangle(x, y, 0, 0)
  # print "Angle", angle, "Vect1", vector1, "Vect2", vector2, "Normalized:", rect
  return rect
  
  
'''
Orthogonal vectors
'''

def rectangle_orthogonal(rect, point):
  '''
  Return unit vect orthogonal to a rect from a point.
  The rect must be aligned with axises of coordinate system.
  '''
  if point.x >= rect.x + rect.width:
    vect = vector.Vector(1,0)
  elif point.x <= rect.x :
    vect = vector.Vector(-1,0)
  elif point.y >= rect.y + rect.height:
    vect = vector.Vector(0,1)
  else:
    vect = vector.Vector(0,-1)
  return vect

@dump_return
def line_orthogonal(rect, point):
  '''
  Return unit vect orthogonal to line from point.
  Where line is diagonal of rect.
  '''
  # vector diagonal of rectangle
  vect = vector.Vector(rect.width, rect.height)
  orthogonal = vect.orthogonal(-1)  # left handed
  return orthogonal.unitize()
  
  

'''
Various constant objects.
'''

def any_dims():
  '''
  Return an arbitrary Dimensions instance.
  '''
  return gdk.Rectangle(10, 10, 20, 20)
  
  

  
  
