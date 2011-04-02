'''
Item in a handle menu that creates morphs (draws) when user drags.
TODO name should be itemhandledraw.py
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
import morph.morph
import gui.manager.drop

from decorators import *
import config

import logging

my_logger = logging.getLogger("pensool")

class DrawHandleItem(itemhandle.HandleItem):
  '''
  A handle that stretches a morph from the controlee, when a drag starts within.
  Another control (bkgd mgr usually)
  gets involved when drag moves out of this item control.
  '''
  
  def __init__(self, command):
    itemhandle.HandleItem.__init__(self, command)
    # unfilled circle
    self.append(morph.glyph.CircleGlyph())
    self.scale_uniformly(config.ITEM_SIZE)
    self.symbol_type = "line" # mode: morph type to draw
  
  @dump_event
  def scroll_down(self, event):
    '''
    Cycle tool through kinds of glyphs user can drag out.
    '''
    if self.symbol_type == "line":
      self.symbol_type = "rect"
    else:
      self.symbol_type = "line"
    # print ">>>>>>>>>>>>Next line kind", self.symbol_type
   
  
  @dump_event
  def start_drag(self, event):
    '''
    Generically: Mouse departed item with button down.
    Start drag with source being controlee.
    
    Specifically: Create a symbol to stretch.
    '''
    itemhandle.HandleItem.start_drag(self, event)  # Super
    
    # Create
    my_logger.debug("Created morph")
    if self.symbol_type == "line":
      new_thing = morph.morph.LineMorph() 
    else:
      new_thing = morph.morph.RectMorph()
    
    self.controlee.insert(new_thing)  # Insert morph into controlee's group, or make group
    # Assert the object now has a parent group.
    # But if controlee is the model (top), controlee is not in that group, controlee IS the group.
    # Morph extends from my menu manager's hotpot to the event.
    new_thing.set_by_drag(self.group_manager.layout_spec.hotspot, event)
    # !!! The draggee is different from source morph set above via super.start_drag()
    gui.manager.drop.dropmgr.set_draggee(new_thing)  
    
    
  '''
  Note this control might not be active, drawn when this event comes.
  A line is being dragged, but the handle menu item is hidden already.
  '''
  #@dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost morph being dragged/stretched
    
    event, offset, increment are in device coord system
    '''
    thing = gui.manager.drop.dropmgr.get_draggee()
    thing.set_by_drag(self.group_manager.layout_spec.hotspot, event)
    
    
  @dump_event
  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    (Note that usually the background control is active now and called this method.)
    Leave the morph as last ghosted.
    '''
    # TODO more precisely, the point on the controlee
    # TODO anchor line end at drag begin
    '''
    Notes about wrapping up a drag:
    assert the gui.manager.drop reset itself.
    This control might not be reset from the dragging state (if the mouse never left this control.)
    If the mouse exited this control, the background control has been in charge of the drag.
    
    '''
    pass

