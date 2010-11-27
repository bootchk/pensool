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
  # Activate any associated controls on the morph
  # e.g. for text morph activate text select control
  # TODO activate while inside
  # TODO deactivate see menu.close()
  thing.activate_controls(True)
  
  
def unfocus():
  '''
  Unfocus operand.
  '''
  global _focused_operand
  
  if _focused_operand:
    # callees must invalidate
    _focused_operand.activate_controls(False)
    _focused_operand.highlight(False)
    _focused_operand = None
      
    

