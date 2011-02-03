#!/usr/bin/env python

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
  is_
'''

import gtk

PENSOOL_TARGET = ("PENSOOL", gtk.TARGET_SAME_APP, 1)

class Clipboard(object):

  def __init__(self):
    self.global_clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    # self.clipboard.request_text(self.clipboard_text_received)
    self.contents = None

    
  def paste(self, contents):
    print "To clipboard"
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
    print "Len to CB", len(contents)
    return
  
  def _get_clipboard_data_cb(self, clipboard, selectiondata, info, data):
    '''
    GTK calls this when clipboard data wanted by an app.
    This should return clipboard data in the selectiondata struct.
    def get_func(clipboard, selectiondata, info, data):
    '''
    # What target is wanted.
    # FIXME 
    print "get data target", selectiondata.get_target()
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
    
  def _clear_func_cb(self):
    return "Zab"
  
  def targets_cb(self, clipboard, targets, data ):
    for target in targets:
      print target
    # TODO sensitize edit menu
  
  def contents_cb(self, clipboard, selectiondata, data):
    '''
    Called when the provider has provided contents.
    '''
    print "Target", selectiondata.get_target()
    print "Data", selectiondata.data
    pass
    
  def copy(self):
    '''
    From the clipboard
    '''
    # Queue sensitizing of edit menu
    self.global_clipboard.request_targets(self.targets_cb, user_data=None)
    
    # wait_is_text_available() returns True, not the text
    # print "From clipboard, text available:", self.global_clipboard.wait_for_text()
    
    # Queue retrieval of contents
    # self.global_clipboard.request_contents("PENSOOL", self.contents_cb, user_data=None)
    
    # Synchronous: meaning wait, but uses the GTK event loop, so we also can provide while waiting?
    selectiondata = self.global_clipboard.wait_for_contents("PENSOOL")

    print "Len from CB", len(selectiondata.data)
    return selectiondata.data
    
  
# Singleton

clipboard = Clipboard()
