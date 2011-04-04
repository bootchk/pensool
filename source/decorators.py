'''
Most Pensool decorators for debug, transform, invalidate.  See also picking.

Generically: functions that modify other functions i.e. metaprogramming.  Like macros.

Specifically, modify function calls with pre- and post- operations.
'''

'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

import inspect  # for indent by stack depth


'''
Development decorators
'''

DEBUG = True

# FIXME rename to dump_call
def dump_event(func):
  '''
  Decorator: dumps a call:  name and args.
  Use for tracing execution.
  
  Since self is a parameter, when used on a class method,
  dumps class, method name, and instance.
  This is useful since many events are handled by different handlers 
  with same method names in different classes and instances.
  '''
  fname = func.__module__ + "." + func.func_name
  argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
  def dump_func(*args, **kwargs):
    if DEBUG:
      depth = len(inspect.stack())  # Indent message by call stack depth
      print " "*depth, fname, ",".join(
        '%s=%s' % entry for entry in zip(argnames,args) + kwargs.items())
    return func(*args, **kwargs)
  return dump_func


def dump_return(func):
  '''
  Decorator: dumps bracket: name and args on entry, return values on exit
  '''
  fname = func.__module__ + "." + func.func_name
  argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
  def dump_return(*args, **kwargs):
    if DEBUG:
      depth = len(inspect.stack())  # Indent message by call stack depth
      print " "*depth, fname, ",".join(
        '%s=%s' % entry for entry in zip(argnames,args) + kwargs.items())
    value = func(*args, **kwargs)
    if DEBUG:
      # use %r for repr() %s for str()
      print " "*depth, fname, "returns", value
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

# FIXME try except IndexError probably first arg not a context
def transforming(func):
  '''
  Decorator: wrap decorated func in save, transform, restore.
  Decorated func alters the view: transform or style.
  Self is a drawable.
  !!! First arg must be a context.
  '''
  def transforming_decor(self, *args, **kwargs):
    args[0].save()
    self.put_transform_to(args[0])
    value = func(self, *args, **kwargs)
    args[0].restore()
    return value
  return transforming_decor


def coords_translated(func):
  '''
  Decorator: translates coords of first argument
  '''
  def new_func(self, event, *args, **kwargs):
    event.x, event.y = self.view.device_to_user(event.x, event.y)
    return func(self, event, *args, **kwargs)
  return new_func
  
  
  
  
def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name
  
  
# FIXME 
'''
This came from composite.

def aggregate(fn):
  def new(self, *args):
    for item in self.items:
      item.fn(*args)
  return new
'''
