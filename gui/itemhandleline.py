#!/usr/bin/env python

'''
Item in a handle menu that creates line morphs.
'''

import itemhandle
# This handle creates a morph in the scheme and uses drag and drop
import morph.morph
import scheme
import gui.manager.drop

from decorators import *
from config import *

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
    self.scale_uniformly(ITEM_SIZE)
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
  
  """
  OLD
  def group_with_controlee(self, morph):
    '''
    Group morph with controlee.
    Controlee is in scheme, so no need to add line to scheme.
    If the controlee is a primitive morph, expand to group morph?
    '''
    if self.controlee.is_primitive():
      print "...............NOT grouping with primitive", repr(self.controlee)
      # FIXME for now, put in scheme
      # should be, create a new group containing primitive and self
      scheme.model.append(morph)
    else:
      print "...............Grouping with ", repr(self.controlee)
      self.controlee.append(line)
  """ 
  
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

