
import compound
import glyph
import gui.textselectcontrol
import textselectmanager
from decorators import *


class TextMorph(compound.Compound):
  '''
  Morph comprising a box of text.
  
  It is a compound containing one primitive TextGlyph.
  (For reasons discussed elsewhere.)
  
  The primitive text glyph in turn comprises list of characters
  (called glyphs in Pango.)
  
  A TextMorph is not hashable because it is a Compound (a list.)
  The TextGlyph is hashable.
  '''


  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)
    # textglyph is an attribute so that we can tell it to activate its select.
    # I suppose we could use self[0]
    self.textglyph = glyph.TextGlyph(viewport)
    self.append(self.textglyph)
    
    '''
    TextMorph has a selection but it is not a member of the compound.
    Hashed by the TextGlyph, not the TextMorph
    '''
    # The textglyph will save a reference to this selection control.
    # Here discard the reference to textglyph
    bar = gui.textselectcontrol.TextSelectControl(viewport, self.textglyph)
   
    
  """
  Since dimensions are a property, this is bypassed anyway.
  Possibly reclare dimensions property.
  
  def set_dimensions(self, rect):
    '''
    TODO set the dimensions changes font size or just lays it out differently.
    '''
    raise RuntimeError("Can't yet set dimensions of text.")
  """  
    
  @dump_event
  def activate_controls(self, event):
    '''
    This text has pointer focus.  Activate its text select for keyboard focus.
    '''
    textselectmanager.activate_select_for_text(self.textglyph)
