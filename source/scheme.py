'''
Container of things to be drawn (morphs and controls.)

A singleton, one per application instance.

Not all ports draw all things (only a viewport draws controls, usually.)
'''

'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''


import composite
import morph.morph
import base.vector as vector
import gui.boundingbox
import config


class Scheme(object):
  ''' Named struct of things to draw. '''

  def __init__(self):
    self.model = morph.morph.Morph()
    ''' root of modeling tree of user's objects'''
    
    self.bounding_box = gui.boundingbox.BoundingBox()
    ''' Singleton controls.  Ghosts, not directly controllable by user '''
    # TODO this is being appended to transformed_c...

    # TODO this is obsolete? and should be a morph?
    self.transformed_controls = composite.Composite() 
    ''' Semi-permanent GUI controls widgets e.g. text selections that are attached to transformed morphs, thus also need to be transformed.
    '''
    
    self.widgets = []
    ''' Untransformed. Ephemeral GUI controls widgets '''
    
    # TODO move this to transformer
    # !!! Set the topmost transform to scale by PENSOOL.SCALE
    translation = vector.Vector(0.0, 0.0)
    scale = vector.Vector(config.PENSOOL_UNIT, config.PENSOOL_UNIT)
    self.model.set_transform(translation, scale, 0.0)
    
    
  def zoom(self, direction, event):
    '''
    Zoom is op on viewing transformation, i.e. the top transformation.
    It zooms the model and other controls that might be visible.
    TODO the bounding box.
    Note that some morphs contain controls but those controls are transformed by their morph.
    FIXME and of certain controls such as handles?
    
    This encapsulates knowledge of what scheme objects need to be transformed, and also the knowledge of the step size.
    '''
    if direction:
      self.model.zoom(config.ZOOM_RATE, event, config.viewport.user_context())
    else:
      self.model.zoom(1.0/config.ZOOM_RATE, event, config.viewport.user_context())
    # FIXME zoom handles?
  

