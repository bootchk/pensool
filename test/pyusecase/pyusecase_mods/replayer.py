
""" Generic recorder classes. GUI-specific stuff is in guishared.py """

import os, sys, signal, time, stat, logging
from threading import Thread
from definitions import *

# lkk
import datetime

class ReplayScript:
    def __init__(self, scriptName):
        self.commands = []
        self.exitObservers = []
        self.pointer = 0
        self.name = scriptName
        if not os.path.isfile(scriptName):
            raise UseCaseScriptError, "Cannot replay script " + repr(scriptName) + ", no such file or directory."
        for line in open(scriptName).xreadlines():
            line = line.strip()
            if line != "" and line[0] != "#":
                self.commands.append(line)

    def addExitObserver(self, observer):
        self.exitObservers.append(observer)

    def getShortcutName(self):
        return os.path.basename(self.name).split(".")[0].replace("_", " ").replace("#", "_")

    def getCommand(self, name=""):
        if self.pointer >= len(self.commands):
            if len(name) == 0:
                # reset the script and notify exit only if we weren't trying for a specific command
                self.pointer = 0
                for observer in self.exitObservers:
                    observer.notifyExit()
        else:
            nextCommand = self.commands[self.pointer]
            if len(name) == 0 or nextCommand.startswith(name):
                # Filter blank lines and comments
                self.pointer += 1
                return nextCommand        

    def getCommands(self):
        command = self.getCommand()
        if not command:
            return []

        # Process application events together with the previous command so the log comes out sensibly...
        waitCommand = self.getCommand(waitCommandName)
        if waitCommand:
            return [ command, waitCommand ]
        else:
            return [ command ]
        
    
