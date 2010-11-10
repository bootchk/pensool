#!/usr/bin/env python

'''
dropmanager.py

!!! Note that all event coords are in the device coord system.

TODO not a class, just a singleton module
'''

import coordinates
from decorators import *



class DropManager(object):
  '''
  Manages drag and drop within the app.
  (Doesn't manage drag and drop between apps.)
  Similar to Carbon Drop Manager.
  
  Source: the control where drag started
  Target: the control where drag ended (dropped)
  Controlee: the drawable being dragged.
  
  Enforces: only one drag and drop operation at a time.
  
  For now, each object must implement drop() method.
  TODO query each object for acceptance of drop.
  '''
  
  def __init__(self):
    self.start_x = None
    self.start_y = None
    self.current_x = None
    self.current_y = None
    self.source = None
    self.source_control = None
    self.draggee = None


  @dump_event
  def begin(self, event, controlee, control):
    '''
    Enter dragging state.
    Remember event and source controlee and control.
    
    !!! Event already in user coords.
    '''
    assert(controlee is not None)
    assert(self.source is None)   # Not begin before
    self.start_x = event.x
    self.start_y = event.y
    self.current_x = event.x
    self.current_y = event.y
    self.source = controlee
    self.source_control = control
    
  
  @dump_event
  def continued(self, event, target):
    '''
    Some control received mouse motion while is_drag.
    Tell source (EG to ghost its action.)
    '''
    self.source_control.continue_drag(event, 
      self._get_offset(event),
      self._get_increment(event))
    self.current_x = event.x
    self.current_y = event.y

    
  @dump_event
  def end(self, target, event):
    '''
    On mouse button release after motion (that's the definition of drag.)
    Tell the target object that source object dropped on it.
    '''
    if self.source is None:
      raise RuntimeError("Drag end without source")
    '''
    Tell the target:
      what was dropped (source)
      where (event)
      why (source_control)
      how far (offset)
    '''
    target.drop(self.source, event, self._get_offset(event), self.source_control)
    self.__init__()
  
    
  @dump_event
  def cancel(self):
    '''
    Cancel drag.
    ??? When would this happen
    '''
    self.source = None
  
  def is_drag(self):
    return self.source is not None
    
  
  def set_draggee(self, draggee):
    self.draggee = draggee
  
  def get_draggee(self):
    return(self.draggee)
  
  
  def _get_offset(self, event):
    # Calculate offset drag end to drag begin
    offset = coordinates.coords_to_bounds(event)
    offset.x -= self.start_x
    offset.y -= self.start_y
    return offset
  
  def _get_increment(self, event):
    # Calculate incremental offset previous event to this event
    offset = coordinates.coords_to_bounds(event)
    offset.x -= self.current_x
    offset.y -= self.current_y
    return offset
  
# Singleton
dropmgr = DropManager()
