
import morph
import glyph
import textglyph
import gui.textselectcontrol
import textselectmanager
from decorators import *


class TextMorph(morph.PrimitiveMorph):
  '''
  Morph comprising frame, text, selection control.
  
  User can:
    pick and manipulate frame as representative of whole
    set font and size of text.
    enter keystrokes into the text.
    constrain: frame sides
    constrain: text clipping or auto frame expand
    
  Text does layout to fit the frame.
  set_dimensions of the frame should layout.
  
  For now, the frame is virtual (not a separate morph.)
  Use the standard grouping method to make a frameed text where frame is visible?
  
  It is a compound containing one primitive TextGlyph.
  (For reasons discussed elsewhere.)
  
  The primitive text glyph in turn comprises list of characters
  (called glyphs in Pango.)
  
  A TextMorph is not hashable because it is a Compound (a list.)
  The TextGlyph is hashable.
  '''


  def __init__(self, viewport):
    # morph.Morph.__init__(self, viewport)
    super(TextMorph, self).__init__(viewport)
    """
    Three members: 
      text, a glyph
      frame, a glyph
      text_select_control, a morph with its transform
    !!! Note however that textglyph overrides draw and futzes with scale.
    """
    self.frame = glyph.RectGlyph(viewport)  # TODO singleton?
    self.append(self.frame)
    
    # textglyph is an attribute so that we can tell it to activate its select.
    # I suppose we could use self[0]
    self.textglyph = textglyph.TextGlyph(viewport)
    self.append(self.textglyph)
    
    '''
    TextMorph has a selection but it is not a member of the composite.
    Hashed by the TextGlyph, not the TextMorph
    '''
    # The textglyph will save a reference to this selection control.
    self.text_select = gui.textselectcontrol.TextSelectControl(viewport, self.textglyph)
    self.append(self.text_select)
    
  """
  def set_dimensions(self, rect):
    '''
    TODO set the dimensions changes font size or just lays it out differently.
    '''
    raise RuntimeError("Can't yet set dimensions of text.")
  """  
    
  @dump_event
  def activate_controls(self, direction):
    '''
    This text has gained/lost pointer focus.  
    Activate/deactivate its text select for keyboard focus.
    '''
    textselectmanager.activate_select_for_text(direction, self.textglyph)
   
   
  def put_edge_to(self, context):
    '''
    !!! Override: Hit detection is just on frame, not text glyphs
    TODO hit detection on TextSelect control
    '''
    context.save()
    self.put_transform_to(context)
    self.frame.put_edge_to(context)
    context.restore()
  
  
    
  """
  # !!! Override
  @dump_event
  def draw(self, context):
    '''
    This is a composite, but the single member is a textglyph.
    Has a frame: virtual, optional member.
    Return the bounds of the frame,
    which surrounds everything else (text and selection.)
    '''
    # Draw the frame transformed.
    # !!! Scaling unit rectangle.
    self.put_transform_to(context)
    bounds = self.frame.draw(context)
    context.restore()
    
    # Draw my single text glyph.
    # Translate, but don't scale (Pango text unscaled.)
    # Set width to device CS width of frame
    context.save()
    # !!! Don't get the union dimensions, just the origin of this morph.
    # That is, the text is translated to the same place as the frame.
    dims = self.get_origin()
    context.translate(dims.x, dims.y)
    self[0].draw(context)
    context.restore()
    
    # Draw text select control
    # Translate, but scale to size of font, not size of morph
    # FIXME scale to size of font, draw unit rect for IB
    context.save()
    # Translate to frame origin
    dims = self.get_origin()
    context.translate(dims.x, dims.y)
    # Text select control knows its own translation within frame
    self.text_select.draw(context)
    context.restore()
    
    return bounds
    """
    
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
    
    
    
    
