'''
Edit operations: cut, copy, paste.  Glue between app and clipboard.

Strategy is to pickle a morph, put the pickle on the clipboard.

!!! Important to break a morph's reference to parent, else whole model is pickled.
IOW, model tree is doubly linked, remove the rootward references.
Disown: parent breaks with child: remove parent's reference to child morph.
Emancipate: child breaks with parent: Remove child's reference to parent morph.
Adopt: refer parent to child
'''
'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''


import copy
import pickle
import clipboard
from decorators import *

import logging
my_logger = logging.getLogger('pensool')


@view_altering
def do_cut(operand, event=None):
  '''
  Cut from model to clipboard.
  Operand is the morph the user chose Cut upon.
  Event is DCS coords.
  '''
  parent = operand.parent
  operand.parent = None # Emancipate to prevent pickle from crawling uptree
  
  foo = pickle.dumps(operand, pickle.HIGHEST_PROTOCOL)
  clipboard.clipboard.paste(foo)
  
  if parent:  # If not top i.e. cutting document
    parent.remove(operand)  # Disown
  else: # Is top, the document.  Empty the document morph.
    del operand[:]
  # Referred-to cut objects will be garbage collected.
  my_logger.debug("Cutted")


@view_altering
def do_paste(operand, event=None):
  '''
  From clipboard to model.
  Operand is a morph the paste op was chosen upon.
  Event is DCS coords.
  '''
  foo = pickle.loads(clipboard.clipboard.copy())  # Unpickle
 
  # TODO refactor this to transformer.py
  # Transform the pasted morph.
  # Get offset of event from operand group origin.
  # Translate pasted morph to that offset.
  offset = operand.device_to_local(event)
  foo.translation = offset
  # Transforms on unpickled morphs are messed.  Derive them again.
  foo.derive_transform()
  
  operand.insert(foo) # Adopt
  my_logger.debug("Pasted")


# copy does not alter the view
def do_copy(morph, event=None):
  '''
  From model to clipboard.
  '''
  # Temporarily emancipate from model tree
  saved_parent = morph.parent
  morph.parent = None
  
  clipboard.clipboard.paste(pickle.dumps(morph, pickle.HIGHEST_PROTOCOL))
  
  morph.parent = saved_parent # Reverse the emancipate
  my_logger.debug("Copied")
 
 
