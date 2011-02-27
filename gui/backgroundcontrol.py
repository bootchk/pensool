#!/usr/bin/env python

import gui.control
import gui.manager.drop
import gui.manager.focus
import gui.manager.textselect
import gui.manager.handle
import gui.manager.pointer
import controlinstances
import scheme
from decorators import *
import base.alert as alert
import base.vector as vector

from gtk import gdk
import port



  
  


class BackgroundManager(gui.control.GuiControl):
  '''
  A special control that manages background,
  that is, events when no other smaller controls are active.
  
  The background is: anywhere in the window not near a morph edge.
  TODO: inside a morph is in the background? Filled versus unfilled?
  
  Understands:
    bkgd context menu
    bkgd handle menu
    interaction with morphs via handle menus
    inside morphs
    via the bkgd context menus:
      controlling ports:
        view
        printerport
        fileport
  '''
  def __init__(self, printer_port, file_port):
    # handle_group, menu, 
    gui.control.GuiControl.__init__(self) # super
    self.printerport = printer_port
    self.fileport = file_port
    # !!! Controls self, ie the document
    # FIXME this is wierd.  None?  Document model?
    self.controlee = self
    self.set_background_bounds()
    gui.manager.pointer.register_callback(self.pick_cb)
  
  def set_background_bounds(self):
    ''' 
    Set the invisible, undrawn bounds of the background.
    This is a control, a drawable, has bounds
    even though it is not really drawn.
    Might not be necessary?
    '''
    self.bounds.from_rect(port.view.da.allocation)
  
  @dump_event
  def pick_cb(self, point):
    '''
    A callback.
    Called when pointer has stopped moving.
    Point is approximately coordinates of pointer when it stopped.
    Pick (popup on mouseover.)
    '''
    
    # Pick: detect pointer intersect handles
    # Handles are in foreground, pick them first.
    picked_handle = gui.manager.handle.pick(point)  # TODO was event
    if picked_handle:
      print "Picked handle !!!!!!!!!!!!!!!!!!!!!!!!"
      return True
      
    # Pick: detect pointer intersect morph edges
    context = port.view.user_context()
    picked_morph = scheme.model.pick(context, point)
    if picked_morph:
      gui.manager.focus.focus(picked_morph)
      controlinstances.handle_menu.open(point, picked_morph) # !!! Open at event DCS
      # !!! Closing handle menu cancels focus
      return True
    
    # If nothing else picked, open handle menu on document
    self.open_document_handle_menu()
    return True
    
    # ALT design: wait for control key to open handle menu on doc
    # return False  # nothing picked
  
  
  def configure_event_cb(self, widget, event):
    ''' 
    Event from window manager: window size changed.
    We don't care about window moves?
    '''
    self.set_background_bounds()
  
  
  # @dump_event
  def motion_notify_event_cb(self, widget, event):
    '''
    !!! Overrides default motion callback for GuiControl.
    Does not check for in bounds, that is handled by the desktop window manager.
    '''
    # TODO activate background controls ie handles on inside of window frame?
    # TODO draw the page frame
    
    # Event compression not needed. ne = gdk.event_peek(), ne.free() never seems to return any events
    
    self.pointer_DCS = vector.Vector(event.x, event.y) # save for later key events
    # print "Motion", self.pointer_DCS
    
    # TODO not handling mouse exit see guicontrol.py
    
    if gui.manager.drop.dropmgr.is_drag():
      # TODO find probe suitable targets
      gui.manager.drop.dropmgr.continued(event, self)
      return True
      
    # pointer manager decides if stopped and callbacks pick_cb
    gui.manager.pointer.decide_stopped(event)
          
    return True # Did handle event


  '''
  Other callbacks are inherited from guicontrol
  and come here as these filtered events.
  '''


  def button_press_left(self, event):
    '''
    Generally: left button pressed: begin drag. 
    App logic: background control drags are pans of view.
    Since the background controls the document,
    meaning of drag is move (pan) document beneath the window.
    IE a hand icon drag.
    '''
    # TODO consolidate in guicontrol? and delay start until movement
    self.start_drag(event)
  
  
  def button_release_left(self, event):
    '''
    This defines that the background manager accepts a left drop.
    From self into self: becomes drop()
    Drops from not self to self handled differently, see guicontrol.
    '''
    gui.manager.drop.dropmgr.end(self, event)
  
    
  def button_press_right(self, event):
    '''
    This defines that background manager shows traditional context menu.
    
    Controlee is self, the background manager.
    '''
    controlinstances.document_menu.open(event, self)
  
  
  def scroll_up(self, event):
    '''
    Scroll wheel event in background.
    Convert to zoom op on *document*.
    '''
    print "Scrolling", repr(event)
    # Zoom is an operation on the viewing transformation and model
    scheme.model.zoom(0.5, event, port.view.user_context())
    # FIXME constant for zoom speed
  
  
  def scroll_down(self, event):
    scheme.model.zoom(2.0, event, port.view.user_context())
  
  
  def open_document_handle_menu(self):
    '''
    Open handle menu on document (a composite morph.)
    Not passed event, which might be a KeyEvent or None, 
    but current pointer coords 
    ??? if they are in window and not inside a graphic morph.
    '''
    
    # !!! controlee is model i.e. document i.e. group of graphics
    controlinstances.handle_menu.open(self.pointer_DCS, controlee=scheme.model)
      
    """
    try:
    except Exception as exception_instance:
      print "Exception", type(exception_instance)
      alert.alert("??? Mouse not in background?")
    """
    
  @dump_event
  def control_key_release(self, event):
    '''
    Show handle menu control so user can create independent morphs at top level of scheme.
    '''
    self.open_document_handle_menu()
    
    
    
  @dump_event
  def bland_key_release(self, event):
    '''
    Background mgr redirects ordinary keys to active text selection if any.
    '''
    selection = gui.manager.textselect.get_active_select()
    if selection:
      selection.key(event)
    else:
      alert.alert("No text selection is active to receive keys.")
     
    
    
  """
  Drag and drop.
  """ 

  @dump_event
  def start_drag(self, event):
    '''
    controlee is the view ie the entire doc?? TODO
    '''
    ### self.is_dragging = True
    gui.manager.drop.dropmgr.begin(event, controlee=scheme.model, control=self)
    
  
  @dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost document being dragged in the view
    '''
    #TODO ghosting
    
    
  @dump_event
  def drop(self, source, event, offset, source_control):
    '''
    Source object dropped in background at event.
    Source object can be:
      document (background, distant)
      morph (middle)
      control (foreground, close)
    !!! The background is agnostic about drops: tell source control to act.
    !!! Except if the background is the source of the drag.
    '''
    
    ###if self.is_dragging:
    if source_control is self:  # Did drag start in background?
      # backgroundctl controls view.  Assert source is the scheme.
      source.move_relative(offset)
    ###  self.is_dragging = False  # Local drag state
    else:    # Drag started in another control.
      source_control.drop(source, event, offset, source_control)
    
    
  '''
  Drawing methods
  '''
  
  def draw(self, context):
    '''
    !!! One of few controls to override draw.  
    This control is not visible: draw nothing, just pass.
    It has attributes of a drawable (size).
    TODO use the size to implement frame controls on the background.
    '''
    print "Not drawing background manager"
    pass


  def put_path_to(self, context):
    '''
    Background manager has a path equal to its rectangular window.
    We don't draw path but it is necessary for bounds for invalidate.
    '''
    context.rectangle(self.bounds.x, self.bounds.y, self.bounds.width, self.bounds.height)

    
    
# Scraps
# self.fileport.do_save()
# self.printerport.do_print()
# Zoom uniformly in both axis

    
