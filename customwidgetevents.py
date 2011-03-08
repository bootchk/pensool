'''
customwidgetevents.py

This makes pyusecase track pointer motion events in the DrawingArea.
'''

from usecase.gtktoolkit.simulator.baseevents import SignalEvent
import gtk



class MotionEvent(SignalEvent):
   signalName = "motion-notify-event"
   #def connectRecord(self, method):
   #   self._connectRecord(self.widget.get_model(), method)

# Standard name for module containing custom widget events
customEventTypes = [(gtk.DrawingArea, [ MotionEvent])]

