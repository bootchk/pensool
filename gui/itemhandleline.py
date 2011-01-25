#!/usr/bin/env python

'''
Item in a handle menu that creates line morphs.
'''

import itemhandle
import coordinates

# This handle creates a morph in the scheme and uses drag and drop
import morph.morph
import scheme
import dropmanager

from decorators import *
from config import *

class LineHandleItem(itemhandle.HandleItem):
  '''
  A handle that stretches a line from the controlee, when a drag starts within.
  Another control (bkgd mgr usually)
  gets involved when drag moves out of this item control.
  '''
  
  def __init__(self, port):
    itemhandle.HandleItem.__init__(self, port)
    self.append(morph.glyph.RectGlyph(port))
    self.scale_uniformly(ITEM_SIZE)
  
  @dump_event
  def scroll_down(self, event):
    '''
    Cycle tool through line kinds.
    '''
    # TODO
    print ">>>>>>>>>>>>Next line kind"
    pass
  
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
    
    Specifically: Create a line to stretch.
    '''
    itemhandle.HandleItem.start_drag(self, event)  # Super
    # TODO generically create any morph
    
    line = morph.morph.LineMorph(scheme.viewport) # Create
    line.set_by_drag(self.group_manager.layout_spec.hotspot, event, self.controlee)
    dropmanager.dropmgr.set_draggee(line)  # Remember line morph being dragged
    self.controlee.insert(line)  # Insert line into controlee's group
    
    
  @dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost line being stretched
    
    event, offset, increment are in device coord system
    '''
    # TODO look for suitable target
    line = dropmanager.dropmgr.get_draggee()
    line.set_by_drag(self.group_manager.layout_spec.hotspot, event, self.controlee)
    
    
  @dump_event
  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    Leave the line as last ghosted.
    '''
    # TODO more precisely, the point on the controlee
    # TODO anchor line end at drag begin
    '''
    Notes about wrapping up a drag:
    assert the dropmanager reset itself.
    This control might not be reset from the dragging state
    (if the mouse never left this control.)
    '''
    pass

