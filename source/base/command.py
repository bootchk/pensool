'''
Command pattern
'''

'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
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
  Note callables should usually be defined (..., *args)
  as call time args may vary.
  '''
  def __init__(self, cmd, *args):
      self._cmd=cmd   # callable
      self._args=args # define time args

  def __call__(self, *args):
    # cat define time and call time args
    return apply(self._cmd, self._args+args)

# Singleton NullCommand
NULL_COMMAND = NullCommand()

