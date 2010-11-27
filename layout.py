#!/usr/bin/env python

'''
LayoutSpec

Base geometry spec for calculating layout geometry.

A LayoutSpec does not necessarily describe the actual layout.
'''

class LayoutSpec(object):

  def __init__(self):
    self.vector = None
    self.benchmark = None


