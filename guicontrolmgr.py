#!/usr/bin/env python


class ControlsManager():
  '''
  Manages active-ness in a set of controls on a window (gtk object that generates events)
  Only one is active at a time.
  Here active means: receiving events, callbacks connected. Also called focus.
  Controls are anonymous here: not keeping references to them.
  Other aspects of controls are also managed by group managers such as menus.
  '''
  
  def __init__(self, port):
    self.port = port
    self.current_control = None
    self.root_control = None

    
  def set_root_control(self, control):
    '''
    Set root control which takes events when no other control does.
    Some events always go to the root control, not to the active control.
    '''
    self.root_control = control
    self.port.da.connect('configure-event', control.configure_event_cb)
    self.port.da.connect_after('key-release-event', control.key_release_event_cb)
    self.port.da.connect('focus-in-event', control.focus_in_event_cb)

    
  def activate_control(self, control, event, controlee):
    '''
    Also deactivates the current control !!!
    Really is swap.
    '''
    if control.has_focus:
      print "Redundant activation"
      return
      
    print "Activating control", repr(control)
    
    '''
    if event is not None:
      # Position center of control at event
      # !!! If not centered, need debouncing, 
      # since mouse might jiggle right back out
      control.center_at(event)
    '''
    
    # Reconnect mouse events
    if self.current_control is not None:
      self.current_control.release_focus()
      self.port.da.disconnect(self.current_motion_handler)
      self.port.da.disconnect(self.current_press_handler)
      self.port.da.disconnect(self.current_release_handler)
      self.port.da.disconnect(self.current_scroll_handler)
    self.current_press_handler = self.port.da.connect('button-press-event', control.button_press_event_cb)
    self.current_motion_handler = self.port.da.connect('motion-notify-event', control.motion_notify_event_cb)
    self.current_release_handler = self.port.da.connect('button-release-event', control.button_release_event_cb)
    self.current_scroll_handler = self.port.da.connect('scroll-event', control.scroll_event_cb)
    
    self.current_control = control
    
    control.take_focus()  # feedback focus change to user
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



