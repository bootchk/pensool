'''
Copyright 2010, 2011 Lloyd Konneker

    This file is part of Pensool.

    Pensool is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

customwidgetevents.py

Disclaimer: I am not an authority on Pyusecase.  I could be mistaken.  The code seems to work.

In general, a file of this name extends or customizes pyusecase to support more widgets.
This particular example supports gtk.DrawingArea widget and some of its events.

Note that the tested app must return False from its handlers for the corresponding toolkit events
because pyusecase handlers follow (are after) in the responsibility chain.
Also the pyusecase documentation says even returning False is insufficient, use stop_emission().

See:
texttest/source/pyusecase/lib/usecase.py for superclass UserEvent (generic to all apps)
.../guiusecase.py for class GuiEvent(UserEvent) (for all gui toolkits)
.../gtkusecase/simulator/basevents.py etc. for:
  GtkEvent(GuiEvent)
  SignalEvent(GtkEvent) subclasses for gtk

A pyusecase UserEvent is sort of a proxy for toolkit events in a UI.
UserEvents are high level and abstract; toolkit events are low level and concrete.
A UserEvent is a proxy in the sense that it controls access to toolkit events:
it filters on recording, and generates on playback.
You might also think of it as an adapter.
It also associates a widget with a toolkit event 
(each pair is a distinct UserEvent.)

API for events:

attributes:
  signalName: string constant for the signal name as defined by the gui toolkit
  eventType: string constant for the signal type (class, group) as defined by the gui toolkit
    each eventType has different attributes
  
Record  time methods:

shouldRecord(self, widget, event, *args):
  return whether to record given event on given widget with given args
  Default (base class) implementation returns True.
  Override to filter events (beyond compression and others already builtin.)
  
outputForScript(): return a string to be written to a usecase
  Self is a UserEvent.
  The first variable argument is the toolkit event.
  Base class implementation returns just the name of the event.
  Override if you need to capture arguments (i.e. concrete event details.)

isStateChange():
  define to return True to compress a sequence of same type events to the last in the sequence
  
Playback time methods:

getEmissionArgs(): return a toolkit event constructed from given args to emit at replay time.
  Must define.

Other (record and playback time?):

connectRecord(): connects event to gui toolkit
  Only override base class method if special connection is needed.

'''

from usecase.gtktoolkit.simulator.baseevents import SignalEvent
import gtk


class ConfigureEvent(SignalEvent):
  '''
  Window configuration: move, resize, stacking order.
  '''
  signalName = "configure-event"
  eventType = gtk.gdk.CONFIGURE

  def outputForScript(self, widget, *args):
    '''
    Return string repr of event and its attributes.
    That is, adapt gtk event to usecase command.
    Called at record time.
    '''
    event = args[0]
    return " ".join((self.name, str(event.x), str(event.y), str(event.width), str(event.height)))
 
  def isStateChange(self):
    ''' 
    True means only capture the final event in a series of these event type.
    If the SUT is animated (ghosting a drag for example), 
    you might presume that the last event suffices to test.
    Called at record time.
    '''
    return True
 
    
  def getEmissionArgs(self, argumentString):
    '''
    Return concret toolkit event.
    That is, adapt usecase command to gtk event.
    Inverse of outputForScript
    Called at playback time.
    '''
    event = gtk.gdk.Event(self.eventType)
    int_args = [int(x) for x in argumentString.split()] # parse and convert to list of ints
    event.x = int_args[0]
    event.y = int_args[1]
    event.width = int_args[2]
    event.height = int_args[3]
    return [ event ]

"""
class ExposeEvent(SignalEvent):
  '''
  Expose: an area needs to be redrawn.
  '''
  signalName = "expose-event"
  eventType = gtk.gdk.EXPOSE

  def outputForScript(self, widget, *args):
    '''
    Return string repr of event and its attributes.
    That is, adapt gtk event to usecase command.
    Called at record time.
    '''
    event = args[0]
    # !!! Note in gtk the rect is a separate attribute: area
    # Not using the count attribute
    return " ".join((self.name, str(event.area.x), str(event.area.y), 
      str(event.area.width), str(event.area.height)))
  
  def isStateChange(self):
    ''' 
    True means only capture the final event in a series of these event type.
    If the SUT is animated (ghosting a drag for example), 
    you might presume that the last event suffices to test.
    Called at record time.
    '''
    # TODO For expose events, want compression?
    return True

  def getEmissionArgs(self, argumentString):
    '''
    Return concret toolkit event.
    That is, adapt usecase command to gtk event.
    Inverse of outputForScript
    Called at playback time.
    '''
    event = gtk.gdk.Event(self.eventType)
    int_args = [int(x) for x in argumentString.split()] # parse and convert to list of ints
    event.area.x = int_args[0]
    event.area.y = int_args[1]
    event.area.width = int_args[2]
    event.area.height = int_args[3]
    event.count = 0 # Count of following expose events
    return [ event ]
"""

