#!/usr/bin/env python

import gui.control
import gui.manager.drop
import gui.manager.focus
import gui.manager.textselect
import gui.manager.handle
import gui.manager.pointer
import gui.manager.control
import controlinstances
import scheme
from decorators import *
import base.alert as alert
import base.vector as vector

from gtk import gdk
import port



  
  


class BackgroundControl(gui.control.GuiControl):
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
  
  def deactivate(self):
    '''
    Overrides control.deactivate()
    Background control cancels timer.
    '''
    gui.manager.pointer.cancel_timer()
    
    
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
    Attempt pick (popup on mouseover.)
    
    !!! A race.  Don't open a menu if already open.
    
    Return True if successfully open a control,
    else False to continue the periodic pointer timer.
    '''
    
    # Pick: detect pointer intersect handles
    # Handles are in foreground, pick them first.
    picked_handle = gui.manager.handle.pick(point)  # TODO was event
    if picked_handle:
      print "Picked handle !!!!!!!!!!!!!!!!!!!!!!!!"
      # TODO open a menu on the handle
      return True
      
    # Pick: detect pointer intersect morph edges
    context = port.view.user_context()
    picked_morph = scheme.model.pick(context, point)
    if picked_morph:
      self._open_menu(point, picked_morph, controlinstances.handle_menu)
      # !!! Closing handle menu cancels focus
      return True
    
    # If nothing else picked, open handle menu on document
    self._open_menu(point, scheme.model, controlinstances.handle_menu)
    return True
    
    # ALT design: wait for control key to open handle menu on doc
    # return False  # nothing picked
  
  
  def configure_event_cb(self, widget, event):
    ''' 
    Event from window manager: window size changed.
    We don't care about window moves?
    '''
    self.set_background_bounds()
  
  
  #@dump_event
  def motion_notify_event_cb(self, widget, event):
    '''
    Pointer move event from GUI toolkit.
    
    !!! Overrides default motion callback for GuiControl.
    Does not check for in bounds, that is done by desktop window manager.
    
    At this juncture, the document is NOT the operand, so no need to feedback.
    Alternatively, we could show handles on the window frame, etc.
    
    Event compression on mouse events not needed: ne = gdk.event_peek(), ne.free() 
    never seems to return any events.
    '''
    self.pointer_DCS = vector.Vector(event.x, event.y) # save for later key events
    # print "Motion", self.pointer_DCS
    
    if gui.manager.drop.dropmgr.is_drag():
      # TODO find probe suitable targets
      gui.manager.drop.dropmgr.continued(event, self)
    else:   
      # pointer manager decides if stopped and callbacks pick_cb
      gui.manager.pointer.decide_stopped(event)   
    return True # Did handle event


  '''
  Other callbacks are inherited from guicontrol
  and come here as these filtered events.
  
  TODO not handling mouse exit see guicontrol.py
  Since the background is the entire window, pointer leaving window could
  generate a filtered event mouse_exit.
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
    From self into self: becomes self.drop()
    Drops from not self to self are handled differently:
    dropmgr calls the originating control drop() method.
    '''
    gui.manager.drop.dropmgr.end(self, event)
    # Since a drag is no longer happening, reset the pointer manager
    # so that further motion delays before picking.
    gui.manager.pointer.reset()
  
    
  def button_press_right(self, event):
    '''
    This defines that background manager shows traditional context menu.
    Controlee is document.
    '''
    self._open_menu(event, scheme.model, controlinstances.document_menu)
  
  
  #@dump_event
  def scroll_up(self, event):
    ''' Scroll wheel event in background is zoom op on *document*. '''
    scheme.zoom(True, event) # zoom in
  
  def scroll_down(self, event):
    scheme.zoom(False, event)
  
      
  @dump_event
  def control_key_release(self, event):
    '''
    Show handle menu so user can create independent morphs at top level of scheme.
    '''
    self._open_menu(self.pointer_DCS, scheme.model, controlinstances.handle_menu)

    
  @dump_event
  def bland_key_release(self, event):
    '''
    Background control redirects ordinary keys to active text selection if any.
    '''
    selection = gui.manager.textselect.get_active_select()
    if selection:
      selection.key(event)
    else:
      alert.alert("No text selection is active to receive keys.")
     
  '''
  Private functions
  '''
  
  def _open_menu(self, point, morph, menu):
    if gui.manager.control.control_manager.is_root_control_active():
      # deactivate self, the background control
      gui.manager.control.control_manager.deactivate_current_control()
      # Open at event DCS on the given morph
      menu.open(point, morph)
      gui.manager.focus.focus(morph)
    # else this is a race, some other control already open
    

    
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

    
