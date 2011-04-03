'''
Coordinates drag and drop, which crosses controls.

!!! Note that all event coords are in the device coord system.

TODO not a class, just a singleton module
'''
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

import base.vector as vector
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
    self.start_point = None
    self.current_point = None
    self.source = None  # which morph drag started from
    self.source_control = None # which control on the source
    self.draggee = None # which morp is being dragged
    # source not necessarily equal draggee, but often does.
    # For example, when dragging out a new morph from source morph


  @dump_event
  def begin(self, event, controlee, control):
    '''
    Enter dragging state.
    Remember event and source controlee and control.
    
    !!! Event already in user coords.
    '''
    assert(controlee is not None)
    assert(self.source is None)   # Not begin before
    self.start_point = vector.Vector(event.x, event.y)
    self.current_point = self.start_point.copy()
    self.source = controlee
    self.draggee = controlee # Defaults to same as source
    self.source_control = control
    
  
  #@dump_event
  def continued(self, event, target):
    '''
    Some control received mouse motion while is_drag.
    Tell source (EG to ghost its action.)
    '''
    self.source_control.continue_drag(event, 
      self._get_offset(event),
      self._get_increment(event))
    self.current_point = vector.Vector(event.x, event.y)

    
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
    offset = vector.Vector(event.x, event.y)
    offset -= self.start_point
    return offset
  
  def _get_increment(self, event):
    # Calculate incremental offset previous event to this event
    offset = vector.Vector(event.x, event.y)
    offset -= self.current_point
    return offset
  
# Singleton
dropmgr = DropManager()
