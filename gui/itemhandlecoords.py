#!/usr/bin/env python

'''
Items in a handle menu.
These items move and resize the controlee.
'''

import itemhandle
import coordinates
from decorators import *
from config import *
import focusmgr
import morph.glyph
import base.alert


class MoveHandleItem(itemhandle.HandleItem):
  '''
  A handle that moves the controlee, when a drag starts within.
  Another control is involved when a drag moves out of this item control.
  
  Scrolling descends/rises into controlee when it is composite(compound.)
  '''
  
  def __init__(self, command):
    itemhandle.HandleItem.__init__(self, command)
    self.append(morph.glyph.RectGlyph())
    self.scale_uniformly(ITEM_SIZE)
  
  
  @dump_event
  def _change_controlee(self, new_controlee):
    '''
    If controlee is not none, change to it.
    None means at the top
    '''
    if new_controlee:
      focusmgr.focus(new_controlee)
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
    if len(self.controlee) > 1:
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
    else:
    ## OLD except TypeError: # if not iterable
      base.alert.alert("Can't scroll past primitive morph")
  
  
  @dump_event
  def scroll_up(self, event):
    '''
    Filtered event from GuiControl: scroll wheel UP in a handle item.
    Parent of this item's controlee becomes new controlee.
    '''
    self._change_controlee(self.controlee.parent)
  
  
  # start_drag inherited
  
  @dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost controlee being dragged
    '''
    # Display at new coords, same width and height
    # Since moving in real time, use the increment from previous continue
    thing = dropmanager.dropmgr.get_draggee()
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
    pass
    


  
class ResizeHandleItem(itemhandle.HandleItem):
  '''
  A handle that resizes the controlee, when a drag starts within.
    Another control is involved when drag exits this item control.
  
  Scrolling alters constraints on resize. TODO
  '''
  def __init__(self, command):
    itemhandle.HandleItem.__init__(self, command)
    self.append(morph.glyph.CircleGlyph())
    self.scale_uniformly(ITEM_SIZE)
  
  """
  def put_path_to(self, context):
    centerx, centery, radius = coordinates.circle_from_dimensions(self.get_dimensions())
    context.arc(centerx, centery, radius, 0, 2.0*math.pi)
  """

  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    This control resizes source.
    '''
    source.resize(event, offset)

