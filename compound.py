#!/usr/bin/env python

'''
Composite drawables i.e. groups i.e. containers of drawables.

Subclasses are menus and morphs.

Composites can contain other composites, or primitives (guicontrols or glyphs.)
'''
# FIXME rename to composite

import drawable
from decorators import *
import coordinates
import layout



'''
It might be better not to inherit from list,
but to implement standard container API,
or to have-a container instead of be-a container.
'''




class Compound(list, drawable.Drawable):
  '''
  A container of Drawables.
  
  Isolates hierarchy aspects:
  Compounds aggregate properties from their members.
  Compounds donate default properties to members.
  (Members inherit properties from parents.)
  
  !!! Drawable.invalidate() 
    is_inpath() 
    get_bounds()
  are inherited.
  They call put_path_to() which comes here and it does the right thing.
  '''
  
  def __init__(self, viewport):
    drawable.Drawable.__init__(self, viewport)
    self.viewport = viewport
    # self.stroke_width = 1       # TODO style
    self.layout_spec = layout.LayoutSpec()
    
    
  #@dump_event
  def draw(self, context):
    '''
    Iterate draw contained objects.
    The drawing order is important.
    !!! Note we draw separately, not in one stroke.
    '''
    for item in self:
      item.draw(context)
 
 
  
  def put_path_to(self, context):
    '''
    Aggregate the paths of members.
    '''
    for item in self:
      item.put_path_to(context)
  
  
  @dump_event
  def orthogonal(self, point):
    '''
    Orthogonal of a composite is ??
    To the bounding box?
    To hitted member and let user slide between members?
    FIXME Aggregate the orthogonal of all members that intersect the point??
    '''
    print "                  TODO orthogonal of a composite>>>>>>>"
    rect = self.get_dimensions()
    return coordinates.rectangle_orthogonal(rect, point)
    ## return self[0].orthogonal(point)
    
  
  @dump_event
  def set_origin(self, rect):
    '''
    Move group to a new origin.
    Width and height depend on members.
    '''
    """
    # Each one of these triggers the dimensions property setter
    # and that adjusts the width, height each time !!!!
    self.dimensions.x = rect.x
    self.dimensions.y = rect.y
    """
    # This triggers a warning about setting composite dimensions in set_dimensions??
    self.set_dimensions(rect)
    # drawable.Drawable.set_origin(self, rect)
    # !!! Caller must also layout and invalidate
    # layout changes origins of members
    self.layout(rect)
 
 
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
    
  
  '''
  Dimensions property.
  !!! A compound has dimensions.  Its members also have dimensions.
  Layout() propagates dimensions to members.
  After changing dimensions, caller should call layout() and invalidate().
  '''
  
  @dump_event
  def set_dimensions(self, rect):
    '''
    !!! Overrides drawable.set_dimensions, setter for the dimensions property.
    This is for a morph, which is a composite with one item.
    TODO is this a resize?  
    Why can't you resize a composite and layout/resize all members?
    '''
    if len(self) > 1:
      '''
      This is just what is asked for: layout may recompute dimensions from member
      dimensions.
      '''
      drawable.Drawable.set_dimensions(self, rect)  # super
      print "Set dimensions on a composite with many items."
    else:
      # It only makes sense to set the origin, but doesn't hurt to set w,h
      # since layout() should soon recalculate it.
      self[0].set_dimensions(rect)
      
      # self.layout()
 
  
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
  # !!! Redeclare the property on this subclass of Drawable.
  dimensions = property(get_dimensions, set_dimensions)
  """
  
  
  
  
  def move_relative(self, event, offset):
    '''
    Move origin relative. Redraw.
    TODO set_dimensions?
    '''
    print "compound.move_relative", repr(self), "by ", offset.x, offset.y
    # Move members
    for item in self:
      item.move_relative(event, offset)

  
  @dump_event
  def highlight(self, direction):
    # highlight components
    for item in self:
      item.highlight(direction)
  
  
  def invalidate(self):
    for item in self:
      item.invalidate()


  def activate_controls(self, event):
    '''
    Activating controls is NOT aggregate, but only on the top level.
    I.E. Don't activate all the controls in a tree of morphs.
    '''
    print "Virtual activate controls"
   
   
   
   
