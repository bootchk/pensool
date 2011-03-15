'''
customwidgetevents.py

L. Konneker 2011

Disclaimer: I am not an authority.  I could be mistaken.  The code seems to work.

In general, a file of this name extends or customizes pyusecase to support more widgets.
This particular example supports gtk.DrawingArea widget and some of its events.

Note that the tested app must return False from its handlers for the corresponding toolkit events
because pyusecase handlers follow (are after) in the responsibility chain.

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
 
  """
  def isStateChange(self):
    ''' 
    True means only capture the final event in a series of these event type.
    If the SUT is animated (ghosting a drag for example), 
    you might presume that the last event suffices to test.
    Called at record time.
    '''
    return True
  """
 
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

   
class MotionEvent(SignalEvent):
  signalName = "motion-notify-event"
  eventType = gtk.gdk.MOTION_NOTIFY
  
  def shouldRecord(self, widget, event, *args):
    return True
    
  def outputForScript(self, widget, *args):
    '''
    Return string repr of event and its attributes.
    That is, adapt gtk event to usecase command.
    Called at record time.
    '''
    event = args[0]
    # !!! gtk returns coords of pixels as floats
    # Arbitrarily, and just for ease of reading, store as ints
    return " ".join((self.name, str(int(event.x)), str(int(event.y)), str(event.time)))
 
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
    # !!! gtk wants float for pixel coords
    event.x = float(int_args[0])
    event.y = float(int_args[1])
    event.time = int_args[2]
    return [ event ]


# Standard module attribute defining custom widget events
# List of tuple pairs of widget types and list of events
customEventTypes = [(gtk.DrawingArea, [ ConfigureEvent, ExposeEvent, MotionEvent])]


