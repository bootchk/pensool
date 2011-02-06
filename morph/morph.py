#!/usr/bin/env python

'''
Morph: drawable composites.  Forms, symbols.

Note morphs are containers, of other morphs or primitive glyphs.

A strategy:
We always instantiate morphs, not glyphs.
A controlee is always a morph, not a glyph.
Thus we can always append to a controlee,
instead of continually checking for a primitive glyph.

Morphs can have associated controls, but don't contain them.
  ghost bounding box
  text select (insertion bar)
'''

import compound
import glyph
import scheme # for bounding box
import base.vector as vector
import base.orthogonal as orthogonal
import base.transform as transform
from decorators import *


class Morph(compound.Compound):
  '''
  A Morph is a Composite with associated controls.
  A composite of Morphs or Glyphs.
  '''

  def __init__(self, parent=None):
    compound.Compound.__init__(self, parent)

  def cleanse(self):
    self.transform = None
    self.retained_transform = None
    
    for item in self:
      item.cleanse()


  # TODO move to compound?  a mixture of transform
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

  def activate_controls(self, direction):
    '''
    Activate associated controls.
    
    Some morphs default to have no controls.
    If this composite has more than one component, 
    AND if this is the top level of a tree of composites,
    activate control: ghost of bounding box enclosing components.
    Note simple morphs are composites of one element so do not get bounding boxes.
    '''
    if direction:
      if len(self) > 1:
        # Activate singleton bounding box ghost
        scheme.bounding_box.activate(True, self.bounds.to_rect())
    else:
      scheme.bounding_box.activate(False)


  @dump_return
  def get_orthogonal(self, point):
    '''
    Orthogonal of a morph with one member is orthogonal of member,
    under my transform.  FIXME apply my transform
    '''
    if len(self) > 1:
      print "Orthogonal of a composite morph is orthog to bounding box?????"
      '''
      It might be better to selectively hit only the frame primitive of some composites.
      But is the frame always drawn?
      To hitted member and let user slide between members?
      FIXME Aggregate the orthogonal of all members that intersect the point??
      '''
      # Note both bounds and point are in DCS
      return orthogonal.rect_orthogonal(self.bounds, point)
    else:
      return self[0].get_orthogonal(point)
    
  
  """ Virtual"""
  def resize(self, event, offset):
    print "Virtual resize morph"
    
  
  def is_primitive(self):
    '''Morph that is not PrimitiveMorph is not primitive, I.E. is a group '''
    return False
    

class PrimitiveMorph(Morph):
  '''
  A PrimitiveMorph is a Composite of only Glyphs.
  The transform of a PrimitiveMorph defines aspect of its glyph, a unit shape.
  Cannot append a Morph to a PrimitiveMorph.  TODO enforce?
  '''
  def is_primitive(self):
    return True


def set_transform_from_parent():
  '''
  '''

class LineMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.LineGlyph())
    
  
  @view_altering  
  @dump_event
  def set_by_drag(self, start_coords, event):
    '''
    Establish my dimensions (set transform) according to drag op from start_coords to event.
    My glyph is a unit line.
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
    """
    dimensions = coordinates.dimensions(start_coords_UCS.x, start_coords_UCS.y, 
      drag_length_UCS, drag_length_UCS)
    self.set_dimensions(dimensions)
    """


class RectMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.RectGlyph())
    
    
class CircleMorph(PrimitiveMorph):
  def __init__(self):
    Morph.__init__(self)
    self.append(glyph.CircleGlyph())


# See also textmorph.py for TextMorph
    
    
    
    
