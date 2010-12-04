#!/usr/bin/env python

'''
LayoutSpec

For menu layout geometry.
For other composites?

A LayoutSpec does not necessarily describe the actual layout.
For example, vector may not be used, but hardcoded.
'''
import base.vector
import math
import cairo
from decorators import *

class LayoutSpec(object):

  def __init__(self, hotspot=None, benchmark=None, vector=None, opening_item=0):
    if hotspot:
      self.hotspot = base.vector.Point(hotspot.x, hotspot.y) # intersection point of vector and morph
    if benchmark:
      self.benchmark = base.vector.Point(benchmark.x, benchmark.y) # starting point of layout
    self.vector = vector  # axis
    self.opening_item = opening_item
    
  
def slide_layout_spec(spec, pixels_off_axis):
  '''
  Slide this layout spec orthogonally.
  
  This version doesn't limit sliding
  and doesn't follow a the controllee especially if is a curve.
  '''
  # Right handed unit vector orthogonal to menu's vector.
  vect = spec.vector.orthogonal(pixels_off_axis)
  # Scale by magnitude of pixels_off_axis
  vect = vect * abs(pixels_off_axis)
  # Offset prior benchmark
  spec.benchmark += vect
  # !!! Note hotspot is unchanged



def make_slide_transform(spec, pixels_off_axis):
  '''
  Make a transform matrix
  from vectors aligned with x axis
  to vectors aligned orthogonal to menu axis
  translated to hotspot.
  '''
  # Rotation in direction of slide
  # Right handed unit vector orthogonal to menu's vector.
  vect = spec.vector.orthogonal(pixels_off_axis)
  m1 = cairo.Matrix()
  m1.rotate(vect.angle())
  
  # Translation to prior hotspot
  m2 = cairo.Matrix()
  m2.translate(spec.hotspot.x, spec.hotspot.y)
  
  return m1 * m2


def find_new_hotspot(controlee, spec, pixels_off_axis):

  hit_pattern = (base.vector.Point(2,-2),
    base.vector.Point(2,-1),
    base.vector.Point(2,0),
    base.vector.Point(2,1),
    base.vector.Point(2,2))
  
  matrix = make_slide_transform(spec, pixels_off_axis)
  
  print "Old hotspot", spec.hotspot
  for point in hit_pattern:
    transformed_point = base.vector.Point(*matrix.transform_point(point.x, point.y))
    print "Transformed", transformed_point
    if controlee.is_inpath(transformed_point):
      return transformed_point
  return None


@dump_return
def benchmark_from_hotspot(axis, hotspot):
  '''
  Calculate benchmark from hotspot.
  Since opening on middle item, benchmark at first item is half length away.
  '''
  to_benchmark = axis.copy()
  to_benchmark *= 10  # scale by half length of menu - half width of item
  # Here menu is 3 items of 20 overlapping by 10 = 40 / 2 -10
  benchmark = base.vector.Point(hotspot.x, hotspot.y) + to_benchmark
  return benchmark
  
  
def slide_layout_spec_follow(controlee, spec, pixels_off_axis):
  '''
  Slide this layout spec orthogonally.
  
  This version limits sliding
  and follows controllee's curve.
  
  Algorithm: we know the cursor moved just a little.
  Brute force search a pattern in the direction of movement,
  looking for hits on the controllee.
  '''
  spot = find_new_hotspot(controlee, spec, pixels_off_axis)
  if spot:
    print "New hotspot ", spot
    spec.hotspot = spot
    # new hotspot engenders new axis, then benchmark
    spec.vector = controlee.get_orthogonal(spot)
    spec.benchmark = benchmark_from_hotspot(spec.vector, spot)
  # else don't slide
    

