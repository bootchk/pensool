#!/usr/bin/env python

'''
Text selection control (i.e. a selection)
A zero-length selection is an insertion bar.
Pensool only has selections in text.

This is an overlay (e.g. gray or transparent) over text that is selected.

A control: does not appear in renderings on ports other than view displays.

Receives key presses when parent text glyph is active operand.

!!! A control that can be controlled by another control, a handle menu.
'''

import gui.control
import gui.manager.textselect
from decorators import *
import base.vector as vector
import morph


class TextSelectControl(gui.control.GuiControl):
  
  def __init__(self, textglyph):
    '''
    '''
    gui.control.GuiControl.__init__(self)
    
    # selection in units of glyph (character) index
    self.start_index = 0
    self.end_index = 0
    # a selection has-a text morph, belongs to it
    self.text_glyph = textglyph
    # a manager maps text to its textselectcontrol etc.
    gui.manager.textselect.new_select(self, textglyph, 0)
    
    ## OLD scheme.transformed_controls.append(self) # put in drawing scheme
    # Note dimensions are defaults until drawn
    
    # Self is morph comprising a group of rect glyphs that cover lines of selected text.
    # Initially, self is a single rectangle for an insertion bar.
    self.append(morph.glyph.RectGlyph())
    
    # Self transforms the group of rect glyphs.
    # Initial scale of insertion bar is size of font.
    # Initial translation of insertion bar is end of text.
    self.position_selection()
    # print "Bounds of initial text select", self.bounds
  
  @dump_return
  def position_selection(self):
    '''
    Translate and scale the text selection.
    Self is morph transformer of IB.
    '''
    # Get position of IB relative to TextMorph origin.
    ## position = self.text_glyph.insertion_position()
    position = vector.Vector(0.1,0.1)
    self.translation = position
    # !!!  scale and translation is some fraction of the TextMorph unit?
    self.scale = vector.Vector(0.1,0.1)
    self.derive_transform() # !!! If change specs, derive
    ## return position
  
  
  #FIXME morph.put_path_to should suffice
  # and any changes to the text glyph should change the transform of the selection
  """
  
  @dump_event
  def put_path_to(self, context):
    '''
    Shape of this control.
    
    Note this is inside a text box, which might be transformed.
    The same transform applies here.
    That is, this is called when walking the hierarchical model.
    '''
    self.filled = True  # TODO filled?
    # TODO shape it to mask text
    # get coords from pango.x_for_index etc.
    # print "Selection dimensions", self.get_dimensions()
    
    # FIXME temporarily just set the origin
    # self.set_origin(position)
    position = self.text_glyph.insertion_position(context)
    # Translate within text box
    context.translate(position.x, position.y)
    # print self.get_dimensions(), context.get_matrix()
    
    # more generally, a rectangle with cutouts to fit a block of text
    # i.e. a group of rectangles
    # FIXME
    # For now, one rectangle
    ## context.rectangle(self.get_dimensions())
    self[0].put_path_to(context)
  """
    
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
  
  @view_altering  # key alters this control
  @dump_event
  def key(self, event):
    '''
    Filtered event from background manager's callback.
    
    Key pressed in active text select.
    Replace select with key in the text.
    Move the select to following the key in the text.
    '''
    # FIXME for now append to text glyph
    self.text_glyph.text += event.string
    
    # This control probably move and possibly resize.
    # FIXME
    
    # FIXME relayout changed text (with invalidation)
    


