#!/usr/bin/env python

'''
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

