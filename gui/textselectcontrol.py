#!/usr/bin/env python

'''
Text selection control (i.e. a selection)
A zero-length selection is an insertion bar.
Pensool only has selections in text.

This is an overlay (e.g. gray or transparent) over text that is selected.

A control because it does not appear in renderings other than GUI displays.

Receives key presses when parent text glyph is active operand.

!!! A control that can be controlled by another control, a handle menu.
'''

import gui.control
import textselectmanager  # Manages set of text selection controls.
import scheme
from gtk import gdk


class TextSelectControl(gui.control.GuiControl):
  
  def __init__(self, viewport, textglyph):
    '''
    '''
    gui.control.GuiControl.__init__(self, viewport)
    
    # selection in units of glyph (character) index
    self.start_index = 0
    self.end_index = 0
    # a selection has-a text morph, belongs to it
    self.text_glyph = textglyph
    # a manager maps text to its textselectcontrol etc.
    textselectmanager.new_select(self, textglyph, 0)
    # put in drawing scheme
    scheme.transformed_controls.append(self)
    # Note dimensions are defaults until drawn
  
  
  def put_path_to(self, context):
    '''
    Shape of this control.
    '''
    self.filled = True  # TODO filled?
    # TODO shape it to mask text
    # get coords from pango.x_for_index etc.
    # print "Selection dimensions", self.dimensions
    
    # FIXME temporarily just set the origin
    self.set_origin(self.text_glyph.insertion_position(context))
    
    context.rectangle(self.dimensions)
    
    
  """
  def attach_to(self, text, context):
    '''
    Position self at end of text.
    More generally, after glyph x.
    Sized to fit the font.
    '''
    rect = text.insertion_position(context)
    rect.width = 10
    rect.height = 10
    self.set_dimensions(rect)
  """ 
  
  
  def key(self, event):
    '''
    Key pressed in a text select.
    Replace select with key.
    '''
    # This control will move (and possibly resize).
    # Queue redraw at current.
    self.invalidate()
    # Queue redraw changed text
    self.text_glyph.invalidate()
    
    keystring = event.string
    # FIXME for now append to text glyph
    self.text_glyph.text += keystring
    
    
    
    
  # TODO key events
