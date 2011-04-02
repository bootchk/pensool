'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

'''
Handle manager: ensure only one set of handles active.

HandleSet's are not in the model.
An active HandleSet is in the scheme and is drawn.
Generally Handle's draw on top of the morphs they handle.
However, it may be drawn invisibly !!!  
E.G. points may be hidden by lines they handle.
E.G. style of handles may be invisible.
A HandleSet is drawn and picked in the transform of its parent morph.
A HandleSet is not a child of parent morph !!!
'''
import config
from decorators import *

current_handle_set = None
current_morph = None


@dump_event
def rouse(handle_set, morph, direction):
  ''' Rouse handle set on (visually) morph. '''
  global current_handle_set, current_morph
  
  if direction:
    current_handle_set = handle_set
    current_morph = morph
    # FIXME put in scheme or append to morph and later remove
  else:
    current_handle_set = None
    current_morph = None

#@dump_return
def pick(point):
  ''' Pick any handle of the current handle set. '''
  picked = None
  if current_handle_set:
    context = config.viewport.user_context()
    context.set_matrix(current_morph.retained_transform)
    picked = current_handle_set.pick(context, point)
  if picked:
    picked.highlight(True)
  # TODO unhighlight at appropriate time
  return picked

    
def draw():
  ''' Draw current handle set. '''
  if current_handle_set:
    context = config.viewport.user_context()
    context.set_matrix(current_morph.retained_transform)
    return current_handle_set.draw(context)
  


