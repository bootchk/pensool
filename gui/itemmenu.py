#!/usr/bin/env python

import gui.itemcontrol
import morph.glyph
from gtk import gdk
from decorators import *
import config


class MenuItem(gui.itemcontrol.ItemControl):
  '''
  A classic menu item control:
    -appears anywhere (locatable)
    -fixed location after appears
    -doesn't dissappear on mouseexit
  
  For use in menus:
  
  Context menus:
  -click appearance
  -mouseout dissappearance
  -clickable
  -is managed
  '''
  
  '''
  Button releases choose the menu item.
  '''
  @dump_event
  def button_release_left(self, event):
    # TODO
    pass
  
  @dump_event
  def button_release_right(self, event):
    # TODO the item's action
    self.group_manager.close(event)
  
  @dump_event
  def start_drag(self, event):
    '''
    Filtered event from GuiControl.
    Overrides GuiControl.start_drag()
    This defines that can't drag an ordinary menu item.
    But GuiControl already changed drag state?
    cancel drag on mouse_exit?
    '''
    #TODO 
    gdk.beep()
    print "?????????????????Dragging a menu item"
    pass
  
  @dump_event
  def mouse_exit(self, event):
    '''
    Handler for filtered mouse_exit event.
    Tell my group manager which direction to go,
    depending on the side exited.
    For traditional, square menu items.
    '''
    # Note both bounds and event in DCS
    bounds = self.bounds.value
    if event.y < bounds.y:  # above
      self.group_manager.previous(event)
    elif event.y > bounds.y + bounds.height:  # below
      self.group_manager.next(event)
    elif event.x < bounds.x : # left
      self.group_manager.close(event)
    elif event.x > bounds.x + bounds.width: # right
      # TODO traditional cascading
      self.group_manager.close(event)
   
  # @dump_event
  def mouse_move(self, event):
    ''' Pass because classic menu items do not move i.e. track the pointer. '''
    pass
    
    
class SquareMenuItem(MenuItem):
  
  def __init__(self, port):
    MenuItem.__init__(self, port)
    self.append(morph.glyph.RectGlyph(port))
    # define my size
    self.scale_uniformly(config.ITEM_SIZE)
    ## , morph.morph.RectMorph
    ## ??? Doesn't work: super(SquareMenuItem, self).__init__(port)

  """
  def put_path_to(self, context):
    context.rectangle(self.get_dimensions())
  """
