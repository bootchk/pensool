#!/usr/bin/env python

'''
Thin wrapper around informative dialogs with user for error conditions.
See also excepthook that catches most exceptions and calls them bugs.
'''

import gtk
from gtk import gdk

def alert(msg):
  gdk.beep()
  print msg

def _dialog(strength, text):
  ''' Display modal dialog of given strength with given text '''
  # TODO parent window the app instead of None
  md = gtk.MessageDialog(None, 
      gtk.DIALOG_DESTROY_WITH_PARENT, strength, 
      gtk.BUTTONS_CLOSE, text)
  md.run()
  md.destroy()
  
def critical_dialog(text):
   ''' 
   program critical errors.
   usually resources, HW, or external errors
   '''
   _dialog(gtk.MESSAGE_ERROR, text)
   
def warning_dialog(text):
   ''' warnings about user mistakes '''
   _dialog(gtk.MESSAGE_WARNING, text)
