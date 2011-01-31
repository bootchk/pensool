#!/usr/bin/env python

'''
import pygtk
import gtk 
import cairo
import os
import scheme
import style
import base.vector as vector
from decorators import *
'''

class NullCommand(object):
  def __call__(self, *args):
    ''' Callable with no effect'''
    print "Null command called."
    return
    
class Command(object):
  '''
  Pattern: Command.
  Disconnects most gui code from app logic.
  Also supports Undo?
  '''
  def __init__(self, cmd, *args):
      self._cmd=cmd
      self._args=args

  def __call__(self, *args):
     return apply(self._cmd, self._args+args)

# Singleton NullCommand
NULL_COMMAND = NullCommand()

