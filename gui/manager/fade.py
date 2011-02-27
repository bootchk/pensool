#!/usr/bin/env python

'''
Fade manager: handles persist for a short time after pointer moves away.
So user can grab handles that are remote from the edge
(for curve tangent lines and center handles.)
Fade has only one step, it is not a slow dissolve.
'''

import base.timer as timer
from decorators import *

faded_callback = None
fade_timer = timer.Timer()
TIME = 500


def register_callback(func):
  '''
  Register a function to callback upon timeout,
  when it is time to fade.
  '''
  global faded_callback
  faded_callback = func
  
def focus_lost():
  ''' Start timer for fading '''
  fade_timer.start(TIME, timeout_cb)
  
def focus_gained():
  ''' There is new focus, possibly on the same morph '''
  fade_timer.cancel()
  # immediately fade.  If same morph, focus must follow.
  faded_callback()
  
    
@dump_event
def timeout_cb():
  ''' Timer went off.  Fade now. '''
  faded_callback()
  return False # so timer stops
