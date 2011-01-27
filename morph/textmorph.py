
import morph
import glyph
import textglyph
import gui.textselectcontrol
import textselectmanager
from decorators import *

class TextMorph(morph.PrimitiveMorph):
  '''
  Morph comprising frame, text
  
  Text does layout to fit the frame.
  set_dimensions of the frame should layout.
  '''
  
  def __init__(self, viewport):
    super(TextMorph, self).__init__(viewport)
    """
    Members: 
      text, a glyph
      frame, a glyph
    !!! Note however that textglyph overrides draw and futzes with scale.
    """
    self.frame = glyph.RectGlyph(viewport)  # TODO singleton?
    self.append(self.frame)
    
    # textglyph is an attribute so that we can tell it to activate its select.
    self.textglyph = textglyph.TextGlyph(viewport)
    self.append(self.textglyph)
  
  
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
  
  def __init__(self, viewport):
    super(TextEditMorph, self).__init__(viewport)
  
    '''
    TextEditMorph has a selection, IS a transformed member of the composite.
    Hashed by the TextGlyph, not the TextEditMorph
    '''
    # The textglyph will save a reference to this selection control.
    self.text_select = gui.textselectcontrol.TextSelectControl(viewport, self.textglyph)
    self.append(self.text_select)
    
    
  @dump_event
  def activate_controls(self, direction):
    '''
    This text has gained/lost pointer focus.  
    Activate/deactivate its text select for keyboard focus.
    '''
    textselectmanager.activate_select_for_text(direction, self.textglyph)
   
    
  '''
  def is_inpath(self, user_coords):
    """ Are coords in our path (usually edge)? """
    context = self.viewport.user_context()
    context.save()
    self.textglyph.put_edge_to(context)
    hit = context.in_stroke(user_coords.x, user_coords.y)
    context.restore()
    if hit:
      print "Hit text"
    return hit
  '''


"""
  def set_dimensions(self, rect):
    '''
    TODO set the dimensions changes font size or just lays it out differently.
    '''
    raise RuntimeError("Can't yet set dimensions of text.")
  """  
    
    
    
