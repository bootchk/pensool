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
import coordinates


class Morph(compound.Compound):
  '''
  A Morph is a Composite with associated controls.
  A composite of Morphs and Glyphs.
  '''

  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)


  def activate_controls(self, direction):
    '''
    Activate associated controls.
    
    Some morphs default to have no controls
    If this composite has more than one component, 
    AND if this is the top level of a tree of composites,
    activate control: ghost of bounding box enclosing components.
    Note simple morphs are composites of one element so do not get bounding boxes.
    '''
    if direction:
      if len(self) > 1:
        # Activate singleton bounding box ghost
        scheme.bounding_box.activate(True, self.get_dimensions())
    else:
      scheme.bounding_box.activate(False)


  def get_orthogonal(self, point):
    '''
    Orthogonal of a morph with one member is orthogonal of member.
    
    TODO rip get_orthogonal out of compound???
    '''
    if len(self) > 1:
      print "Orthogonal of a composite morph is orthog to bounding box?????"
      '''
      To hitted member and let user slide between members?
      FIXME Aggregate the orthogonal of all members that intersect the point??
      '''
      rect = self.get_dimensions()
      return coordinates.rectangle_orthogonal(rect, point)
    else:
      return self[0].get_orthogonal(point)
    
    


class LineMorph(Morph):
  def __init__(self, viewport):
    Morph.__init__(self, viewport)
    self.append(glyph.LineGlyph(viewport))
    

class RectMorph(Morph):
  def __init__(self, viewport):
    Morph.__init__(self, viewport)
    self.append(glyph.RectGlyph(viewport))
    
    
class CircleMorph(Morph):
  def __init__(self, viewport):
    Morph.__init__(self, viewport)
    self.append(glyph.CircleGlyph(viewport))


# See also textmorph.py for TextMorph
    
    
    
    
