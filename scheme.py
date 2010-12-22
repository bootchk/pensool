#!/usr/bin/env python

'''
The scheme, containers of things to be drawn.

A singleton, one per application instance.

Not all ports draw all things.
'''
import compound
import gui.boundingbox

# Untransformed.
# Ephemeral GUI controls widgets
widgets = []

# Transformed.
# The same tr
# Semi-permanent GUI controls widgets e.g. text selections
# that are attached to transformed morphs,
# thus also need to be transformed.
transformed_controls = None

# Model.  Transformed collection of morphs.
model = None

# Singleton controls
# Ghosts, not controls, not morphs
# TODO this is being appended to transformed_c...
bounding_box = None

viewport = None


# TODO do we need a separate initializer?
def initialize(a_viewport):
  global model
  global transformed_controls
  global viewport, bounding_box
  
  transformed_controls = compound.Compound(a_viewport)
  model = compound.Compound(a_viewport)
  
  viewport = a_viewport
  bounding_box = gui.boundingbox.BoundingBox(viewport)
  


