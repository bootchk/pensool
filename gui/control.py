#!/usr/bin/env python

# import config
# import transformer
import morph.morph
import gui.manager.drop
import drawable
from gtk import gdk
from decorators import *
import base.vector as vector


def report_virtual():
  # During devt..
  import sys
  print "??? Override virtual method", sys._getframe(1).f_code.co_name


class GuiControl(morph.morph.PrimitiveMorph):
  '''
  Base class for GUI controls i.e. widgets.
  
  Has callbacks for *low-level* events, i.e. gtk events.
  Callbacks filter *low-level* into *high-level* gui events:
    drags (not using GTK drags)
    button press and release (high-level)
  Filters low-level events into high-level events for subclasses.
  
  Is active when events are connected to its callbacks.
  (Callbacks are not always connected.)

  A control is a morph because it has-a glyph that is transformed.
  That is, controls are transformable drawables.
  Is-a Morph is-a Transformer is-a Drawable.
  
  Some controls are in a different scheme than the graphic morphs the user is editing.
  The topmost transform for such controls is a user setting or preference.
  
  Other controls are members of another morph, and transformed by their parent morph.
  e.g. a text selection.
  
  Inherits Drawable.draw(), put_path_to(), is_inbounds(), invalidate_will_draw()
  !!! Overrides is_in_control_area see below.
  '''
  
  def __init__(self):
    
    self._reset_state()
    
    # Every control controls another object (model)
    self.controlee = None
    
    self.group_manager = None # Coordination among group subset of controls
    
    # Super init
    # TODO document that using super
    # drawable.Drawable.__init__(self)
    # super is Transformer, then Drawable
    super(GuiControl, self).__init__()
    
    # !!! This is an empty morph (composite.)  Subclasses should append a glyph.
  
  
  def __repr__(self):
    ''' Represent by the class name'''
    return self.__class__.__name__
    
    
  def _reset_state(self):
    '''
    Reset local state variables.
    Local means: there is other state, such as global dragging.
    '''
    self.has_focus = False
    ## self.is_dragging = False
    self.button_pressed = 0
    self.pointer_DCS = None # FIXME a singleton?


  # @dump_return
  def is_in_control_area(self, event):
    '''
    Is the event in the hot area?
    For some controls the hot area is not same as the bounding box.
    Can be overridden.
    '''
    # TODO For most square shaped controls: the bounding box.
    # Faster if use bounding box?
    # Jan. 24 2011 return self.is_inbounds(event)
    return self.in_fill(event)
      
    
  '''
  GTK callbacks
  '''
  @dump_event
  def motion_notify_event_cb(self, widget, event):
    '''
    Fundamental mouse interaction with controls:
      Exit if not mouse still inside.
      Move the control to follow the mouse.
      Continue dragging.
      
    !!! Note this is overridden by the bkgd manager.
    '''
    # !!! Note events and control dimensions are in device coords
    if self.is_in_control_area(event):
      # Remember the last pointer position (not use gtk.get_pointer())
      self.pointer_DCS = vector.Vector(event.x, event.y)
      # print "Inside", repr(self)
      if gui.manager.drop.dropmgr.is_drag():   ### self.is_dragging:
        # Drop manager knows which control is in charge (source or target.)
        gui.manager.drop.dropmgr.continued(event, target=self)
      else:
        self.mouse_move(event)
    else:
      '''
      Note the control continues to exist, with state (eg about drag.)
      It might not be visible.
      Another control will take focus.
      '''
      self._reset_state()
      self.mouse_exit(event)  # Filtered event to subclasses
    return True
  
  
  @dump_event
  def button_press_event_cb(self, widget, event):
    '''
    Button pressed in this active control
    '''
    ## was assert( self.is_inbounds(event))
    # Jan 25 2011 Assertion breaks background control
    # assert( self.is_in_control_area(event))
    
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
      
    
  @dump_event
  def button_release_event_cb(self, widget, event):
    '''
    Button released inside control
    '''
    assert(self.has_focus)
    
    # TODO Check for wierd chording: press, press, release, release
    # TODO If items are large enough, a short drag stays in an item.
    if(not event.button == self.button_pressed):
      # By design, pop-up menus open on press in one button, can release in other buttons.
      print "Button released outside control button was pressed in", self.button_pressed
    else:  # Released in same control as pressed
      print "Button release in same control."
       
    if gui.manager.drop.dropmgr.is_drag():
      # Drag may have started in another control.
      gui.manager.drop.dropmgr.end(self, event)  # self is target
    elif self.group_manager:  # If control is item in group
      # User pressed to open menu, moved to this item, then released to choose.
      self._dispatch_button_release(event)
    else: 
      # This control is NOT a menu AND no drag in effect.
      # Typically: press to open a pop-up, move out, then release to cancel.
      print "Button release outside menu with no drag."
    return True
    
  
  def scroll_event_cb(self, widget, event):
    '''
    Scroll wheel inside control.
    '''
    if event.direction == gdk.SCROLL_UP:
      self.scroll_up(event)
    else :
      self.scroll_down(event)
    return True
    
    
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
    if gdk.keyval_name(event.keyval) == "Control_L" : # Left control
      print "Control key"
      self.control_key_release(event)
    else:
      self.bland_key_release(event)
    return True


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
    print "WINDOW FOCUSED ................"
    # TODO grab_focus() ??  set HAS_FOCUS on the da?
    return True   # This widget took the focus, don't look further.



  '''
  Internal focus: 
  Highlight which control is sensitive (active?)
  Only one control is getting most low-level events.
  '''
  #@dump_event
  def take_focus(self, direction):
    self.has_focus = direction
    self.invalidate_will_draw()
    # Tooltips
    if direction:
      # FIXME more specific.  For now, the class of the control.
      print "Focus", self
      

  
 

  '''
  Virtual methods:
  Filtered events that subclasses should override.
  Filtered and translated according to state of control,
  EG a mouse move translated to a drag if button is down.
  '''
 
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
    
  def continue_drag(self, event, offset, increment):
    report_virtual()  
  
  def drop(self, source, event, offset, source_control):
    report_virtual()
  
  
