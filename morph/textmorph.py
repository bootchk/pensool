'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

import morph
import glyph
import textglyph
import gui.textselectcontrol
import gui.manager.textselect
from decorators import *
import scheme # bounding box

class TextMorph(morph.PrimitiveMorph):
  '''
  Morph comprising frame, text
  
  Text does layout to fit the frame.
  set_dimensions of the frame should layout.
  '''
  
  def __init__(self,  text):
    super(TextMorph, self).__init__()
    """
    Members: 
      text, a glyph
      frame, a glyph
    !!! Note however that textglyph overrides draw and futzes with scale.
    """
    self.frame = glyph.RectGlyph()  # TODO singleton?
    self.append(self.frame)
    
    # textglyph is an attribute so that we can tell it to activate its select.
    self.textglyph = textglyph.TextGlyph( text)
    self.append(self.textglyph)
  
  def set_text(self, text):
    self.textglyph.text = text
  
  @transforming
  def put_edge_to(self, context):
    '''
    !!! Override: Hit detection is just on frame, not text glyphs
    TODO hit detection on TextSelect control
    '''
    self.frame.put_edge_to(context)
  
  
class TextEditMorph(TextMorph):
  '''
  TextMorph with extra selection control.
  
  Extra member:
    text_select_control, a morph with its transform
    
  User can:
    pick and manipulate frame as representative of whole
    set font and size of text.
    enter keystrokes into the text.
    constrain: frame sides
    constrain: text clipping or auto frame expand
  
  The primitive text glyph in turn comprises list of characters
  (called glyphs in Pango.)
  
  A TextEditMorph is not hashable because it is a Compound (a list.)
  The TextGlyph is hashable.
  '''
  
  def __init__(self,  text):
    super(TextEditMorph, self).__init__( text)
  
    '''
    TextEditMorph has a selection, IS a transformed member of the composite.
    Hashed by the TextGlyph, not the TextEditMorph
    '''
    # The textglyph will save a reference to this selection control.
    self.text_select = gui.textselectcontrol.TextSelectControl( self.textglyph)
    self.append(self.text_select)
    
    
  @dump_event
  def rouse_feedback(self, direction):
    '''
    This text has gained/lost pointer focus.  
    Activate/deactivate its text select for keyboard focus.
    '''
    scheme.bounding_box.activate(direction, self.bounds.to_rect())
    gui.manager.textselect.activate_select_for_text(direction, self.textglyph)
   

    
    
