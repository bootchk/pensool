
""" The base classes from which widget record/replay classes are derived"""

from usecase.guishared import GuiEvent, MethodIntercept
from usecase.definitions import UseCaseScriptError
import gtk

# Abstract Base class for all GTK events
class GtkEvent(GuiEvent):
    def __init__(self, name, widget, *args):
        GuiEvent.__init__(self, name, widget)
        self.interceptMethod(self.widget.stop_emission, EmissionStopIntercept)
        self.interceptMethod(self.widget.emit_stop_by_name, EmissionStopIntercept)
        self.stopEmissionMethod = None
        
    @classmethod
    def getAssociatedSignal(cls, widget):
        return cls.signalName

    @classmethod
    def canHandleEvent(cls, widget, signalName, *args):
        return cls.getAssociatedSignal(widget) == signalName and cls.widgetHasSignal(widget, signalName)

    @staticmethod
    def widgetHasSignal(widget, signalName):
        if widget.isInstanceOf(gtk.TreeView):
            # Ignore this for treeviews: as they have no title/label they can't really get confused with other stuff
            return widget.get_model() is not None

        # We tried using gobject.type_name and gobject.signal_list_names but couldn't make it work
        # We go for the brute force approach : actually do it and remove it again and see if we succeed...
        try:
            def nullFunc(*args) : pass
            if hasattr(widget, "connect_for_real"): # convention for when we intercept connect, as with dialogs
                handler = widget.connect_for_real(signalName, nullFunc)
            else:
                handler = widget.connect(signalName, nullFunc)
            widget.disconnect(handler)
            return True
        except TypeError:
            return False

    def isTimed(self, argumentString):
        # return time attribute or None
        return None  # override in subclasses
        
    def shouldDelay(self):
        # If we get this when in dialog.run, the event that cause us has not yet been
        # recorded, so we should delay
        topLevel = self.widget.get_toplevel()
        return hasattr(topLevel, "dialogRunLevel") and topLevel.dialogRunLevel > 0

    def getRecordSignal(self):
        return self.signalName

    def connectRecord(self, method):
        self._connectRecord(self.widget, method)

    def _connectRecord(self, gobj, method):
        handler = gobj.connect(self.getRecordSignal(), method, self)
        gobj.connect(self.getRecordSignal(), self.stopEmissions)
        return handler

    def outputForScript(self, widget, *args):
        return self._outputForScript(*args)

    def stopEmissions(self, *args):
        if self.stopEmissionMethod:
            self.stopEmissionMethod(self.getRecordSignal())
            self.stopEmissionMethod = None

    def shouldRecord(self, *args):
        return GuiEvent.shouldRecord(self, *args) and self.widget.get_property("visible")

    def _outputForScript(self, *args):
        return self.name

    def checkWidgetStatus(self):
        if not self.widget.get_property("visible"):
            raise UseCaseScriptError, "widget '" + self.widget.get_name() + \
                  "' is not visible at the moment, cannot simulate event " + repr(self.name)

        if not self.widget.get_property("sensitive"):
            raise UseCaseScriptError, "widget '" + self.widget.get_name() + \
                  "' is not sensitive to input at the moment, cannot simulate event " + repr(self.name)

    def generate(self, argumentString):
        self.checkWidgetStatus()
        args = self.getGenerationArguments(argumentString)
        try:
            self.changeMethod(*args)
        except TypeError:
            raise UseCaseScriptError, "Cannot generate signal " + repr(self.signalName) + \
                  " for  widget of type " + repr(self.widget.getType())


class EmissionStopIntercept(MethodIntercept):
    def __call__(self, sigName):
        stdSigName = sigName.replace("_", "-")
        for event in self.events:
            if stdSigName == event.getRecordSignal():
                event.stopEmissionMethod = self.method

        
# Generic class for all GTK events due to widget signals. Many won't be able to use this, however
class SignalEvent(GtkEvent):
    def __init__(self, name, widget, signalName=None):
        GtkEvent.__init__(self, name, widget)
        if signalName:
            self.signalName = signalName
        else:
            self.signalName = self.getAssociatedSignal(widget)

    @classmethod
    def getAssociatedSignal(cls, widget):
        if hasattr(cls, "signalName"):
            return cls.signalName
        elif widget.isInstanceOf(gtk.Button) or widget.isInstanceOf(gtk.ToolButton):
            return "clicked"
        elif widget.isInstanceOf(gtk.Entry):
            return "activate"

    def getRecordSignal(self):
        return self.signalName

    def getChangeMethod(self):
        return self.widget.emit

    def getGenerationArguments(self, argumentString):
        return [ self.signalName ] + self.getEmissionArgs(argumentString)

    def getEmissionArgs(self, argumentString):
        return []


# Some widgets have state. We note every change but allow consecutive changes to
# overwrite each other. 
class StateChangeEvent(GtkEvent):
    signalName = "changed"
    def isStateChange(self):
        return True
    def shouldRecord(self, *args):
        return GtkEvent.shouldRecord(self, *args) and self.eventIsRelevant()
    def eventIsRelevant(self):
        return True
    def getGenerationArguments(self, argumentString):
        return [ self.getStateChangeArgument(argumentString) ]
    def getStateChangeArgument(self, argumentString):
        return argumentString
    def _outputForScript(self, *args):
        return self.name + " " + self.getStateDescription(*args)
        

class ClickEvent(SignalEvent):
    def shouldRecord(self, widget, event, *args):
        return SignalEvent.shouldRecord(self, widget, event, *args) and event.button == self.buttonNumber

    def getEmissionArgs(self, argumentString):
        area = self.getAreaToClick(argumentString)
        event = gtk.gdk.Event(self.eventType)
        event.x = float(area.x) + float(area.width) / 2
        event.y = float(area.y) + float(area.height) / 2
        event.button = self.buttonNumber
        return [ event ]

    def getAreaToClick(self, *args):
        return self.widget.get_allocation()


class LeftClickEvent(ClickEvent):
    signalName = "button-release-event" # Usually when left-clicking things (like buttons) what matters is releasing
    buttonNumber = 1
    eventType = gtk.gdk.BUTTON_RELEASE

class RightClickEvent(ClickEvent):
    signalName = "button-press-event"
    buttonNumber = 3
    eventType = gtk.gdk.BUTTON_PRESS
