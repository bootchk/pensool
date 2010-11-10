#!/usr/bin/env python

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
def activate_select_for_text(text):
  '''
  '''
  global active_text_select
  active_text_select = text_select[text]


def deactivate_select_for_text():
  '''
  '''
  global active_text_select
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
