#!/usr/bin/env python

'''
Pointer manager: state machine for pointer movement.
The pointer must remain within a few pixels
for a short time
before mouseover (picking) is done.

Alternatively, we could pick at every mouse move, and delay the result
of the pick until it was confirmed a short time later.
But that requires efficient picking so as not to be jerky.

Here we use the mouse speed in pixel distance per second (?).
Using absolute mouse move distances is subject to jitter
and system busy problems.

We might be able to reconstruct a more accurate mouse position (float)
by averaging with previous mouse position.
The drawing library is in floating point, why not use mouse position in float?

!!! Note that the callback is asynchronous.
In general, it must be prepared for a race condition.
For example, the user may have just opened a menu using for example a control key,
and the callback must not interfere.

To test: python -m doctest -v gui/manager/pointer.py

Examples:
  
  # Normal sequence
  >>> import collections
  >>> import time
  >>> Event = collections.namedtuple('Event', 'x y time')
  >>> foo = Event(1,1, 1)
  >>> bar = Event(1,1, 5)
  >>> register_callback(dummy_callback)
  >>> decide_stopped(foo)
  >>> decide_stopped(bar)
  >>> time.sleep(2)
  
  # How to get a callback?
  
'''

import base.vector as vector
import base.timer as timer
import config
from decorators import *
import collections

Event = collections.namedtuple('Event', 'x y time')

# global state
state = None
previous_event = None

pointer_timer = timer.Timer()
stopped_callback = None


# For testing
def dummy_callback():
  print "Callback called."
  
  
def register_callback(func):
  '''
  Register a function to callback when pointer is stopped.
  Typically a pick for mouseover.
  '''
  global stopped_callback
  stopped_callback = func


def reset():
  ''' Reset to initial, null state. '''
  global state, previous_event
  
  state = None
  previous_event = None
  
  
def cancel_timer():
  ''' 
  Cancel my timer. Usually means pointer manager is not being used.
  See below: decide_stopped() may later be called and can restart timer.
  '''
  pointer_timer.cancel()


# @dump_return
def decide_stopped(event):
  '''
  Decide whether pointer is more or less stationary,
  given pointer movement event.
  A state machine.
  '''
  global state, previous_event, pointer_timer
  
  # Copy the event.  event.copy() does not seem to work.
  event_copy = Event(event.x, event.y, event.time)
  
  if state is None: # First motion after a reset
    state = "moving"
    # !!! a copy.  Seems like gtk might be deallocating the original?
    previous_event = event_copy 
    return
  
  assert previous_event is not None
  move = vector.Vector(event.x, event.y)
  previous_point = vector.Vector(previous_event.x, previous_event.y)
  motion_vector = move - previous_point
  distance = motion_vector.length()
  elapsed = event.time - previous_event.time
  
  previous_event = event_copy
    
  if elapsed <= 0:
    # event.time rolled over, wait for another mouse move.
    # Or, mouse moving so fast the event.time is the same,
    # avoid division by zero.
    return  
  speed = distance/elapsed
  # print distance, elapsed, speed
  
  if state is "moving":
    if speed <= config.GUI_MOVING_SLOWING_THRESHOLD:
      state = "slowed"
      pointer_timer.start(config.GUI_MOVING_POPUP_TIME, timeout_cb) # after a delay, go to stopped state
    # else moved fast
  elif state is "slowed":
    if speed > config.GUI_MOVING_SLOWING_THRESHOLD:
      state = "moving"
      pointer_timer.cancel()
    # else same state  still slow motion
  elif state is "stopped":
    if speed <= config.GUI_MOVING_SLOWING_THRESHOLD:
      # slow motion from stopped, try pick if user is making small adjustment
      # if it is acceleration, hope nothing to pick
      if stopped_callback(move):
        state = None
      # else, probably acceleration but don't change state
    else: # fast motion again
      state = "moving"
  else:  # Null state, the starting state.
    state = "moving"
  return state

    
# @dump_event
def timeout_cb():
  '''
  Timer went off.
  Enter stopped state and attempt a pick
  '''
  global state, pointer_timer
  
  if not pointer_timer.was_canceled():  # Avoid race
    if state is "slowed" or state is "stopped":
      state = "stopped"
      # callback now, if pointer is not moving won't be move events
      if stopped_callback(previous_event):
        # Return False so timer quits.  Otherwise it continues.
        return False
      else:
        # pick failed, let timer run in stopped state to keep trying
        return True
  

