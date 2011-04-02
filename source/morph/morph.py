'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

Morph: drawable composites.  Synonyms: shapes, forms, symbols.

Note morphs are containers, of other morphs or primitive glyphs.

A strategy:
We always instantiate morphs, not glyphs.
A controlee is always a morph, not a glyph.
Thus we can always append to a controlee,
instead of continually checking for a primitive glyph.

Morphs can contain controls:
  TextEditMorph contains a TextSelect (insertion bar)
  
Morphs do NOT contain the BoundingBox morph used for feedback,
it is a singleton.
'''

import composite
import glyph
import config # for scheme and bounding box
import gui.manager.handle
import base.vector as vector
import base.orthogonal as orthogonal
import base.transform as transform
from decorators import *


class Morph(composite.Composite):
  '''
  A Morph is a Composite with associated controls.
  A composite of Morphs or Glyphs.
  '''

  def __init__(self, parent=None):
    composite.Composite.__init__(self, parent)

  """
  UNUSED
  def cleanse(self):
    self.transform = None
    self.retained_transform = None
    
    for item in self:
      item.cleanse()
  """

  # TODO move to composite?  a mixture of transform
  @dump_return
  def insert(self, morph):
    '''
    Insert morph into this group.
    If self is a primitive morph, insert new group morph in hierarchy, i.e. branch.
    Because, if self is a primitive morph, it has a transform that shapes its glyphs
    but we want a distinct transform for the new group [self,morph].
    
    For debugging, return either new branch or self.
    '''
    if self.is_primitive():
      # Standard insert branch into tree.
      parent = self.parent
      branch = Morph()  # new branch, parented soon, on append
      # Assert branch.transform is identity, branch.retained_transform is None
      
      # Rearrange parent of self
      parent.remove(self) # break self, former child from parent
      # !!! But self.parent still points to parent
      branch.append(self) # self, former child of parent, now child of branch
      # !!! Note the above changed self.parent
      branch.append(morph) # new child of new branch
      parent.append(branch) # parent has new child, a branch
      # !!! Sets branch.parent = parent
      branch.retained_transform = transform.copy(parent.retained_transform)
      # Assert branch.transform is identity, branch.retained_transform equals parents
      # Assert parent.transform and parent.retained_transform are untouched
      # print "branch retained", branch.retained_transform
      return branch
    else:
      print "...............Grouping with ", self
      self.append(morph)
      return self

  
  
  def rouse_feedback(self, direction):
    '''
    Assert morph is focused.
    Activate associated feedback.
    
    Feedback:
      handles
      bounding box
     
    Feedback is not a control: doesn't take events.
    Some feedback is pickable.
    Some morphs default to have no controls.
    
    If this composite has more than one component, 
    AND if this is the top level of a tree of composites,
    activate control: ghost of bounding box enclosing components.
    Note simple morphs are degenerate composites (one element) so do not get bounding boxes.
    '''
    """
    # Bounding box only on composites
    if direction:
      if len(self) > 1:
        # Activate singleton bounding box ghost
        config.scheme.bounding_box.activate(True, self.bounds.to_rect())
    else:
      config.scheme.bounding_box.activate(False)
    """
    config.scheme.bounding_box.activate(direction, self.bounds.to_rect())


  #@dump_return
  def get_orthogonal(self, point):
    '''
    Return a unit vector orthogonal to self at point.
    
    Cases:
      zero members: default orthogonal
      one member: orthogonal to member
      many members: orthogonal to bounding box???
      
    Note the point is not necessarily outside the morph.
    '''
    if len(self) > 1:
      # print "Orthogonal of a composite morph is orthog to bounding box?????"
      '''
      It might be better to selectively hit only the frame primitive of some composites.
      But is the frame always drawn?
      To hitted member and let user slide between members?
      FIXME Aggregate the orthogonal of all members that intersect the point??
      '''
      # Note both bounds and point are in DCS
      return orthogonal.rect_orthogonal(self.bounds, point)
    elif len(self) == 1:
      return self[0].get_orthogonal(point)
    else:
      return vector.downward_vector() # upright
      # TODO make this a user preference: conventional orientation for culture
    
  
  """ Virtual"""
  def resize(self, event, offset):
    print "Virtual resize composite morph"
    
  
  def is_primitive(self):
    '''
    Morph that is not class PrimitiveMorph is not primitive.
    A PrimitiveMorph can be a group but only of glyphs.
    A non-primitive morph is a group of other morphs.
    '''
    return False
  
  def is_top(self):
    '''Morph that is the root of the modeling tree. '''
    return self.parent is None
  
  
  @view_altering  
  @dump_event
  def set_by_drag(self, start_coords, event):
    '''
    Establish my dimensions (set transform) 
    according to drag op from start_coords to event.
    My glyph is a unitary thing (unit scale, translation.)
    Set my transform within my parent group's coordinate system (GCS).
    '''
    # assert start_coords and event in device DCS
    # Transform to GCS (Local)
    start_point = self.device_to_local(start_coords)
    event_point = self.device_to_local(event)
    drag_vector_UCS = event_point - start_point
    
    # Scale both axis by vector length
    drag_length_UCS = drag_vector_UCS.length()
    scale = vector.Vector(drag_length_UCS, drag_length_UCS)
    
    # print "start", start_coords, "new", start_point, drag_length_UCS
    self.set_transform(start_point, scale, drag_vector_UCS.angle())


  @view_altering  
  #@dump_event
  def move_by_drag(self, offset, increment):
    '''
    Establish my translation
    according to drag op
    of glyph
    by offset
    '''
    self.move_relative(increment)
    
  @view_altering  
  @dump_event
  def move_by_drag_handle(self, offset, increment):
    '''
    Establish my dimensions (set transform) 
    according to drag op
    of handle
    by offset
    '''
    # FIXME depends on which handle
    # FIXME more complicated
    # This is all in x-axis aligned coordinate system
    assert isinstance(self, Morph)
    drag_vector = self.device_to_local(increment)
    # insure old vector is along x-axis, length given by scale
    old_vector = vector.Vector(self.scale.x, 0)
    new_vector = old_vector + drag_vector
    length = new_vector.length()
    new_scale = vector.Vector(length, length)
    print self.scale, new_scale
    self.set_transform(self.translation, new_scale, self.rotation + new_vector.angle())
    self.derive_transform()
    # self.move_origin(increment)
    

class PrimitiveMorph(Morph):
  '''
  A PrimitiveMorph is a Composite of only Glyphs.
  The transform and style of a PrimitiveMorph defines aspect of its glyph, a unit shape.
  Cannot append a Morph to a PrimitiveMorph, only glyphs.  TODO enforce?
  '''
  # TODO refactor rouse_feedback here
  def is_primitive(self):
    return True

  """
  This does not work because we append a single glyph.
  def append(self, item):
    raise RuntimeError("Appending to primitive morph")
  """


'''
Classes for morphs that user understands, with a shape.

