'''
Fade manager: persists handles for a short period after pointer moves away.
So user can grab handles that are remote from the edge
(for curve tangent lines and center handles.)
Fade has only one step, it is not a slow dissolve.
'''
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

import base.timer as timer
import  config
from decorators import *

faded_callback = None
fade_timer = timer.Timer()


def register_callback(func):
  '''
  Register a function to callback upon timeout,
  when it is time to fade.
  '''
  global faded_callback
  faded_callback = func
  
def focus_lost():
  ''' Start timer for fading '''
  fade_timer.start(config.GUI_FADE_TIME, timeout_cb)
  
def focus_gained():
  ''' 
  There is new focus, possibly on the same morph. 
  Does NOT assume focus is fading, i.e. a callback is registered.
  '''
  fade_timer.cancel()
  # immediately fade.  If same morph, caller must focus it again.
  if faded_callback:
    faded_callback()
  
    
@dump_event
def timeout_cb():
  ''' Timer went off.  Fade now. '''
  faded_callback()
  return False # so timer stops
