'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

Classic vertical, linear, static menu.
'''

import menu
from decorators import *
import layout
import base.vector as vector
import config

class MenuGroup(menu.ItemGroup):
  '''
  Traditional menu, layout is:
    fixed position (menu does not track cursor)
    static layout (items in same relation every open)
    vertical layout (items one above the other), 
    all items visible concurrently
  '''
  
  def new_layout_spec(self, event):
    '''
    Layout spec for traditional menu: 
      vector is downward (positive y ward)
      opening item is 0 (the topmost item)
      benchmark is at event (under the opening item.)
      FIXME benchmark is UL of first item
    '''
    ## menu_vect = vector.Vector(0, 1.0)
    menu_vect = vector.UNIT_X_AXIS.copy()
    # Translate menu group so opens with opening item centered on event
    # FIXME compute a proper offset to center the opening item
    benchmark = vector.Vector(event.x, event.y)
    benchmark += vector.Vector(-10, -10)
    self.layout_spec = layout.LayoutSpec(event, benchmark, menu_vect, opening_item=0)

    
  @dump_event
  def layout(self, event=None):
    '''
    Layout (position) all items in group.
    In linear, rectangular table, with non-overlapping items.
    Relative positioning within the parent GCS.
    Note that the menu group points the axis of the menu in a direction.
    Layout must be on a corresponding axis.
    
    Layout is along the y-axis by convention.
    
    Event is ignored, use coords of most recent event (open, slide, etc.).
    '''
    point = vector.ORIGIN.copy()
    for item in self:
      ## item.center_at(point)
      item.move_absolute(point)
      # Next item along a line (the x-axis).
      # FIXME more generally, get the size of an item
      # point.y += item.get_dimensions().height
      point.y += config.ITEM_SIZE # HEIGHT?
      
    """
    OLD using non-transformed layout
    # Center first item on benchmark.
    # (Which is the same as opening event?)
    temp_rect = self.layout_spec.benchmark.copy()
    for item in self:
      item.center_at(temp_rect)
      # Next item downward
      temp_rect.y += item.get_dimensions().height
    """
