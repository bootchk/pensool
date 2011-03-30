'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
'''
'''
Clipboard wrapper.
Wraps clipboard provided by underlying OS/window system.

A singleton within the app, called clipboard.clipboard.
Maintains global_clipboard, the wrapped clipboard.
Wrapped clipboard is available to other running apps.

For now, provide limited targets (data types) globally.
Namely, text.

Locally, provide the PENSOOL type, but no other apps will understand it yet.

API:
  paste(): to clipboard
  copy(): from clipboard
  is_contents(): return whether clipboard has contents  TODO
'''

import gtk
import logging

my_logger = logging.getLogger('pensool')

PENSOOL_TARGET = ("PENSOOL", gtk.TARGET_SAME_APP, 1)

class Clipboard(object):

  def __init__(self):
    self.global_clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    # self.clipboard.request_text(self.clipboard_text_received)
    self.contents = None

    
  def paste(self, contents):
    # Basic: hardcode text into clipboard
    # self.global_clipboard.set_text("Foo")clipboard
    
    # Advanced: agree to provide clipboard data when asked.
    # Type (file suffix) data we will provide).
    # Note if we don't agree to provide a type, then getters may short circuit, never call our get_clipboard_data_cb
    targets = [("PENSOOL", gtk.TARGET_SAME_APP, 1),("UTF8_STRING",gtk.TARGET_SAME_APP, 1)]
    user_data = 1
    self.global_clipboard.set_with_data(targets, self._get_clipboard_data_cb, self._clear_func_cb, user_data)
    # Store copied object (paste onto clipboard) so we can return it upon a user "paste" (copy from clipboard.)
    self.contents = contents
    my_logger.debug('To clipboard ' + str(len(contents)))

  
  def _get_clipboard_data_cb(self, clipboard, selectiondata, info, data):
    '''
    GTK calls this when clipboard data wanted by an app.
    This should return clipboard data in the selectiondata struct.
    '''
    # What target is wanted.
    # FIXME 
    # print "get data target", selectiondata.get_target()
    # Possible conversion of what we stored.
    # FIXME
    ## selectiondata.set("PENSOOL", 8, "Foob")
    # Return the contents of the clipboard
    # Note a gtk clipboard only stores "strings".
    # Python strings will hold binary data.  Therefore, via pygtk, X clipboard
    # can hold binary data.
    # Here 8 means 8 bits per unit.
    selectiondata.set("PENSOOL", 8, self.contents)
    return True
    
  def _clear_func_cb(self, clipboard, selection_data):
    ''' 
    Called when the global clipboard is changed outside this app.
    If this app is interested in changes to that clipboard, AT THE TIME OF THE CHANGE,
    do something here.
    We really don't care to know in realtime that other apps are changing the clipboard,
    so just pass for now, and when this app wants the clipboard, study its contents then.
    TODO How ID the Clipboard?
    '''
    # print "Clear func called on clipboard ", clipboard
    pass
  
  
  def targets_cb(self, clipboard, targets, data ):
    for target in targets:
      # print target
      pass
    # TODO sensitize edit menu

  
  def contents_cb(self, clipboard, selectiondata, data):
    '''
    Called when the provider has provided contents.
    '''
    # print "Target", selectiondata.get_target()
    # print "Data", selectiondata.data
    pass


  def copy(self):
    ''' Copy from the clipboard, return to app to be pasted. '''
    # Queue sensitizing of edit menu
    self.global_clipboard.request_targets(self.targets_cb, user_data=None)
    
    # wait_is_text_available() returns True, not the text
    # print "From clipboard, text available:", self.global_clipboard.wait_for_text()
    
    # Queue retrieval of contents
    # self.global_clipboard.request_contents("PENSOOL", self.contents_cb, user_data=None)
    
    # Synchronous: meaning wait, but uses the GTK event loop, so we also can provide while waiting?
    selectiondata = self.global_clipboard.wait_for_contents("PENSOOL")

    my_logger.debug('From clipboard ' + str(len(selectiondata.data)))
    return selectiondata.data
    
  
# Singleton

clipboard = Clipboard()
