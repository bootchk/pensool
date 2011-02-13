#!/usr/bin/env python

'''
Composite drawables i.e. groups i.e. containers of drawables.

Subclasses are menus and morphs.
All composites are Transformers and Drawables.
All composites are pickable, even Controls. TODO
Menus are also Controls.
Morphs implement get_orthogonal, Menus don't.

Composites can contain other composites, or primitives (guicontrols or glyphs.)

Embodies:
   an op on composite is an iterated op on its members or elements.
   hiearchal modeling: drawing a composite transforms its members

Certain ops are iterated on members, e.g. highlight.
Certain ops are not iterated, but are ops on composite's transform, e.g. move.
For those, see transformer.py

The signature and documentation for each method
is the same as for methods on primitive members.
'''

# FIXME rename to composite

import transformer
import style
from decorators import *
import coordinates
import base.bounds as bounds



'''
It might be better not to inherit from list,
but to implement standard container API,
or to have-a container instead of be-a container.
'''



class Compound(list, transformer.Transformer):
  '''
  A container of Transformer:Drawables.
  
  Isolates hierarchy aspects:
  Compounds aggregate properties from their members.
  Compounds donate default properties to members.
  (Members inherit properties from parents.)
  
  !!! inherits from Drawable:
    in_path() 
    get_bounds()
  They call put_path_to() which comes here and it does the right thing.
  
  These ops are directly transformed for hierarchal modeling:
    draw()
    put_path_to()
  
  The invalidate operation is aggregate and transformed
  It invalidates the union region of members.
  However, invalidate may be cached.
  And invalidate may aggregate and be transformed via the recursion of put_path_to.
  So you don't see invalidate as a method of compound.
  '''
  
  def __init__(self, parent=None):
    # init just one of two supers?  Can't call list.__init__() ?
    # FIXME inconsistent use of super()
    transformer.Transformer.__init__(self)
    # self.stroke_width = 1       # TODO style
    self.style = style.Style()
    if parent:
      self.parent = None
    else:
      self.parent = parent
    
  
  def append(self, item):
    '''
    override list.append to keep parent of each list element
    That is, hierachal model tree is digraph with bidirectional links.
    '''
    item.parent = self
    list.append(self, item)
  
  
  def get_parent(self):
    return self.parent

  
  @transforming
  # @dump_return  # Uncomment to debug composite draw()
  def draw(self, context):
    '''
    Iterate draw contained objects.
    The drawing order is important.
    !!! Note we draw separately, not in one stroke.
    
    Note this is standard hierarchal modeling:
    apply my transform to the current transform matrix of the context (CTM).
    '''
    self.style.put_to(context)
    union_bounds = bounds.Bounds()  # null 
    for item in self:
      # !!! Each item is not necessarily in its own saved context.
      # !!! Be careful that one item does not mess the context for siblings.
      item_bounds = item.draw(context)  # walk tree
      union_bounds = union_bounds.union(item_bounds)
      # print "Matrix for item:", context.get_matrix()
    self.bounds = union_bounds
    # !!! Note empty composites return null bounds
    return self.bounds.copy() # TODO return union_bounds to save a copy
 
  
  # @dump_return
  @transforming
  def pick(self, context, point):
    '''
    Pick: return first member that hits point.
    Ultimately calls glyph.pick() but it returns glyph.parent, a morph.
    Note: not returning self if member picks,
    that is, we are picking primitive morphs, not glyphs.
    That is, we are picking the smallest morph at coords.
    Alternatively, we could return composite morphs (the largest pick.)
    '''
    morph = None
    for item in self:
      morph = item.pick(context, point)
      if morph:
        break
    return morph


  # @dump_event
  @transforming
  def put_path_to(self, context):
    '''
    Aggregate the paths of members.
    !!! Note paths accumulate in the context even through save/restore
    '''
    # TODO putting style not necessary if only color?  Color not affect path?
    self.style.put_to(context)
    for item in self:
      item.put_path_to(context)
      

  # @dump_event
  def layout(self, event=None):
    '''
    Layout members.
    Usually based on origin and/or dimensions of group.
    Often overridden.
    Defaults to all items have same dimensions as the group.
    That is sensible for morphs, which have one item in a group. 
    '''
    if len(self) > 1:
      raise RuntimeError("Must override layout method for composite.")
    else:
      # Layout the single item as the dimensions of this group.
      print "Layout single item morph with group dimensions.<<<<<<"
      self[0].set_dimensions(self.get_dimensions())
  
  
  # FIXME the dimensions of a compound are not useful
  # only the bounds???
  @dump_return
  def get_dimensions(self):
    '''
    !!! Overrides drawable.get_dimensions getter for the dimensions property.
    !!! Dimensions of a composite is the union over member items.
    '''
    # Calculate dimensions
    rect = coordinates.copy(self[0].get_dimensions())
    for item in self:
      # print item, item.dimensions
      rect = coordinates.union(rect, item.get_dimensions())
    # No need to store it in this composite, always recalculated.
    # self.dimensions = rect  # calls Drawable.set_dimensions()
    # TODO do the calculation once, during layout
    return rect
  
  
  @dump_event
  def highlight(self, direction):
    # TODO transform??
    if self.is_primitive():
      self.style.highlight(direction)
    else:
      for item in self:
        item.highlight(direction)
  
  
  def activate_controls(self, event):
    '''
    Activating controls is NOT aggregate, but only on the top level.
    I.E. Don't activate all the controls in a tree of morphs.
    '''
    print "Virtual activate controls"
   
   
   
   
