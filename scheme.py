#!/usr/bin/env python

'''
The scheme, containers of things to be drawn.

A singleton, one per application instance.

Not all ports draw all things.
'''
import composite
import morph.morph
import base.vector as vector
import config
import gui.boundingbox
import port

# Untransformed.
# Ephemeral GUI controls widgets
widgets = []

# FIXME comments wrong
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


# TODO do we need a separate initializer?
def initialize():
  global model
  global transformed_controls
  global bounding_box
  
  transformed_controls = composite.Composite()  # GUI widgets
  model = morph.morph.Morph() # group morph is root of modeling tree of user's objects
  
  # !!! Set the topmost transform to scale by PENSOOL.SCALE
  translation = vector.Vector(0.0, 0.0)
  scale = vector.Vector(config.PENSOOL_UNIT, config.PENSOOL_UNIT)
  model.set_transform(translation, scale, 0.0)
  
  bounding_box = gui.boundingbox.BoundingBox()
  
def zoom(direction, event):
  '''
  Zoom is an operation on the viewing transformation.
  Of the model.
  FIXME and of certain controls such as handles?
  '''
  ZOOM_RATE = 0.5
  if direction:
    model.zoom(ZOOM_RATE, event, port.view.user_context())
  else:
    model.zoom(1.0/ZOOM_RATE, event, port.view.user_context())
  # FIXME user preference constant for zoom speed
  # FIXME zoom handles?
  

