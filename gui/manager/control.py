#!/usr/bin/env python

from decorators import *
import port

class ControlsManager():
  '''
  Manages active-ness in a set of controls on a view or window (gtk object that generates events)
  Only one is active at a time.
  Here active means: receiving events, callbacks connected. Also called focus.
  Controls are anonymous here: not keeping references to them.
  Other aspects of controls are also managed by group managers such as menus.
  '''
  
  def __init__(self):
    self.current_control = None
    self.root_control = None

    
  def set_root_control(self, control):
    '''
    Set root control which takes events when no other control does.
    Some events always go to the root control, not to the active control.
    '''
    self.root_control = control
    port.view.da.connect('configure-event', control.configure_event_cb)
    port.view.da.connect('focus-in-event', control.focus_in_event_cb)

    
  #@dump_event
  def activate_control(self, control, event, controlee):
    '''
    Deactivates current control and activate control.
    A swap if there is a current control.
    Also change focus.
    '''
    if control.has_focus:
      print "Redundant activation"
      return
    
    '''
    if event is not None:
      # Position center of control at event
      # !!! If not centered, need debouncing, 
      # since mouse might jiggle right back out
      control.center_at(event)
    '''
    # Reconnect events
    # Mouse and keyboard
    if self.current_control is not None:
      port.view.da.disconnect(self.current_motion_handler)
      port.view.da.disconnect(self.current_press_handler)
      port.view.da.disconnect(self.current_release_handler)
      port.view.da.disconnect(self.current_scroll_handler)
      port.view.da.disconnect(self.current_key_handler)
    self.current_press_handler = port.view.da.connect('button-press-event', control.button_press_event_cb)
    self.current_motion_handler = port.view.da.connect('motion-notify-event', control.motion_notify_event_cb)
    self.current_release_handler = port.view.da.connect('button-release-event', control.button_release_event_cb)
    self.current_scroll_handler = port.view.da.connect('scroll-event', control.scroll_event_cb)
    self.current_key_handler = port.view.da.connect_after('key-release-event', control.key_release_event_cb)
    
    # change focus (invalidates?)
    if self.current_control is not None:
      self.current_control.take_focus(False)
    control.take_focus(True)
      
    self.current_control = control
    control.controlee = controlee
    
    
  def draw_active_control(self, context):
    self.current_control.draw(context)
  
  def deactivate_control(self, control, event):
    '''
    Only call this if no controls will be active (except the root)
    '''
    # The background manager should not deactivate itself
    assert(control is not self.root_control)
    '''
    Activate the background manager
    More generally, the root control.
    This is the second place where defined that background manager controls itself.
    '''
    self.activate_control(self.root_control, event, self.root_control)




# singleton instance, initialized when port is known
control_manager = None



