#!/usr/bin/env python

import gui.control
from gtk import gdk
from decorators import *




class ItemControl(gui.control.GuiControl):
  '''
  A control that is part of a group (an item in a group.)
  Usually a menu item.
  Knows its group manager.
  Cooperates with its group to define behavior.
  
  Default behavior (should be overridden):
    Clickable (button release)
    Draggable (button press)
    
  Sublasses MUST override:
     __init__ to define the contained glyph shape (an item is a morph)
      (NOT put_path_to(), which is done by the glyph)
     mouse_move to define behavior under mouse movement inside item
  
  Group behavior primarily is defined by mouse_exit().
  
  Inherits GuiControl.callbacks(), draw(), __init__
  '''
  
  def __init__(self, port, command):
    '''
    Every item has a command, could be NULL_COMMAND
    '''
    gui.control.GuiControl.__init__(self, port) # super
    self.command = command
    
  def set_group_manager(self, manager):
    self.group_manager = manager

  def button_release_left(self, event):
    self.group_manager.close(event)
    print "Item clicked without an action"
  
  def button_release_right(self, event):
    self.group_manager.close(event)
    print "Item clicked without an action"
  
  #FIXME are these in guicontrol 
  # @virtual
  @dump_event
  def start_drag(self, event):
    '''
    This could happen if user only wants to drag a little bit,
    and the item bounds are bigger than the bounds of the 
    drag start constraint.
    '''

  



