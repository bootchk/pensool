'''
Items in handle menu. Items that move and resize controlee.
'''
'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

import itemhandle
from decorators import *
import gui.manager.focus
import gui.manager.drop
import morph.glyph
import base.alert
import config

import logging
my_logger = logging.getLogger('pensool')


class MoveHandleItem(itemhandle.HandleItem):
  '''
  A handle that moves the controlee, when a drag starts within.
  Another control is involved when a drag moves out of this item control.
  
  Scrolling descends/rises into controlee when it is composite.
  '''
  
  def __init__(self, command):
    itemhandle.HandleItem.__init__(self, command)
    # unfilled rect
    self.append(morph.glyph.RectGlyph())
    self.scale_uniformly(config.ITEM_SIZE)
  
  
  @dump_event
  def _change_controlee(self, new_controlee):
    '''
    If controlee is not none, change to it.
    None means at the top
    '''
    if new_controlee:
      gui.manager.focus.focus(new_controlee)
      self.controlee = new_controlee
    else:
      base.alert.alert("Can't scroll up past document.")
    
  @dump_event
  def scroll_down(self, event):
    '''
    Filtered event from GuiControl: scroll wheel down in a handle item.
    Make operand a child of composite that is at hotspot of handle menu
    to which this item belongs.
    '''
    print "Old controlee", self.controlee
    ## OLD if len(self.controlee) > 1:
    if self.controlee.is_top():
      config.scheme.zoom(False, event)
    if self.controlee.is_primitive():
      base.alert.alert("Can't scroll down past primitive morph")
    else:
      # Iterate children to find first at hotspot of handle menu.
      # TODO If more than one at hotspot?
      # Then cycle through siblings ie walk depth first
      for child in self.controlee:
        print "Child ....", repr(child)
        # TODO Too strict?  Allow jitter?
        if child.in_path(self.group_manager.layout_spec.hotspot):
          self._change_controlee(child)
          return
      # Assert one must be at this event, else we would not have opened menu.
      raise RuntimeError("No morph found for handle menu")

  
  @dump_event
  def scroll_up(self, event):
    '''
    Filtered event from GuiControl: scroll wheel UP in a handle item.
    Parent of this item's controlee becomes new controlee.
    '''
    if self.controlee.is_top():
      # FIXME hotspot of handle menu, not the event
      config.scheme.zoom(True, event)
    else:
      self._change_controlee(self.controlee.parent)
  
  
  # start_drag inherited
  
  #@dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost controlee being dragged
    '''
    # Display at new coords, same width and height
    # Since moving in real time, use the increment from previous continue
    thing = gui.manager.drop.dropmgr.get_draggee()
    if self.group_manager.handle: # if dragging a handle
      thing.move_by_drag_handle(offset, increment)
    else:
      thing.move_by_drag(offset, increment)
 

  @dump_event
  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    Leave the ghosted move in last position.
    '''
    my_logger.debug("Drop move of " + source.__class__.__name__)
    pass
    


  
class ResizeHandleItem(itemhandle.HandleItem):
  '''
  A handle that resizes the controlee, when a drag starts within.
    Another control is involved when drag exits this item control.
  
  Scrolling alters constraints on resize. TODO
  '''
  def __init__(self, command):
    itemhandle.HandleItem.__init__(self, command)
    # filled rect
    self.append(morph.glyph.RectGlyph())
    self.style.filled = True
    self.scale_uniformly(config.ITEM_SIZE)
  

  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    This control resizes source.
    '''
    source.resize(event, offset)

