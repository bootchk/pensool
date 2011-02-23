#!/usr/bin/env python



'''
FocusManager

Manages focus.
Focus includes:
  keyboard focus (receiving keyboard events)
  feedback ie highlighting
  activating controls associated with or part of operand
  
There is no selection, but there is focused (or current) operand.
Focused operand is a morph, not a control?
Drawables can be highlighted.
'''

from decorators import *

# Attribute private to module
_focused_operand = None
  
@dump_event
def focus(thing):
  '''
  Focus on an operand.
  '''
  global _focused_operand
  
  unfocus()
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
    _focused_operand.highlight(False)
    _focused_operand = None
      
    