class UseCaseReplayer:
    def __init__(self):
        self.logger = logging.getLogger("usecase replay log")
        self.scripts = []
        self.events = {}
        self.waitingForEvents = []
        self.applicationEventNames = []
        self.replayThread = None
        self.timeDelayNextCommand = 0
        # lkk
        self.previous_event_emit_time = None
        replayScript = os.getenv("USECASE_REPLAY_SCRIPT")
        if os.name == "posix":
            os.setpgrp() # Makes it easier to kill subprocesses
        if replayScript:
            self.addScript(ReplayScript(replayScript))
    
    def isActive(self):
        return len(self.scripts) > 0
    
    def addEvent(self, event):
        self.events[event.name] = event
    
    def addScript(self, script):
        self.scripts.append(script)
        waitCommand = script.getCommand(waitCommandName)
        if waitCommand:
            self.processWait(self.getArgument(waitCommand, waitCommandName))
        else:
            self.enableReading()
        
    def enableReading(self):
        # By default, we create a separate thread for background execution
        # GUIs will want to do this as idle handlers
        self.replayThread = Thread(target=self.runCommands)
        self.replayThread.start()
        #gtk.idle_add(method)

    def registerApplicationEvent(self, eventName, timeDelay):
        self.applicationEventNames.append(eventName)
        self.logger.debug("Replayer got application event " + repr(eventName))
        self.timeDelayNextCommand = timeDelay
        if self.waitingCompleted():
            if self.replayThread:
                self.replayThread.join()
            for eventName in self.waitingForEvents:
                self.applicationEventNames.remove(eventName)
            self.enableReading()
            
    def applicationEventRename(self, oldName, newName):
        toRename = filter(lambda eventName: oldName in eventName and newName not in eventName,
                          self.applicationEventNames)
        self.logger.debug("Renaming events " + repr(oldName) + " to " + repr(newName))
        for eventName in toRename:
            self.applicationEventNames.remove(eventName)
            newEventName = eventName.replace(oldName, newName)
            self.registerApplicationEvent(newEventName, timeDelay=0)
        self.logger.debug("Finished renaming")

    def waitingCompleted(self):
        if len(self.waitingForEvents) == 0:
            return False
        for eventName in self.waitingForEvents:
            if not eventName in self.applicationEventNames:
                return False
        return True

    def runCommands(self):
        while self.runNextCommand():
            pass

    def getCommands(self):
        nextCommands = self.scripts[-1].getCommands()
        if len(nextCommands) > 0:
            return nextCommands

        del self.scripts[-1]
        if len(self.scripts) > 0:
            return self.getCommands()
        else:
            return []
        
    def runNextCommand(self):
        if len(self.waitingForEvents):
            self.write("")
        for eventName in self.waitingForEvents:
            self.write("Expected application event '" + eventName + "' occurred, proceeding.")
        self.waitingForEvents = []
        if self.timeDelayNextCommand:
            self.logger.debug("Sleeping for " + repr(self.timeDelayNextCommand) + " seconds...")
            time.sleep(self.timeDelayNextCommand)
            self.timeDelayNextCommand = 0
        commands = self.getCommands()
        if len(commands) == 0:
            return False
        for command in commands:
            try:
                commandName, argumentString = self.parseCommand(command)
                self.logger.debug("About to perform " + repr(commandName) + " with arguments " + repr(argumentString))
                if commandName == waitCommandName:
                    if not self.processWait(argumentString):
                        return False
                else:
                    self.processCommand(commandName, argumentString)
            except UseCaseScriptError:
                type, value, traceback = sys.exc_info()
                self.write("ERROR: " + str(value))
            # We don't terminate scripts if they contain errors
        return True
    
    def write(self, line):
        try:
            self.logger.info(line)
        except IOError: # pragma: no cover - not easy to reproduce this
            # Can get interrupted system call here as it tries to close the file
            # This isn't worth crashing over!
            pass

    def processCommand(self, commandName, argumentString):
        if commandName == signalCommandName:
            self.processSignalCommand(argumentString)
        else:
            event = self.events[commandName]
            
            # lkk
            # Emit simulated timed events at the speed with which they were recorded.
            # Delay until the real elapsed time between timed event emissions is at least the delta between their recorded times.
            # Note that untimed events proceed as quickly as possible (as quickly as the replayer and the app can run.)
            # Note that any earlier sleep for any slow-motion PROBABLY means a timed event is already late.
            event_time = event.isTimed(argumentString)
            if event_time:  # is a timed event
              if self.previous_event_emit_time:  # at least one timed event emitted already
                real_delta = datetime.datetime.now() - self.previous_event_emit_time
                # Convert to milliseconds, the unit used by GTK events
                real_delta_msec = (real_delta.days * 24 * 3600 + real_delta.seconds) * 1000 + real_delta.microseconds / 1000.0
                simulated_delta_msec = event_time - self.previous_event_simulated_time
                msec_to_sleep = simulated_delta_msec - real_delta_msec # both ints of msec units
                if msec_to_sleep > 0:
                  # Convert to seconds and sleep.  Note sleep takes a fractional float.
                  time.sleep(msec_to_sleep / 1000.0)
                # else replay time is later than recorded time already
              self.previous_event_emit_time = datetime.datetime.now()
              self.previous_event_simulated_time = event_time
              
            self.write("")
            self.write("'" + commandName + "' event created with arguments '" + argumentString + "'")
            event.generate(argumentString)
            
    def parseCommand(self, scriptCommand):
        commandName = self.findCommandName(scriptCommand)
        if not commandName:
            raise UseCaseScriptError, "Could not parse script command '" + scriptCommand + "'"
        argumentString = self.getArgument(scriptCommand, commandName)
        return commandName, argumentString

    def getArgument(self, scriptCommand, commandName):
        return scriptCommand.replace(commandName, "").strip()

    def findCommandName(self, command):
        if command.startswith(waitCommandName):
            return waitCommandName
        if command.startswith(signalCommandName):
            return signalCommandName

        longestEventName = ""
        for eventName in self.events.keys():
            if command.startswith(eventName) and len(eventName) > len(longestEventName):
                longestEventName = eventName
        return longestEventName            
    
    def processWait(self, applicationEventStr):
        allHappened = True
        self.write("") # blank line
        for applicationEventName in applicationEventStr.split(", "):
            self.write("Waiting for application event '" + applicationEventName + "' to occur.")
            if applicationEventName in self.applicationEventNames:
                self.write("Expected application event '" + applicationEventName + "' occurred, proceeding.")
                self.applicationEventNames.remove(applicationEventName)
            else:
                self.waitingForEvents.append(applicationEventName)
                allHappened = False
        return allHappened

    def processSignalCommand(self, signalArg):
        signalNum = getattr(signal, signalArg)
        self.write("")
        self.write("Generating signal " + signalArg)
        os.killpg(os.getpgid(0), signalNum) # So we can generate signals for ourselves...
        self.logger.debug("Signal " + signalArg + " has been sent")