class PointerEvent(SignalEvent):
  ''' 
  Base class for pointer events.
  Pointer event attributes: x, y, time.
  Subclasses are Motion and Button.
  That is, mouse move and mouse button press and release.
  Doesn't include the scroll wheel on a mouse.
  What is in common is how we record and playback the attributes.
  '''
  def outputForScript(self, widget, *args):
    '''
    Return string repr of event and its attributes.
    That is, adapt gtk event to usecase command.
    Called at record time.
    '''
    event = args[0]
    # print "Event ", event.x, " ", event.y
    # !!! gtk returns coords of pixels as floats
    # Arbitrarily, and just for ease of reading, store as ints
    return " ".join((self.name, str(int(event.x)), str(int(event.y)), str(event.time)))
 
  def isTimed(self, argumentString):
    ''' 
    Return the time from this event if it has one, else None. 
    Called at playback time.
    '''
    int_args = [int(x) for x in argumentString.split()] # parse and convert to list of ints
    return int_args[2]

 
  def getEmissionArgs(self, argumentString):
    '''
    Return concrete toolkit event.
    That is, adapt usecase command to gtk event.
    Inverse of outputForScript().
    Called at playback time.
    '''
    event = gtk.gdk.Event(self.eventType)
    int_args = [int(x) for x in argumentString.split()] # parse and convert to list of ints
    # !!! gtk wants float for pixel coords
    event.x = float(int_args[0])
    event.y = float(int_args[1])
    event.time = int_args[2]
    return [ event ]

  
class MotionEvent(PointerEvent):
  ''' Pointer motion event. '''
  signalName = "motion-notify-event"
  eventType = gtk.gdk.MOTION_NOTIFY
  
  ''' 
  !!! Recording all motion events.
  Note since we don't define isStateChange(self), we don't compress motion events.
  '''
  def shouldRecord(self, widget, event, *args):
    return True


class PointerButtonEvent(PointerEvent):
  '''
  Base class for pointer (mouse) button events.
  
  !!! Inherits shouldRecord():  recording all pointer button events
  '''
  def outputForScript(self, widget, *args):
    ''' Tack button number arg onto args from superclass.'''
    event = args[0]
    # call super for prefix, then tack on button
    return PointerEvent.outputForScript(self, widget, *args) + " " + str(event.button)
    
  
  def getEmissionArgs(self, argumentString):
    ''' Additionally give value to button (number) attribute of GTK event from emission args from base class '''
    [event] = PointerEvent.getEmissionArgs(self, argumentString) # super
    int_args = [int(x) for x in argumentString.split()] # parse and convert to list of ints
    event.button = int_args[3]
    return [ event ]

''' 
Note these classes are not differentiated by button number.
Event instances in a usecase ARE differentiated by button number
via an arg of the instance (a line in the usecase has a button number appended.)
And event instances in a usecase playback GTK events having button numbers.
'''
class ButtonPressEvent(PointerButtonEvent):
  signalName = "button-press-event"
  eventType = gtk.gdk.BUTTON_PRESS

class ButtonReleaseEvent(PointerButtonEvent):
  signalName = "button-release-event"
  eventType = gtk.gdk.BUTTON_RELEASE
    
"""
Note the following won't work.
You can't have two event classes for the same GTK event type.
Pyusecase can't dispatch a GTK event
by examining its attributes, only its type.

class LMBPressEvent(PointerButtonEvent):
  ''' Left mouse button RMB is 1 in GTK '''
  signalName = "button-press-event"
  buttonNumber = 1
  eventType = gtk.gdk.BUTTON_PRESS
  
class RMBPressEvent(PointerButtonEvent):
  ''' Right mouse button RMB is 3 in GTK '''
  signalName = "button-press-event"
  buttonNumber = 3
  eventType = gtk.gdk.BUTTON_PRESS
"""

# Standard module attribute defining custom widget events
# List of tuple pairs of widget types and list of events
customEventTypes = [(gtk.DrawingArea, [ ConfigureEvent, MotionEvent, 
  ButtonReleaseEvent, ButtonPressEvent ])]


