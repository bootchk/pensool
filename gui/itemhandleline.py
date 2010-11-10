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

class LineHandleItem(itemhandle.HandleItem):
  '''
  A handle that stretches a line from the controlee, when a drag starts within.
  Another control (bkgd mgr usually)
  gets involved when drag moves out of this item control.
  
  '''
  def put_path_to(self, context):
    '''
    Shape of this handle.
    '''
    self.filled = True
    context.rectangle(self.dimensions)
  
  
  @dump_event
  def scroll_down(self, event):
    '''
    Cycle tool through line kinds.
    '''
    # TODO
    print ">>>>>>>>>>>>Next line kind"
    pass
  
  
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
    
    # line is initially zero length at user_coords
    # TODO at the hot spot of the handle menu
    user_coords = self.viewport.device_to_user(event.x, event.y)
    dimensions = coordinates.dimensions(user_coords.x, user_coords.y, 0, 0)
    line.set_dimensions(dimensions)
    
    dropmanager.dropmgr.set_draggee(line)  # Remember line morph being dragged
    
    # Group morph with controlee.
    # Controlee is in scheme, so no need to add line to scheme.
    print "...............Grouping with ", repr(self.controlee)
    self.controlee.append(line)
    
    # No need to invalidate yet, size is zero
    
    
  @dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost line being stretched
    
    event, offset, increment are in device coord system
    '''
    # TODO look for suitable target
    user_coords = self.viewport.device_to_user(event.x, event.y)
    user_distance = self.viewport.device_to_user_distance(offset.x, offset.y)
    dimensions = coordinates.dimensions( 
      user_coords.x - user_distance.x, user_coords.y - user_distance.y, user_distance.x, user_distance.y)
    line = dropmanager.dropmgr.get_draggee()
    line.set_dimensions(dimensions)
    line.invalidate()
    
    
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

