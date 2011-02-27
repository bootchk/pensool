#!/usr/bin/env python

'''
Timer class.
Wraps gobject timer.
Timer is repeating, periodic until canceled or until callback returns False.
'''

import gobject

class Timer(object):
  def __init__(self):
    timer_id = None
    
  def start(self, time, callback):
    # in milliseconds
    self.timer_id = gobject.timeout_add(time, callback)
    
  def cancel(self):
    '''
    Stop timer.
    '''
    gobject.source_remove(self.timer_id)
    self.timer_id = None
    
  def was_canceled(self):
    '''
    Could be a race between a cancel and timeout.
    '''
    return self.timer_id is None
