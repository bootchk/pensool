'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

'''
textselectmanager.py

Manager of text selection controls.

Many text selections can be displayed.
One-to-one with text glyphs.

Only one active: receiving keyboard events.
Generally, when the pointer is in a TextMorph.

Note distinction between TextMorph and TextGlyph
'''

from decorators import *



text_select = {}  # TextGlyph -> TextSelectControl
active_text_select = None


@dump_event
def activate_select_for_text(direction, text = None):
  '''
  '''
  global active_text_select
  if direction:
    try:
      active_text_select = text_select[text]
    except KeyError:
      print "Text glyph without a text select?"
  else:
    active_text_select = None
    
  
def get_active_select():
  '''
  '''
  return active_text_select


def new_select(control, text, index):
  '''
  Associate new selection control with text at position x.
  '''
  text_select[text] = control
