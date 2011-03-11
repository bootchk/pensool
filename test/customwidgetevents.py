'''
customwidgetevents.py

This makes pyusecase track certain events in the DrawingArea.

See texttest/source/pyusecase/lib/guiusecase.py for superclass (generic to all gui toolkits.)
and ... /gtkusecase/simulator/basevents.py etc. for subclasses for gtk

API for events:

attributes:
  signalName: string constant for the signal name as defined by the gui toolkit
  eventType: string constant for the signal type (class, group) as defined by the gui toolkit
    each eventType is a class having different attributes
  
getEmissionArgs: return an event constructed from given args to emit at replay time.
  Must define.
  
shouldRecord: return whether to record given event on given widgth with given args at record time
  Must define to minimally return True.
  Can specialize to filter events.

connectRecord: connects event to gui toolkit
  Only need to define to override base class method if special connection is needed.

'''

from usecase.gtktoolkit.simulator.baseevents import SignalEvent
import gtk


class ConfigureEvent(SignalEvent):
  '''
  Window configuration: move, resize, etc.
  '''
  signalName = "configure-event"
  eventType = gtk.gdk.CONFIGURE


  def outputForScript(self, widget, *args):
    '''
    Return string representation of command and its args.
    Called at record time.  Result goes to script.  Script parsed at playback time.
    '''
    print "self in outputForScript is", self
    return self.name
 
 
  def getEmissionArgs(self, argumentString):
    print "arg string is", argumentString
    event = gtk.gdk.Event(self.eventType)
    '''
    event.x = args[0]
    event.y = args[1]
    event.width = args[2]
    event.height = args[3]
    '''
    return [ event ]

  def shouldRecord(self, widget, event, *args):
   return True
   
   
'''
class MotionEvent(SignalEvent):
   signalName = "motion-notify-event"
   
   def shouldRecord(self, widget, event, *args):
        return SignalEvent.shouldRecord(self, widget, event, *args) and event.button == self.buttonNumber

    def getEmissionArgs(self, argumentString):
        event = gtk.gdk.Event(self.eventType)
        event.x = args[0]
        event.y = args[1]
        return [ event ]
        
   #def connectRecord(self, method):
   #   self._connectRecord(self.widget.get_model(), method)
'''

# Standard name for module containing custom widget events
customEventTypes = [(gtk.DrawingArea, [ ConfigureEvent])]

##  (gtk.DrawingArea, [ MotionEvent])]

