#!/usr/bin/env python

'''
Composite drawables i.e. groups i.e. containers of drawables.

Subclasses are menus and morphs.

Composites can contain other composites, or primitives (guicontrols or glyphs.)

Embodies:
   an op on composite is an iterated op on its members or elements.
   hiearchal modeling: drawing a composite transforms its members

Certain ops are iterated on members, e.g. highlight.
Certain ops are not iterated, but are ops on composite's transform, e.g. move.
For those, see transformer.py

The signature and documentation for each method
is the same as for methods on the members.
'''

# FIXME rename to composite

import transformer
from decorators import *
import coordinates
import layout
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
    is_inpath() 
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
  
  def __init__(self, viewport):
    transformer.Transformer.__init__(self, viewport)
    self.viewport = viewport
    # self.stroke_width = 1       # TODO style
    self.layout_spec = layout.LayoutSpec() # TODO only menu uses this, move it there
    
  
  def append(self, item):
    '''
    override list.append to keep parent of each list element
    That is, hierachal model tree is digraph with bidirectional links.
    '''
    item.parent = self
    list.append(self, item)
  
  
  def get_parent(self):
    return self.parent

  
  @dump_return
  def draw(self, context):
    '''
    Iterate draw contained objects.
    The drawing order is important.
    !!! Note we draw separately, not in one stroke.
    
    Note this is standard hierarchal modeling:
    apply my transform to the current transform matrix of the context (CTM).
    '''
    # !!! context saved by caller but restored here
    self.put_transform_to(context)
    self.style.put_to(context)
    union_bounds = None
    for item in self:
      item_bounds = item.draw(context)
      if union_bounds is None:
        union_bounds = item_bounds
      else:
        union_bounds.union(item_bounds)
      # print "Matrix for item:", context.get_matrix()
    context.restore()
    self.bounds = union_bounds
    return self.bounds
 
  
  def put_path_to(self, context):
    '''
    Aggregate the paths of members.
    '''
    self.put_transform_to(context)
    self.style.put_to(context)
    for item in self:
      item.put_path_to(context)
    context.restore()
      

  @dump_event
  def get_orthogonal(self, point):
    '''
    Get orthogonal of a composite.
    
    FIXME now makes no sense for composite controls.
    '''
    raise RuntimeError("Orthogonal of composite.")
    print "                  TODO orthogonal of a composite>>>>>>>"
    rect = self.get_dimensions()
    return coordinates.rectangle_orthogonal(rect, point)
    
  
  """
  Using transforms, propagation not necessary.
  
  @dump_event
  def set_origin(self, point):
    '''
    Move group to a new origin.
    Width and height depend on members.
    '''
    transformer.Transformer.set_origin(self, point)  # super
    if len(self) > 1:
      print "Set origin on a composite with many items."
    else:
      self[0].set_origin(point)
    # FIXME No need for all this.  Just set super then layout, always.
    '''
    OLD
    # This triggers a warning about setting composite dimensions in set_dimensions??
    self.set_dimensions(rect)
    # drawable.Drawable.set_origin(self, rect)
    # !!! Caller must also layout and invalidate ??
    '''
    # Layout changes origins of members
    self.layout(point)
  """
 
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
  
  
  """
  
  OLD
  @dump_event
  def move_relative(self, event, offset):
    '''
    Move origin relative. Redraw.
    TODO set_dimensions?
    '''
    for item in self:
      item.move_relative(event, offset)
  """
  
  @dump_event
  def highlight(self, direction):
    # TODO transform??
    for item in self:
      item.highlight(direction)
  
  
  def activate_controls(self, event):
    '''
    Activating controls is NOT aggregate, but only on the top level.
    I.E. Don't activate all the controls in a tree of morphs.
    '''
    print "Virtual activate controls"
   
   
   
   
