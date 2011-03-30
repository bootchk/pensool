'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''

'''
Timer class.
Wraps gobject timer.
Timer is repeating, periodic until canceled or until callback returns False.
'''

import gobject

class Timer(object):
  def __init__(self):
    self.timer_id = None
    
  def start(self, time, callback):
    # in milliseconds
    self.timer_id = gobject.timeout_add(time, callback)
    
  def cancel(self):
    '''
    Stop timer.
    '''
    if self.timer_id:
      gobject.source_remove(self.timer_id)
      self.timer_id = None
    
  def was_canceled(self):
    '''
    Could be a race between a cancel and timeout.
    '''
    return self.timer_id is None
