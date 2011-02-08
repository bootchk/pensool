#!/usr/bin/env python

'''
To test:
python -m doctest -v test.py

# A Matrix copy.deepcopy() is the unit matrix
>>> foo = cairo.Matrix()
>>> foo.translate(2,3)
>>> print copy.deepcopy(foo)
cairo.Matrix(1, 0, 0, 1, 0, 0)

# Creating an image surface
>>> image = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)

# Creating a context on the surface
>>> context = cairo.Context(image)

# Line width defaults to 2.0
>>> context.get_line_width()
2.0

# !!!! Note the line width is transformed !!!!
# Make it smaller so unit lines will not be fat in subsequent tests
>>> context.set_line_width(0.0001)
>>> context.get_line_width()
0.0001

# No current point on a new context 
>>> context.has_current_point()
False

# Current point on a new context is 0,0
# !!! Note this seems to contradict has_current_point() is False
>>> context.get_current_point()
(0.0, 0.0)

# Draw line in context
>>> context.line_to(10, 20)

# Stroke extent of line drawn without a current point is empty rect
>>> context.stroke_extents()
(0.0, 0.0, 0.0, 0.0)

# Path extent of line
>>> context.path_extents()
(0.0, 0.0, 0.0, 0.0)

# Line drawn has extents
>>> context.move_to(0,0)
>>> context.line_to(10, 20)
>>> context.path_extents()
(0.0, 0.0, 10.0, 20.0)

# Clear path takes extents to zero
>>> context.new_path()
>>> context.path_extents()
(0.0, 0.0, 0.0, 0.0)

>>> context.scale(10, 10)
>>> context.get_matrix()
cairo.Matrix(10, 0, 0, 10, 0, 0)

# Unit line with small line width
>>> draw_unit_line(context)

# path extents
>>> context.path_extents()
(0.0, 0.0, 1.0, 0.0)

# !!! stroke extents are null because line_width too small
>>> context.stroke_extents()
(0.0, 0.0, 0.0, 0.0)

# Unit line with somewhat larger line width
>>> context.set_line_width(0.01)
>>> draw_unit_line(context)

# !!! stroke extents are not null
# !!! One pixel width and height < 1
>>> context.stroke_extents()
(0.0, -0.0050781250000000002, 1.0, 0.0050781250000000002)

>>> device_bounds(context)
(0, -1, 10, 2)

# !!! Transform after a path does not alter the extents of the path!!!

# Rotate 90 degrees clockwise of unit vector along x axis
>>> context.rotate(math.pi / 2.0)
>>> context.get_matrix()
cairo.Matrix(6.12303e-16, 10, -10, 6.12303e-16, 0, 0)

>>> draw_unit_line(context)

>>> context.path_extents()
(0.0, 0.0, 1.0, 6.1230317691118863e-17)

# DCS bounds are height ~10, width ~1 (line width spans pixel boundary)
>>> device_bounds(context)
(-1, -1, 2, 11)

# Unit vector along x axis has DCS stroke bounds
# 3 pixels tall
>>> context.identity_matrix()

>>> context.set_line_width(0.001)
>>> context.get_line_width()
0.001

>>> draw_unit_line(context)
>>> context.stroke_extents()
(0.0, 0.0, 0.0, 0.0)

>>> device_bounds(context)
(0, 0, 0, 0)

>>> context.scale(10,10)
>>> draw_unit_line(context)

>>> context.stroke_extents()
(0.0, -0.00039062500000000002, 1.0, 0.00039062500000000002)

>>> device_bounds(context)
(0, -1, 10, 2)

# Rotate 45 degrees clockwise of unit vector along x axis
# has DCS stroke bounds (0, 0, 10, 10) : 1 pixel along x, 10 pixels along y
>>> context.identity_matrix()
>>> context.rotate( math.pi / 4.0)
>>> context.scale(10,10)
>>> draw_unit_line(context)
>>> device_bounds(context)
(-4, -4, 15, 15)

# TODO when line_width is the default 2, then bounds are very fat
'''

import cairo
import copy
import math
import base.bounds as bounds

def device_bounds(context):
  ''' Return the device bounds of extents '''
  return bounds.Bounds().from_context_stroke(context)
  
def draw_unit_line(context):
  context.new_path()
  context.move_to(0,0)
  context.line_to(1, 0)
  
  
foo = cairo.Matrix()
foo.translate(2,3)
print foo
print copy.copy(foo)
print copy.deepcopy(foo)
print cairo.Matrix() * foo  # workaround

# output
# cairo.Matrix(1, 0, 0, 1, 2, 3)
# cairo.Matrix(1, 0, 0, 1, 0, 0)
# cairo.Matrix(1, 0, 0, 1, 0, 0)
# cairo.Matrix(1, 0, 0, 1, 2, 3)
