#!/usr/bin/env python

import gui.control
from gtk import gdk
from decorators import *

import gui.manager.control




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

  # This is only special behaviour.
  # TODO why not use self.parent?
  def set_group_manager(self, manager):
    self.group_manager = manager

  # Temporary placeholders.  These should be implemented in subclasses.
  # Also, a button may have been pressed, exited the menu item, 
  # another handle menu created, then released.
  # That may not be handled correctly.
  # FIXME
  def button_release_left(self, event):
    self.group_manager.close(event)
    gui.manager.control.control_manager.activate_root_control()
    print "Item clicked without an action"
  
  def button_release_right(self, event):
    self.group_manager.close(event)
    gui.manager.control.control_manager.activate_root_control()
    print "Item clicked without an action"
  
  def close_manager(self):
    '''
    Close my manager and relinquish control.
    '''
    self.group_manager.close()
    gui.manager.control.control_manager.activate_root_control()

    
  #FIXME are these in guicontrol 
  # @virtual
  @dump_event
  def start_drag(self, event):
    '''
    This could happen if user only wants to drag a little bit,
    and the item bounds are bigger than the bounds of the 
    drag start constraint.
    '''

 
class CommandItemControl(ItemControl):
  '''
  An item that executes a command.
  '''
  def __init__(self, command):
    '''
    Has a command, could be NULL_COMMAND.
    
    After the command is executed,
    usually the parent menu (item group) is finished,
    but the higher menu may remain (if a cascading menu)
    or be restarted.
    '''
    super(ItemControl, self).__init__()
    self.command = command
    
  # TODO the button behaviour should be defined here instead of in subclasses
    
 
class PopupItemControl(ItemControl):
  '''
  An item that popups a menu.
  '''
  def __init__(self, menu):
    '''
    Has a menu.
    
    After the command is executed,
    usually the parent menu (item group) is finished,
    but the higher menu may remain (if a cascading menu)
    or be restarted.
    '''
    super(ItemControl, self).__init__()
    self.menu = menu




