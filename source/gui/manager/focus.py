'''
FocusManager coordinates focus, including:

-  keyboard focus (receiving keyboard events)
-  feedback ie highlighting
-  activating controls associated with or part of operand
  
Pensool has no selection of morphs, but there is focused (or current) operand.
Focused operand is a morph, not a control?
Drawables can be highlighted.
'''
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''


import gui.manager.fade
from decorators import *

# Attribute private to module
_focused_operand = None
  
@dump_event
def focus(thing):
  ''' Focus on an operand. '''
  global _focused_operand
  
  ## OLD unfocus()
  # This cancels any fading and immediately unfocuses
  gui.manager.fade.focus_gained()
  if _focused_operand:
    _focused_operand.highlight(False)
  
  _focused_operand = thing
  thing.highlight(True)
  thing.rouse_feedback(True)
  
  
  
def unfocus():
  '''
  Unfocus operand.
  '''
  global _focused_operand
  
  if _focused_operand:
    # callees must invalidate
    ## temporarily leave feedback
    ## _focused_operand.rouse_feedback(False)
    # TODO is highlight part of feedback
    _focused_operand.highlight(False)
    ## _focused_operand = None
    
    # Fade (delay erase til later) feedback
    gui.manager.fade.register_callback(unfocus_feedback)
    gui.manager.fade.focus_lost()
    
def unfocus_feedback():
  global _focused_operand
  
  # Could be a race between unfocusing because there is a new focus
  # and a timer, so check for None
  if _focused_operand:
    _focused_operand.rouse_feedback(False)
    _focused_operand = None
    

