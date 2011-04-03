#!/usr/bin/env python
''' Geometry: orthogonality.'''
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''
"""
Orthogonality.

Uses vector algebra.  
Any point parameter must have .x and .y but need not be a vector.

Examples:

# Test setup
>>> point1 = vector.Vector(0,0)
>>> point2 = vector.Vector(2,2)
>>> point3 = vector.Vector(0,2)
>>> point4 = vector.Vector(2,0)
>>> rect = bounds.Bounds(0, 0, 1, 1)
>>> rect2 = bounds.Bounds(150, 30, 200, 200)

# Circle
>>> circle_orthogonal(point1, point2)
(0.707106781187,0.707106781187)

>>> circle_orthogonal(point1, point3)
(0.0,1.0)

# Line
>>> line_orthogonal(point1, point3)
(1.0,-0.0)

# Magnitude and distance
>>> magnitude_to_line(point1, point2, point3)
-1.4142135623730951

>>> magnitude_to_line(point1, point2, point4)
1.4142135623730951

# Rectangle
# On line of left side but outside and ortho to bottom side
>>> rect_orthogonal(rect, vector.Vector(0,2))
(0.0,1.0)

# Middle of left side, on the side
>>> rect_orthogonal(rect, vector.Vector(0, 0.5))
(-1.0,0.0)

# Middle of bottom side, on the side
>>> rect_orthogonal(rect, vector.Vector(0.5, 1))
(0.0,1.0)
>>> rect_orthogonal(rect2, vector.Vector(300, 230))
(0.0,1.0)

>>> rect_orthogonal(rect, vector.Vector(0.5, 0.51))
(0.0,1.0)

>>> rect_orthogonal(rect, vector.Vector(2, 0))
(1.0,0.0)

>>> rect_orthogonal(rect, vector.Vector(1, -1))
(0.0,-1.0)

>>> rect_orthogonal(rect, vector.Vector(1, -1))
(0.0,-1.0)
"""

# from gtk import gdk
import math
import base.vector as vector
import base.bounds as bounds
from decorators import *

def circle_orthogonal(center, point):
  '''
  Ortho of circle is: vector from center to point.
  The point can be inside or outside the circle.
  Orthogonal to the center is the (0,0) null vector, causes problem?
  '''
  point_vect = vector.Vector(point.x, point.y)
  orthog = point_vect - center
  return orthog.normal()


# FIXME third point?
def line_orthogonal(point1, point2):
  '''
  Canonical ortho of infinite line defined by two points.
  Canonical means not the orthogonal in the direction of a third point.
  '''
  vect = point2 - point1
  orthogonal = vect.orthogonal(-1)  # left handed
  return orthogonal.normal()
  
  

def magnitude_to_line(point1, point2, point3):
  '''
  Magnitude from point3 to line defined by point1 and point2.
  Magnitude is signed.
  Sign indicates left or right in direction from point1 to point2.
  '''
  norm = line_orthogonal(point1, point2)
  return point3.scalar_projection(norm)
  
  
def distance_to_line(point1, point2, point3):
  '''
  Distance from point3 to line defined by point1 and point2.
  Distance is always positive.
  '''
  norm = line_orthogonal(point1, point2)
  return abs(norm.dot(point3 - point1)/norm.length())


def rect_orthogonal(rect, point):
  '''
  Ortho of rect given a point is:
  outward pointing vector orthogonal to side nearest point.
  Point can be inside, outside, or on the rect.
  
  Implementation: four combinations of left and right of diagonals.
  That is, divide rect into quadrants by its two diagonals.
  Each quadrant has an orthogonal.
  '''
  point_vect = vector.Vector(point.x, point.y)
  corner = [x for x in rect]
  
  # translate points into coordinate systems of diagonals
  point1 = point_vect - corner[0]
  point2 = point_vect - corner[3]
  
  if magnitude_to_line(corner[0], corner[2], point1) < 0:
    # right of first diagonal
    if magnitude_to_line(corner[3], corner[1], point2) < 0 :
      # right of second diagonal
      # FIXME this is for aligned rect
      # return orthogonal to bottom side
      return vector.Vector(0,1)
    else:
      return vector.Vector(-1,0)
  else:
    if magnitude_to_line(corner[3], corner[1], point2) < 0 :
      return vector.Vector(1,0)
    else:
      return vector.Vector(0,-1)
  
"""
def rect_orthogonal(rect, point):
  '''
  Ortho of rect given a point is:
  outward pointing vector orthogonal to side nearest point.
  This is more general algorithm for rect rotated.
  This algorithm generalizes to convex polygons.
  !!! Only works for interior or on-the rect points.
  '''
  distance = 8888888
  nearest_side = None
  for side in rect.sides():
    point1, point2 = side
    a_distance = distance_to_line(point1, point2, point)
    if a_distance < distance:
      distance = a_distance
      nearest_side = side
  print nearest_side
  return line_orthogonal(*nearest_side)



Broken, poor design.  Works for interior points only.

def aligned_rect_orthogonal(rect, point):
  '''
  Unit orthogonal vector to a rectangle given a point,
  where the rect is aligned with axis.
  Ortho of side nearest the point.
  Where a point is equidistant from two sides,
  somewhat arbitrary choice of orthogonal.
  When rect is axis aligned, distance is simpler.
  '''
  # left side
  min_distance = abs(point.x - rect.value.x)
  orthogonal = vector.Vector(-1, 0)
  # right side
  distance = abs(point.x - rect.value.x + rect.value.width)
  if distance < min_distance:
    min_distance = distance
    orthogonal = vector.Vector(1, 0)
  # top side
  distance = abs(point.y - rect.value.y)
  if distance < min_distance:
    min_distance = distance
    orthogonal = vector.Vector(0, -1)
  # bottom side
  distance = abs(point.y - rect.value.y + rect.value.height)
  if distance < min_distance:
    min_distance = distance
    orthogonal = vector.Vector(0, 1)
  return orthogonal
"""

  
  
