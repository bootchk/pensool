#!/usr/bin/env python


'''
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
    '''
    ## was vector = None
    down_vect = vector.Vector(0, 1.0)
    self.layout_spec = layout.LayoutSpec(event, event, down_vect, opening_item=0)

    
  @dump_event
  def layout(self, event=None):
    '''
    Layout (position) all items in group.
    In linear, rectangular table, with non-overlapping items.
    Relative positioning within the parent GCS.
    Note that the menu group points the axis of the menu in a direction:
    layout is along the x-axis by convention.
    
    Event is ignored, use coords of most recent event (open, slide, etc.).
    '''
    point = vector.Point(0,0)
    for item in self:
      item.center_at(point)
      # Next item along a line (the x-axis).
      # FIXME more generally, get the size of an item
      # point.y += item.get_dimensions().height
      point.x += config.ITEM_SIZE # HEIGHT?
      
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
