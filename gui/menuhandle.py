#!/usr/bin/env python


'''
Handle subclass of menu.
See itemhandle.py for the handle subclass of menu item.
'''

import menu
import scheme
import base.vector
import layout
from decorators import *



class HandleGroup(menu.ItemGroup):
  '''
  Handle menu, layout is:
    moveable,
    layout reorients
    !!! only one item shown, as mouseovered
  '''
  
  def new_layout_spec(self, event):
    """
    New layout_spec for a handle menu.
    
    Event opens the menu, here the event is a hit on a morph edge.
    TODO abstract opening with moving.
    """
    assert self.controlee
    
    if self.controlee is scheme.glyphs:
      # Handle menu opened on background, controls the document
      axis = base.vector.downward_vector()
    else:
      # axis is orthogonal to controlee
      axis = self.controlee.get_orthogonal(event)
      
    benchmark = layout.benchmark_from_hotspot(axis, event)
    
    # FIXME hardcoded to open at 1, should be the middle of the menu
    self.layout_spec = layout.LayoutSpec(event, benchmark, axis, opening_item=1)
    
    """
    FIXME center on event, and open on middle item, benchmark away from hotspot
    # center menu on the edge of controlee
    # center is intersection of orthogonal and controlee edge
    ray tracing algorithm
    # benchmark: from center proceed half menu length in direction of orthogonal
    """
    
  @dump_event
  def layout(self, event=None):
    '''
    Layout (position) all items in group
    in a line orthogonal to the glyph
    in an order towards the center of the glyph
    (anti direction of orthogonal vector.)
    
    A handle group is laid out every time it slides.
    When exit an item, other items are already laid out.
    '''
    # Center first item on benchmark.  Ignore the event.
    ## OLD temp_rect = coordinates.dimensions(event.x, event.y, 0, 0)
    ### !!! This causes a seg fault temp_rect = copy.copy(self.layout_spec.benchmark)
    temp_rect = self.layout_spec.benchmark.copy()
    '''
    # get vector for direction of menu: orthogonal to the controlee eg glyph
    layout_vector = self.controlee.get_orthogonal(event)
    self.layout_spec.vector = layout_vector  # Remember it, items can ask for it
    '''
    layout_vector = self.layout_spec.vector.copy()
    
    # layout all items
    for item in self:
      item.center_at(temp_rect)
      ''' Dumbed down version
      # Layout next item leftward
      temp_rect.x -= item.dimensions.width/2
      '''
      # Multiply unit ortho vector by dimension vector; add/sub to previous coords
      # FIXME vector scale, translate
      temp_rect.x -= self.layout_spec.vector.x * item.get_dimensions().width/2
      temp_rect.y -= self.layout_spec.vector.y * item.get_dimensions().height/2
    print "returned from layout", self.layout_spec
      
      
      
   
  def draw(self, context):
    '''
    Draw only the current item.
    !!! Overrides group draw.
    '''
    self[self.active_index].draw(context)
 
