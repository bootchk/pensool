
import morph
import glyph
import gui.textselectcontrol
import textselectmanager
from decorators import *


class TextMorph(morph.Morph):
  '''
  Morph comprising a box of text.
  User can:
    manipulate the box.
    set font and size of text.
    enter keystrokes into the text.
    constrain: box sides
    constrain: text clipping or auto box expand
    
  Text does layout to fit the box.
  
  For now, the box is virtual (not a separate morph.)
  Use the standard grouping method to make a boxed text where box is visible?
  
  It is a compound containing one primitive TextGlyph.
  (For reasons discussed elsewhere.)
  
  The primitive text glyph in turn comprises list of characters
  (called glyphs in Pango.)
  
  A TextMorph is not hashable because it is a Compound (a list.)
  The TextGlyph is hashable.
  '''


  def __init__(self, viewport):
    morph.Morph.__init__(self, viewport)
    # textglyph is an attribute so that we can tell it to activate its select.
    # I suppose we could use self[0]
    self.textglyph = glyph.TextGlyph(viewport)
    self.frame = glyph.RectGlyph(viewport)  # TODO singleton?
    self.append(self.textglyph)
    
    '''
    TextMorph has a selection but it is not a member of the composite.
    Hashed by the TextGlyph, not the TextMorph
    '''
    # The textglyph will save a reference to this selection control.
    # Here discard the reference to textglyph
    bar = gui.textselectcontrol.TextSelectControl(viewport, self.textglyph)
   
    
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
    if direction:
      textselectmanager.activate_select_for_text(self.textglyph)
    else:
      textselectmanager.deactivate_select_for_text()
   
   
  def put_edge_to(self, context):
    self.textglyph.put_edge_to(context)
  
  
  # !!! Override
  @dump_event
  def draw(self, context):
    '''
    This is a composite, but the single member is a textglyph.
    Has a frame: virtual, optional member
    '''
    # Draw the frame, transformed
    self.put_transform_to(context)
    self.frame.draw(context)
    context.restore()
    
    # Draw my single text glyph.
    # Translate, but don't scale.
    # Set width to device CS width of frame
    context.save()
    # !!! Don't get the union dimensions, just the origin of this morph.
    dims = self.get_origin()
    print dims
    context.translate(dims.x, dims.y)
    self[0].draw(context)
    context.restore()
    
    
    
    
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
    
    
    
    
