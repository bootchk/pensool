#!/usr/bin/env python

import drawable
import glyph
import pango
from decorators import *
import base.vector




class TextGlyph(glyph.Glyph):
  """
  see GTK Reference Manual: pangocairo.CairoContext
  """
  
  # !!! Override with additional attribute: text
  def __init__(self, viewport):
    self.text = "Most relationships seem so transitory"
    # self.font = 
    drawable.Drawable.__init__(self, viewport) # super
    self.layout = None  # cache the layout
    
  
  """
  def _put_box_path_to(self, context):
    '''
    The box is NOT the same as the bounds since bounds are aligned with x-axis.
    '''
    # Assert the context is scaled for the box.
    context.rectangle(0,0,1,1)  # Unit rectangle at origin
  """
   
  # @dump_event
  def _put_text_path_to(self,  context):
    """ Put shape of text to context. """
    # self.font.put_to(context) # FIXME
    # With hierarchal modeling, glyph origin is (0,0).
    # Morph has transformed.  Note scale of text is (1,1)
    context.move_to(0, 0)
    # FIXME Don't layout each time, only when text changes.
    # Layout text to any new specifications
    self.layout = self._layout(context)
    # Put paths instead of text so path_extents will be right.
    context.layout_path(self.layout)
  
  
  def put_path_to(self, context):
    """ Put my shape to context. """
    self._put_text_path_to(context)
    
  
  def put_edge_to(self, context):
    # Should not call put_edge_to for text
    assert False
  
  
  def get_orthogonal(self, point):
    return self._aligned_rect_orthogonal(point)

   
  # @dump_event
  def _layout(self, context):
    '''
    Pango layout, for sophisticated text layout.
    Note pycairo context already supports pango
    '''
    # TODO persistent layout?
    layout = context.create_layout()
    layout.set_wrap(pango.WRAP_WORD)
    # FIXME
    # If user chose clipping to box
    # Get the width in device units
    dims = self.get_dimensions()
    # Scale to pangounits.
    # 200k with set_dims(scale=1) wraps into two sentences
    width = 200 * pango.SCALE
    layout.set_width( width )   # pangounits
    # 1 device unit = pango.SCALE pangounits
    layout.set_text(self.text)
    return layout
    
    
  @dump_return
  def insertion_position(self, context):
    '''
    Return user coords of insertion bar.
    
    FIXME for now, lower right corner
    '''
    
    ## rect = self.get_dimensions()  # get origin
    ##layout = self._layout(context)  # layout the text
    
    # If laid out already, use cached layout
    if self.layout:
      size = base.vector.Point(* self.layout.get_pixel_size())  # size in user coords
    else:
      size = base.vector.Point(0,0)
    return size + self.get_drawn_origin()

    ### print "IB cursor", layout.get_cursor_pos(15)
    
    
    
  """
  def get_bounding_box(self, context):
    layout = self._layout(context)
    x, y = layout.get_pixel_size()
    return
    
    context.cairo_select_font_face( "Purisa",
      CAIRO_FONT_SLANT_NORMAL,
      CAIRO_FONT_WEIGHT_BOLD)
    context.set_font_size(13)
  """
    
