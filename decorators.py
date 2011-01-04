#!/usr/bin/env python

'''
decorators:

Generically: functions that modify other functions i.e. metaprogramming.
Also similar to macros.

Specifically, modify function calls with pre- and post- operations.
'''
import inspect  # for indent by stack depth


'''
Development decorators
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
    depth = len(inspect.stack())  # Indent message by call stack depth
    print " "*depth, fname, ",".join(
      '%s=%s' % entry
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
    depth = len(inspect.stack())  # Indent message by call stack depth
    # use %r for repr() %s for str()
    print " "*depth, fname, "returns", value, ",".join(
        '%s=%s' % entry for entry in zip(argnames,args) + kwargs.items())
    return value
  return dump_return



'''
Production decorators
'''
def view_altering(func):
  '''
  Decorator: wrap decorated func in invalidates.
  Decorated func alters the view: transform or style.
  Self is a drawable.
  
  When view is altered, must redraw:
  the former region (possibly erased)
  AND the new region (possibly different)
  Former region, as already drawn.
  New region, not drawn yet, must calculate.
  '''
  def view_altering_decor(self, *args, **kwargs):
    
    self.invalidate_as_drawn()
    value =func(self, *args, **kwargs)
    self.invalidate_will_draw()
    return value
  return view_altering_decor


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
