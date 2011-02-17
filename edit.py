#!/usr/bin/env python

'''
Edit operations: cut, copy, paste.
Glue between app and clipboard.

Strategy is to pickle a morph, put the pickle on the clipboard.
Important to break a morph's reference to parent, else whole model is pickled.
'''
import copy
import pickle
import clipboard
from decorators import *


@view_altering
def do_cut(operand, event=None):
  '''
  From model to clipboard.
  Operand is a morph the cut op was chosen upon.
  Event is DCS coords.
  '''
  operand.parent.remove(operand)
  operand.parent = None
  foo = pickle.dumps(operand, pickle.HIGHEST_PROTOCOL)
  clipboard.clipboard.paste(foo)



@view_altering
def do_paste(operand, event=None):
  '''
  From clipboard to model.
  Operand is a morph the paste op was chosen upon.
  Event is DCS coords.
  '''
  bar = clipboard.clipboard.copy()
  # Unpickle
  foo = pickle.loads(bar)
  print "Paste unpickled:", foo
  
  # Get offset of event from operand group origin.
  # Translate inserted morph to that offset.
  offset = operand.device_to_local(event)
  foo.translation = offset
  # Transforms on unpickled morphs are messed.  Derive them again.
  foo.derive_transform()
  
  print foo.translation, foo.transform
  operand.insert(foo)


# copy does not alter the view
def do_copy(morph, event=None):
  '''
  From model to clipboard.
  '''
  #print "Copying"
  #clone = copy.deepcopy(morph)
  
  # morph.cleanse()
  
  print "Pickling", morph
  # Copy object now so original can change.
  # Divorce from model tree
  bar = morph.parent
  morph.parent = None
  #morph.viewport = None
  foo = pickle.dumps(morph, pickle.HIGHEST_PROTOCOL)
  zed = pickle.loads(foo)
  print zed
  clipboard.clipboard.paste(foo)
  morph.parent = bar
 
  
  # Put object on clipboard.  Not pickled yet.
