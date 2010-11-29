#!/usr/bin/env python

import gui.control
import coordinates
import dropmanager
import focusmgr
import scheme
from decorators import *
from gtk import gdk
import textselectmanager



class BackgroundManager(gui.control.GuiControl):
  '''
  A special control that manages background,
  that is, events when no other smaller controls are active.
  Understands:
    bkgd context menu
    bkgd handle menu
    interaction with morphs via handles
    inside morphs
    via the bkgd context menus:
      controlling ports:
        viewport
        printerport
        fileport
  '''
  def __init__(self,
      handle_group, menu, view_port, printer_port, file_port):
    gui.control.GuiControl.__init__(self, view_port)
    # control managers we delegate to
    self.handle_menu = handle_group
    self.context_menu = menu
    # Inherit viewport from Drawable
    self.printerport = printer_port
    self.fileport = file_port
    # !!! Controls self, ie the document
    # FIXME this is wierd.  None?  Document model?
    self.controlee = self

  
  
  def configure_event_cb(self, widget, event):
    '''
    Window size changed.
    We don't care about window moves.
    '''
    self.dimensions = self.viewport.da.allocation
  
  
  # @dump_event
  def motion_notify_event_cb(self, widget, event):
    '''
    !!! Overrides default motion callback for GuiControl.
    Does not check for in bounds, that is handled by the desktop window manager.
    '''
    # TODO activate background controls ie handles on inside of window frame?
    # TODO draw the page frame
    user_coords = self.viewport.device_to_user(event.x, event.y)
    self.pointer_x = event.x
    self.pointer_y = event.y
    # TODO not handling mouse exit see guicontrol.py
      
    # TODO dragging
    if dropmanager.dropmgr.is_drag():
      # TODO find probe suitable targets
      dropmanager.dropmgr.continued(event, self)
    else:
      # Activate handle controls as approach edge of objects
      for morph in scheme.glyphs:
        # !!! Find morph in user coords
        if morph.is_inpath(user_coords):
          focusmgr.focus(morph)
          # !!! Open handle menu at device coords of event
          self.handle_menu.open(event, morph)
          # !!! Closing the handle menu cancels focus
          break # Only one handle at a time TODO intersections
    return True # Did handle event


  '''
  Other callbacks are inherited from guicontrol
  and come here as these filtered events.
  '''


  def button_press_left(self, event):
    '''
    Generally: left button pressed: begin drag. 
    
    This defines that background control accepts drags.
    
    Since the background controls the document,
    meaning of drag is move (pan) document beneath the window.
    IE a hand icon drag.
    '''
    # TODO consolidate in guicontrol? and delay start until movement
    self.start_drag(event)
  
  
  def button_release_left(self, event):
    '''
    This defines that the background manager accepts a left drop.
    From self into self???
    Drops from not self to self handled differently, see guicontrol.
    '''
    dropmanager.dropmgr.end(self, event)
  
    
  def button_press_right(self, event):
    '''
    This defines that background manager shows traditional context menu.
    
    Controlee is self, the background manager.
    '''
    self.context_menu.open(event, self)
  
  
  def scroll_up(self, event):
    '''
    Scroll wheel event in background.
    Convert to zoom op on *document*.
    '''
    print "Scrolling", repr(event)
    self.viewport.zoom(0.5, event)
    # FIXME constant for zoom speed
  
  
  def scroll_down(self, event):
    self.viewport.zoom(2, event)
    
  
  @dump_event
  def control_key_release(self, event):
    '''
    Background mgr shows handle menu for creating morphs.
    '''
    # Handle menu on the entire document (composite.)
    # Not the passed event, which is a key, but the current mouse coords
    # if they are in the window.
    if self.pointer_x != 0 :
      rect = coordinates.dimensions(self.pointer_x, self.pointer_y, 0, 0)
      self.handle_menu.open(rect, controlee=scheme.glyphs)
    else:
      gdk.beep()
    
  @dump_event
  def bland_key_release(self, event):
    '''
    Background mgr redirects ordinary keys to active text selection if any.
    '''
    selection = textselectmanager.get_active_select()
    if selection:
      selection.key(event)
    else:
      gdk.beep()
     
    
    
  """
  def dispatch_drop():
    '''
    Handle drop by what control drag begin.
    '''
  """ 

  @dump_event
  def start_drag(self, event):
    '''
    Mouse starts moving with button down.
    controlee is the view ie the entire doc?? TODO
    '''
    self.is_dragging = True
    dropmanager.dropmgr.begin(event, controlee=scheme.glyphs, control=self)
    
  
  @dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost document being dragged in the viewport
    '''
    #TODO ghosting
    pass
    
    
  @dump_event
  def drop(self, source, event, offset, source_control):
    '''
    Source object dropped in background at event.
    Source object can be:
      document (background, distant)
      morph (middle)
      control (foreground, close)
    !!! The background is agnostic about drops: tell source control to act.
    '''
    # Is a drag starting in the background?
    if self.is_dragging:
      source.move_relative(event, offset)
      self.is_dragging = False  # Local drag state
    else:
      # Drag started in another control
      source_control.drop(source, event, offset, source_control)
    
    
  '''
  Drawing methods
  '''
  
  def draw(self, context):
    '''
    !!! One of few controls to override draw.  
    This control is not visible == draw nothing, just pass.
    It has attributes of a drawable (size).
    TODO use the size to implement frame controls on the background.
    '''
    print "Not drawing background manager"
    pass


 
  def put_path_to(self, context):
    '''
    Background manager has a path equal to its rectangular window.
    We don't draw path but it is necessary for bounds.
    '''
    rect = self.dimensions
    context.rectangle(rect.x, rect.y, rect.width, rect.height)
  
  
  '''
  Commands (undoable?)
  '''
  def move_relative(self, event, offset):
    '''
    Left drag op from background to background.
    
    Command to pan view of *document*.
    
    Event: point dropped
    Offset: from start drag to drop in window coords
    '''
    self.viewport.scroll(offset.x, offset.y)


    
    
# Scraps
# self.fileport.do_save()
# self.printerport.do_print()
# Zoom uniformly in both axis
# self.viewport.scroll(10, 0)
    
