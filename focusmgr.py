#!/usr/bin/env python



'''
FocusManager

Manages focus feedback ie highlighting.
There is no selection, but there is a current operand.
Current operand is a morph, not a control?
Drawables can be highlighted.
'''

# Attribute private to module
__current_operand = None
  
def feedback_focus(thing):
  '''
  
  '''
  global __current_operand
  
  feedback_focus_cancel()
  __current_operand = thing
  print "Focusing ******* ", repr(thing)
  thing.highlight(True)
  
  
def feedback_focus_cancel():
  global __current_operand
  
  if __current_operand:
    __current_operand.highlight(False)
    __current_operand = None
      
    

