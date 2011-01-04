#!/usr/bin/env python

'''

'''

from gtk import gdk

def alert(msg):
  gdk.beep()
  print msg
  
