#!/usr/bin/env python

'''
Clipboard wrapper.
Wraps clipboard provided by underlying OS/window system.
'''

import gtk

PENSOOL_TARGET = ("PENSOOL", gtk.TARGET_SAME_APP, 1)

class Clipboard(object):

  def __init__(self):
    self.global_clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    # self.clipboard.request_text(self.clipboard_text_received)

    
  def paste(self):
    print "To clipboard"
    # Basic: hardcode text into clipboard
    # self.global_clipboard.set_text("Foo")
    # Advanced: agree to provide clipboard data when asked.
    # Type (file suffix) data we will provide).
    # Note if we don't agree to provide a type, then getters may short circuit, never call our get_clipboard_data_cb
    targets = [("PENSOOL", gtk.TARGET_SAME_APP, 1),("UTF8_STRING",gtk.TARGET_SAME_APP, 1)]
    user_data = 1
    self.global_clipboard.set_with_data(targets, self.get_clipboard_data_cb, self.clear_func, user_data)
    # Store copied object (paste onto clipboard) so we can return it upon a user "paste" (copy from clipboard.)
    # TODO
    return
  
  def get_clipboard_data_cb(self, clipboard, selectiondata, info, data):
    '''
    GTK calls this when clipboard data wanted by an app.
    def get_func(clipboard, selectiondata, info, data):

    '''
    # What target is wanted.
    # FIXME 
    print "get data target", selectiondata.get_target()
    # Possible conversion of what we stored.
    # FIXME
    selectiondata.set("PENSOOL", 8, "Foob")
    return True
    
  def clear_func(self):
    return "Zab"
  
  def targets_cb(self, clipboard, targets, data ):
    for target in targets:
      print target
    # TODO sensitize edit menu
  
  def contents_cb(self, clipboard, selectiondata, data):
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
    self.global_clipboard.request_contents("PENSOOL", self.contents_cb, user_data=None)
    
    # synchronous
    # selectiondata = clipboard.wait_for_contents(target)


    return None
    
  
# Singleton

clipboard = Clipboard()
