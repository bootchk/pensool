#!/usr/bin/env python

'''
The scheme, container of things to be drawn.

A singleton, one per application instance.
'''
import compound
import gui.boundingbox

# Visible untransformed GUI control widgets
widgets = []

# Transformed GUI control widgets e.g. text selections
transformed_controls = []

# Singleton controls
# Ghosts, not controls, not morphs
# TODO this is being appended to transformed_c...
bounding_box = None

# Glyphs, the model  TODO Morphs
glyphs = None



viewport = None

def initialize(a_viewport):
  global glyphs, viewport, bounding_box
  glyphs = compound.Compound(a_viewport)
  viewport = a_viewport
  bounding_box = gui.boundingbox.BoundingBox(viewport)
  


