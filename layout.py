#!/usr/bin/env python

'''
LayoutSpec

Base spec for calculating layout geometry.

A LayoutSpec does not necessarily describe the actual layout.
For example, vector may not be used, but hardcoded.
'''
import base.vector

class LayoutSpec(object):

  def __init__(self, hotspot=None, benchmark=None, vector=None):
    if hotspot:
      self.hotspot = base.vector.Point(hotspot.x, hotspot.y) # intersection point of vector and morph
    if benchmark:
      self.benchmark = base.vector.Point(benchmark.x, benchmark.y) # starting point of layout
    self.vector = vector  # axis
    
    


