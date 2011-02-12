#!/usr/bin/env python

'''
LayoutSpec

Specifications (parameters) for layout.
For menu layout.
For other composites?

Controls are transformed.
Scheme has a group of all controls not belonging to a graphical morph.
The transform of that group is the transform for top-level controls.
The transform only scales (according to user preference or degree of zoom?)

A menu is a group.
Thus the hierarchy of transforms for items is:
  scheme control group transform (scales)
  menu group transform (translates and rotates)
  item transform (scales a unit glyph)
 
A LayoutSpec does not necessarily describe the actual layout.
For example, layout() may ignore vector in LayoutSpec and instead use a hardcoded vector.

Coordinates: currently in DCS.
A menu is drawn in DCS effectively since controls drawn in their own context.
FIXME should be in GCS of glyph?
'''
import base.vector
import cairo
from decorators import *


class LayoutSpec(object):

  def __init__(self, hotspot=None, benchmark=None, vector=None, opening_item=0):
    if hotspot:
      self.hotspot = base.vector.Point(hotspot.x, hotspot.y) # intersection point of vector and morph
    if benchmark:
      self.benchmark = base.vector.Point(benchmark.x, benchmark.y) # starting point of layout
    self.vector = vector  # axis
    self.opening_item = opening_item  # index of item within menu sequence
    
  def __str__(self):
    return str(self.hotspot) + str(self.benchmark) + str(self.vector) + str(self.opening_item)
  
  
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
  rotated from vector aligned with x axis to vector aligned orthogonal to menu axis
  translated to hotspot.
  '''
  # Rotation in direction of slide
  # Right handed unit vector orthogonal to menu's vector.
  vect = spec.vector.orthogonal(pixels_off_axis)
  m1 = cairo.Matrix()
  m1.rotate(vect.angle())
  
  # Translation to prior hotspot.
  # Since hotspot is in DCS, this transform is in DCS
  m2 = cairo.Matrix()
  m2.translate(spec.hotspot.x, spec.hotspot.y)
  
  return m1 * m2


def find_new_hotspot(controlee, spec, pixels_off_axis):
  '''
  Find new hotspot (intersection of menu axis and glyph.)
  
  Returns
  '''

  # Hit pattern is a line of pixels orthogonal to x-axis at distance 2
  hit_pattern = (base.vector.Point(2,-2),
    base.vector.Point(2,-1),
    base.vector.Point(2,0),
    base.vector.Point(2,1),
    base.vector.Point(2,2))
  
  # Make transform of hit pattern to bring it into relation with menu
  matrix = make_slide_transform(spec, pixels_off_axis)
  
  # print "Old hotspot", spec.hotspot
  for point in hit_pattern:
    transformed_point = base.vector.Point(*matrix.transform_point(point.x, point.y))
    # transformed_point now in DCS
    # print "Transformed", transformed_point
    if controlee.in_path(transformed_point):
      return transformed_point
  return None


#@dump_return
def benchmark_from_hotspot(axis, hotspot):
  '''
  Calculate benchmark from hotspot.
  Since opening on middle item, benchmark at first item is half length away.
  '''
  to_benchmark = axis.copy()
  to_benchmark *= -10  # scale by half length of menu - half width of item
  # Here menu is 3 items of 20 overlapping by 10 = 40 / 2 -10
  benchmark = base.vector.Point(hotspot.x, hotspot.y) + to_benchmark
  return benchmark
  
  
def slide_layout_spec_follow(controlee, spec, pixels_off_axis):
  '''
  Slide this layout spec orthogonally.
  
  This limits sliding and follows controllee's curve.
  
  Algorithm: we know the cursor moved just a little.
  Brute force search a pattern in the direction of movement,
  looking for hits on the controllee.
  '''
  spot = find_new_hotspot(controlee, spec, pixels_off_axis)
  if spot:
    print "Hotspot old", spec.hotspot, " new ", spot
    spec.hotspot = spot
    # new hotspot engenders new axis, then benchmark
    spec.vector = controlee.get_orthogonal(spot)
    spec.benchmark = benchmark_from_hotspot(spec.vector, spot)
  # else don't slide
    

