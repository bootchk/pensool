#!/usr/bin/env python

# import config
import dropmanager
import drawable
from gtk import gdk
import coordinates
from decorators import *


def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name


class GuiControl(drawable.Drawable):
  '''
  Base class for GUI controls i.e. widgets.
  
  Has callbacks for *low-level* events, i.e. gtk events.
  Callbacks filter *low-level* into *high-level* gui events:
    drags (not using GTK drags)
    button press and release (high-level)
  Filters low-level events into high-level events for subclasses.
  
  Is active when events are connected to its callbacks.
  (Callbacks are not always connected.)

  Inherits Drawable.draw(), invalidate(), put_path_to(), is_inbounds()
  !!! Overrides is_in_control_area see below.
  '''
  
  def __init__(self, port):
    
    self._reset_state()
    
    # Every control controls another object (model)
    self.controlee = None
    
    self.group_manager = None # Coordination among group subset of controls
    
    # Super init
    drawable.Drawable.__init__(self, port )
    
    
  def _reset_state(self):
    '''
    Reset local state variables.
    Local means: there is other state, such as global dragging.
    '''
    self.has_focus = False
    self.is_dragging = False
    self.button_pressed = 0
    self.pointer = None


  @dump_event
  def invalidate(self):
    ''' 
    Invalidate means queue a region to redraw at expose event.
    GUI specific, not applicable to all surfaces.
    
    !!! A GuiControl is in device coords, does NOT transform at invalidate.
    '''
    device_bounds = self.get_inked_bounds()
    self.viewport.surface.invalidate_rect( device_bounds, True )


  def is_in_control_area(self, event):
    '''
    Is the event in the hot area?
    For some controls the hot area is not same as the bounding box.
    Can be overridden.
    '''
    # For most square shaped controls: the bounding box.
    return self.is_inbounds(event)
      
    
  '''
  GTK callbacks
  '''
  def motion_notify_event_cb(self, widget, event):
    '''
    Fundamental mouse interaction with controls:
      Exit if not mouse still inside.
      Move the control to follow the mouse.
      Continue dragging.
      
    !!! Note this is overridden by the bkgd manager.
    '''
    # print "Mouse moved to", event.x, event.y
    # !!! Note events and control dimensions are in device coords
    if self.is_in_control_area(event):
      # Remember the last pointer position (not use gtk.get_pointer())
      self.pointer = coordinates.DeviceCoords(event.x, event.y)
      # print "Inside", repr(self)
      if self.is_dragging:
        # Drop manager knows which control is in charge (source or target.)
        dropmanager.dropmgr.continued(event, target=self)
      else:
        self.mouse_move(event)
    else:
      '''
      Note the control continues to exist, with state (eg about drag.)
      It might not be visible.
      Another control will take focus.
      '''
      # Reset local state. Global drag state by the dropmanager.
      ### Was self.is_dragging = False 
      self._reset_state()
      self.mouse_exit(event)  # Filtered event to subclasses
    return True
  
  
  @dump_event
  def button_press_event_cb(self, widget, event):
    '''
    Button pressed in this active control
    '''
    ## was assert( self.is_inbounds(event))
    assert( self.is_in_control_area(event))
    
    '''
    !!! Not all controls are draggable.
    Subclasses define whether draggable,
    in their button_press_left method.
    '''
    
    if event.button == 1:
        self.button_pressed = 1
        self.button_press_left(event)
    elif event.button == 3:
      self.button_pressed = 3
      self.button_press_right(event)
    else:
      print "Unhandled button"
      return False
    return True
    
    
  def _dispatch_button_release(self, event):
    '''
    Dispatch a button release.
    Usually dispatch filtered event to a handler
    that is a method in the subclass of the instance.
    '''
    self.button_pressed = 0   # Update state
    # Promote to a click event: Dispatch on type of button
    if event.button == 1:
      self.button_release_left(event)
    elif event.button == 3:
      self.button_release_right(event)
    else:
      # TODO
      raise RuntimeError("Unhandled button " + event.button)
      
    
  def button_release_event_cb(self, widget, event):
    '''
    Button released inside control
    '''
    print "Button released", repr(event), "in", repr(self)
    assert(self.has_focus)
    
    if(not event.button == self.button_pressed):
      print "Button released outside control button was pressed in", self.button_pressed
      # If this control is an item in a group
      if self.group_manager:
        # Button was pressed to open a menu, moved to this item, then
        # released to choose this item.
        self._dispatch_button_release(event)
        # TODO robustness: insure button is same one as opened group?
      else:
        # This control is NOT a menu.
        # Assume it is the background mgr? TODO verify
        # A global drag is in operation, do it.
        # TODO could be a wierd chording of the buttons
        # Cannot assert(self.is_dragging) because dragging started in other
        dropmanager.dropmgr.end(self, event)  # self is target
    else: 
      # Released in same control as pressed
      self._dispatch_button_release(event)
    return True
    
  
  def scroll_event_cb(self, widget, event):
    '''
    Scroll wheel inside control.
    '''
    if event.direction == gdk.SCROLL_UP:
      self.scroll_up(event)
    else :
      self.scroll_down(event)
    
    
  '''
  Keyboard events.
  TODO keyboard modifiers on mouse events.
  '''
  @dump_event
  def key_release_event_cb(self, widget, event):
    '''
    Click
    '''
    # Filter and dispatch control keys
    # TODO key combinations
    if gdk.keyval_name(event.keyval) == "Control_L" :
      print "Control key"
      self.control_key_release(event)
    else:
      self.bland_key_release(event)


  @dump_event
  def focus_in_event_cb(self, widget, event):
    '''
    When the window manager gives our window focus
    (i.e. receiving keyboard events etc.).
    There might be more to do here???
    Generally, we can just resume from our same state when we lost
    focus from the window manager (with the backgroundmgr control
    receiving events.)
    What if a OS window pops up under the mouse and user moves mouse?
    '''
    print "FOCUSED ................"
    # TODO grab_focus() ??  set HAS_FOCUS on the da?
    return True   # This widget took the focus, don't look further.



  '''
  Internal focus: 
  Highlight which control is sensitive (active?)
  Only one control is getting most low-level events.
  '''
  def take_focus(self):
    print "Take focus", repr(self)
    self.has_focus = True
    self.invalidate()   #redraw
    
  def release_focus(self):
    print "Release focus", repr(self)
    self.has_focus = False
    self.invalidate()   #redraw
  
 

  '''
  Virtual methods:
  Filtered events that subclasses should override.
  Filtered and translated according to state of control,
  EG a mouse move translated to a drag if button is down.
  '''

  def start_drag(self, event):
    report_virtual()
    
  def continue_drag(self, event):
    report_virtual()  
  
  def drop(self, source, event, offset, source_control):
    report_virtual()
 
  def mouse_move(self, event):
    '''
    Override to set behavior: whether control can move.
    '''
    report_virtual()
    
  def button_press_left(self, event):
    report_virtual()
    
  def button_release_left(self, event):
    report_virtual()
  
  def button_press_right(self, event):
    report_virtual()
    
  def button_release_right(self, event):
    report_virtual()
  
  def control_key_release(self, event):
    report_virtual()

  def mouse_exit(self, event):
    '''
    If mouse exits the background, window manager grabs it?
    Possible to exit a non-bkgnd control directly to the window manager?
    # print "mouse exit"
    #self.manager.deactivate_control(self, event)
    '''
    report_virtual()
  
  ''' Scrolling '''
  def scroll_up(self, event):
    report_virtual()
  
  def scroll_down(self, event):
    report_virtual()
    

  ''' Drag and drop '''
  def start_drag(self, event):
    report_virtual()
    
  def continue_drag(self, event):
    report_virtual()  
  
  def drop(self, source, event, offset, source_control):
    report_virtual()
  
  
