'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

import gui.itemcontrol
import morph.glyph
import morph.textmorph
from gtk import gdk
from decorators import *
import config
import base.vector as vector


class MenuItem(gui.itemcontrol.CommandItemControl):
  '''
  A classic menu item control:
    -appears anywhere (locatable)
    -fixed location after appears
    -not necessarily dissappear on mouse_exit (only on menu close)
  
  For use in menus:
  
  Context menus:
  -click appearance
  -mouseout dissappearance
  -clickable
  -is managed
  '''
  
  '''
  Button release: choose menu item.
  '''
  @dump_event
  def button_release_left(self, event):
    # TODO
    pass
  
  @dump_event
  def button_release_right(self, event):
    ''' RMB Release: execute, close menu '''
    self.command(self.controlee, event)
    self.group_manager.close()
    gui.manager.control.control_manager.activate_root_control()
  
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
    Handler for filtered mouse_exit event from control.
    Tell my group manager what to do, depending on the side exited.
    For traditional, square menu items, oriented vertically!!!
    
    !!! Note that control.py may use a different method to determine exit.
    Specifically, it may use in_fill() which is slightly different from bounds
    (because of inked strokes.)
    So it is not an error to get here and still be in bounds.
    '''
    # Note both bounds and event in DCS
    if event.y < self.bounds.y:  # above
      self.group_manager.previous(event)
    elif event.y > self.bounds.y + self.bounds.height:  # below
      self.group_manager.next(event)
    elif event.x < self.bounds.x : # left
      # Traditionally exit left means close the menu
      self.close_manager()
    elif event.x > self.bounds.x + self.bounds.width: # right
      # For now, close menu. TODO traditional right cascading
      self.close_manager()
    else:
      # control.py determined pointer is outside fill.
      # If control.py
      # print "Exited item but not out of bounds."
      pass
   
  # @dump_event
  def mouse_move(self, event):
    ''' Pass because classic menu items do not move i.e. track the pointer. '''
    pass
    
    
class IconMenuItem(MenuItem):
  # For now a rect
  def __init__(self, command):
    super(MenuItem, self).__init__(command)
    
    self.append(morph.glyph.RectGlyph())
    self.relative_scale(config.ITEM_SIZE*2, config.ITEM_SIZE) # size


class TextMenuItem(MenuItem):
  
  def __init__(self, text, command):
    super(MenuItem, self).__init__(command)
    
    text_morph = morph.textmorph.TextMorph(text)
    self.append(text_morph)
    # !!! Must scale my morph the parent of the textglyph, not self
    text_morph.relative_scale(config.ITEM_SIZE*2, config.ITEM_SIZE) # size
    
  def __repr__(self):
    ''' For debugging, represent self by my text. '''
    return "TextMenuItem" + str(id(self)) + self[0].__repr__()
    

    