__init__() assigns a glyph (shape)

rouse_feedback() understands feedback:
  1. the set of handles on shape
  2. whether to display a bounding box.
'''

# See also textmorph.py for TextMorph

# For now, user can't create a PointMorph.
# PointMorph used by HandlePoint.
class PointMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.PointGlyph())

class LineMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.LineGlyph())
    
  def rouse_feedback(self, direction):
    config.scheme.bounding_box.activate(direction, self.bounds.to_rect())
    gui.manager.handle.rouse(line_handles, self, direction)

class RectMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.RectGlyph())
    
class CircleMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.CircleGlyph())
  
  def rouse_feedback(self, direction):
    config.scheme.bounding_box.activate(direction, self.bounds.to_rect())
    gui.manager.handle.rouse(circle_handles, self, direction)



'''
Handles: pickable spots on morphs.
Handle menu actions depend on which handle (if any) is picked.
'''

class HandlePoint(PointMorph):
  ''' 
  Handle that is a point.
  
  Draws and picks like user's point morphs.
  
  An action on a handle translates into an action on the morph it handles.
  E.G. dragging the handle on the end of a line drags one end of the line.
  def set_by_drag(
  '''
  
  def __init__(self):
    PointMorph.__init__(self)
    # Set pen width broader than ordinary
    # TODO this should be dynamic, depend on current morph
    self.style.pen_width = 3
    

# class HandleSet(Morph) a set of HandlePoints

# A line morph has set of handles on end points
line_handles = Morph()
line_handles.append(HandlePoint()) # First handle at 0,0 end of unit line
# Second handle at 1,0 end of line
point = HandlePoint()
point.set_translation(vector.Vector(1,0))
line_handles.append(point)

# A circle morph has handle at center.
# TODO temporarily a line
from math import pi as PI
circle_handles = Morph()
aline = LineMorph()
aline.rotation = PI/4.0
aline.derive_transform()
circle_handles.append(aline)



