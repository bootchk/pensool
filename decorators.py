#!/usr/bin/env python

'''
decorators:

Generically: functions that modify other functions i.e. metaprogramming.
Also similar to macros.

Specifically, modify function calls with pre- and post- operations.
'''

# FIXME rename to dump_call
def dump_event(func):
  '''
  Decorator: dumps a call:  name and params.
  Use for tracing execution.
  
  Since self is a parameter, when used on a class method,
  dumps class, method name, and instance.
  This is useful since many events are handled by different handlers 
  with same method names in different classes and instances.
  '''
  fname = func.func_name
  argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
  def dump_func(*args, **kwargs):
    print "Event ", fname, ",".join(
      '%s=%r' % entry
      for entry in zip(argnames,args) + kwargs.items())
    return func(*args, **kwargs)
  return dump_func


def dump_return(func):
  '''
  Decorator: dumps return values, name, and args
  '''
  fname = func.func_name
  argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
  def dump_return(*args, **kwargs):
    value = func(*args, **kwargs)
    print "Return:", value, "from ", fname, ",".join(
        '%s=%r' % entry for entry in zip(argnames,args) + kwargs.items())
    return value
  return dump_return
  

def coords_translated(func):
  '''
  Decorator: translates coords of first argument
  '''
  def new_func(self, event, *args, **kwargs):
    event.x, event.y = self.viewport.device_to_user(event.x, event.y)
    return func(self, event, *args, **kwargs)
  return new_func
  
  
  
  
def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name
  
  
# FIXME 
'''
This came from compound.

def aggregate(fn):
  def new(self, *args):
    for item in self.items:
      item.fn(*args)
  return new
'''
