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



class LineMorph(compound.Compound):
  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)
    self.append(glyph.LineGlyph(viewport))
    

class RectMorph(compound.Compound):
  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)
    self.append(glyph.RectGlyph(viewport))
    
    
class CircleMorph(compound.Compound):
  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)
    self.append(glyph.CircleGlyph(viewport))


# See also textmorph.py for TextMorph
    
    
    
    
