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
'''

import compound
import glyph
import scheme # for bounding box


class Morph(compound.Compound):
  '''
  A Morph is a composite glyph with associated controls.
  '''

  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)

  # Some morphs default to have no controls
  def activate_controls(self, direction):
    '''
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
    
    
    
    
