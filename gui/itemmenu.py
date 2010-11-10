#!/usr/bin/env python

import gui.itemcontrol
from gtk import gdk
from decorators import *


class MenuItem(gui.itemcontrol.ItemControl):
  '''
  A menu item control:
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
    # Depends on the side exited
    # Traditional, square menus
    bounds = self.get_bounds()
    if event.y < bounds.y:
      print "Exit above"
      self.group_manager.previous(event)
    elif event.y > bounds.y + bounds.height:
      print "Exit below"
      self.group_manager.next(event)
    elif event.x < bounds.x :
      print "Exit left"
      self.group_manager.close(event)
    elif event.x > bounds.x + bounds.width:
      print "Exit right"
      # TODO traditional cascading
      self.group_manager.close(event)
   
  # @dump_event
  def mouse_move(self, event):
    '''
    Pass: defines that: conventional menu items do not move.
    '''
    pass
    
    
class SquareMenuItem(MenuItem):

  def put_path_to(self, context):
    context.rectangle(self.dimensions)
