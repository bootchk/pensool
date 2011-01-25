#!/usr/bin/env python

import drawable
import glyph
import pango
from decorators import *
import base.vector
import base.orthogonal as orthogonal
import config
import cairo




class TextGlyph(glyph.Glyph):
  """
  see GTK Reference Manual: pangocairo.CairoContext
  """
  
  def __init__(self, viewport):
    '''
    !!! Override: extra attribute: text
    '''
    self.text = "Most relationships seem so transitory"
    # self.font = 
    drawable.Drawable.__init__(self, viewport) # super
    self.layout = None  # cache the layout
    
  
  @dump_return
  def draw(self, context):
    '''
    !!! Override: pango draws without scaling
    '''
    context.save()
    ## context.set_matrix( cairo.Matrix() )
    
    context.scale(1.0/self.parent.scale.x, 1.0/self.parent.scale.y)  # inverse parent scale
    # assert the context is already translated to the proper origin
    self.put_path_to(context)
    
    self.bounds = self.get_path_bounds(context)
    # !!! Outline fonts invisible at some scales
    context.fill()
    """
    if self.style.is_filled():
      context.fill()  # Filled, up to path
    else:
      context.stroke()  # Outline, with line width
    """
    # Assert fill or stroke clears paths from context
    context.restore()
    return self.bounds
  
    
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
    return orthogonal.rect_orthogonal(self.bounds.value, point)

   
  # @dump_event
  def _layout(self, context):
    '''
    Pango layout, for sophisticated text layout.
    Note pycairo context already supports pango
    '''
    ''' Layout seems to need a unit transform. '''
    ##context.save()
    ##context.set_matrix( cairo.Matrix() )
    
    # TODO persistent layout?
    layout = context.create_layout()
    
    '''Layout parameters: wrap, width, text, font, etc.'''
    layout.set_wrap(pango.WRAP_WORD)
    # FIXME
    # If user chose clipping to box
    
    ''' Set layout width in pangounits.
    1 device unit = pango.SCALE pangounits
    '''
    # Scale to pangounits.
    # 200k with set_dims(scale=1) wraps into two sentences
    width = 200 * pango.SCALE
    #print "matrix", context.get_matrix()
    # print "dims.width", dims.width, "layout width", width
    # FIXME, get parent scale to multiply pango.SCALE
    layout.set_width( width )   # pangounits
    
    layout.set_text(self.text)
    ##context.restore()
    return layout
    
    
  @dump_return
  def insertion_position(self):
    '''
    Return the offset of the selection.
    Offset in local coordinate system GCS of the textmorph.
    Used by the text_select_control to draw itself.
    
    OLD Return user coords of insertion bar.
    
    FIXME for now, lower right corner.
    More generally, the user can move it.
    '''
    ##layout = self._layout(context)
    
    # If laid out already, use cached layout
    if self.layout:
      size = base.vector.Point(* self.layout.get_pixel_size())  # size in user coords
    else:
      size = base.vector.Point(10,10)
    return size  # OLD + self.get_drawn_origin()

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
    
