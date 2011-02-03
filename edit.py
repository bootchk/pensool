#!/usr/bin/env python

'''
Edit operations.
Glue between app and clipboard.
'''
import copy
import pickle
import clipboard


def do_paste():
  '''
  From clipboard to model.
  '''
  pass


def do_copy(morph, event=None):
  '''
  From clipboard to model.
  '''
  #print "Copying"
  #clone = copy.deepcopy(morph)
  
  morph.cleanse()
  
  print "Pickling", morph
  # Copy object now so original can change.
  # Divorce from model tree
  bar = morph.parent
  zed = morph.viewport
  morph.parent = None
  #morph.viewport = None
  foo = pickle.dumps(morph)
  print foo
  morph.parent = bar
  # morph.viewport = zed
 
  
  # Put object on clipboard.  Not pickled yet.
