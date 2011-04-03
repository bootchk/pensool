#!/usr/bin/env python

'''
Main of Pensool 2D drawing app.
'''
'''

Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pensool is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pensool.  If not, see <http://www.gnu.org/licenses/>.
'''

import gtk
from gtk import gdk

# For logging
import os
import os.path
import logging
import logging.config

import morph.morph
import morph.textmorph
import controlinstances
import gui.manager.control
import gui.backgroundcontrol
import port
import config
import scheme

# comment this out if you prefer stderr for exceptions
import share.gui_gtkexcepthook  # show dialog on exception

import collections
Rectangle = collections.namedtuple('Rectangle', 'x y width height')


# Find the path to logging config file via env var.
# Typically "logging.pensool" in the tmp directory which is the sandbox of Texttest
try:
  log_config_path = os.environ['LOG_CONF_PATH']
except Exception as detail:
  print "Could not read env var, looking for logging config in pwd", detail
  log_config_path = "logging.pensool" # try in pwd
try:
  logging.config.fileConfig(log_config_path)
except Exception as detail:
  print "Could not configure logging from file, default to WARNINGs to stdout", detail
  logging.basicConfig(level=logging.WARNING)
  
# create logger as configured by file
mylogger = logging.getLogger("pensool")


  
def main():
  # window 
  window = gtk.Window()
  window.resize(400, 400) # TODO this resizes the surface and view?
  window.move(400, 600)
  window.connect('destroy', gtk.main_quit)
  window.realize()
  
  da = gtk.DrawingArea()

  '''
  This must precede realization of view? or use add_events().
  First three are mouse events.
  STRUCTURE is configure-event (resizing the window)
  Last are focus and keyboard events.
  '''
  da.set_events( \
    gdk.BUTTON_PRESS_MASK \
    | gdk.POINTER_MOTION_MASK \
    | gdk.BUTTON_RELEASE_MASK \
    | gdk.STRUCTURE_MASK \
    | gdk.FOCUS_CHANGE_MASK\
    | gdk.KEY_RELEASE_MASK \
    | gdk.KEY_PRESS_MASK )
   
  '''
  Enable drawing area widget to receive keyboard events: focus_in, key_release, etc.
  We implement our own widgets (controls) including text controls that receive keyboard.
  Also, we implement our own *traversal* (via the tab key per convention)
  among our controls that get the keyboard focus.
  '''
  da.set_flags( da.flags() | gtk.CAN_FOCUS )
    
  window.add(da)

  # Can draw to several ports.
  a_view = port.ViewPort(da)
  a_printerport = port.PrinterPort()
  a_fileport = port.FilePort()

  # global singletons
  config.viewport = a_view  
  config.scheme = scheme.Scheme() 

  window.show_all() # Show now so allocation becomes valid
  
  gui.manager.control.control_manager = gui.manager.control.ControlsManager() # Enforces one control active
  controlinstances.build_all(a_printerport, a_fileport) # build singleton controls
  gui.manager.control.control_manager.set_root_control(controlinstances.bkgd_control)

  # Initial active control is the background manager. Controlee is the bkgd_control itself.
  gui.manager.control.control_manager.activate_control(controlinstances.bkgd_control, controlinstances.bkgd_control)

  a_view.set_model(config.scheme.model)
  a_printerport.set_model(config.scheme.model)
  a_fileport.set_model(config.scheme.model)
  
  make_test_doc()
  
  gtk.main()


def make_test_doc():
  ''' TODO document (model) load from file.
  '''
  # Make separate morphs
  arect = morph.morph.RectMorph()
  acirc = morph.morph.CircleMorph()
  apoint = morph.morph.PointMorph()
  aline = morph.morph.LineMorph()

  config.scheme.model.append(arect)
  config.scheme.model.append(acirc)
  config.scheme.model.append(apoint)
  config.scheme.model.append(aline)
  for item in config.scheme.model:
    item.set_dimensions(Rectangle(150.0/config.PENSOOL_UNIT, 150.0/config.PENSOOL_UNIT, 100.0/config.PENSOOL_UNIT, 100.0/config.PENSOOL_UNIT))
  apoint.set_dimensions(Rectangle(10.0/config.PENSOOL_UNIT, 50.0/config.PENSOOL_UNIT, 100.0/config.PENSOOL_UNIT, 100.0/config.PENSOOL_UNIT))
  aline.set_dimensions(Rectangle(20.0/config.PENSOOL_UNIT, 50.0/config.PENSOOL_UNIT, 100.0/config.PENSOOL_UNIT, 100.0/config.PENSOOL_UNIT))
    

  # !!! Width, height of text are computed??
  # atext.set_origin(Rectangle(150.0/config.PENSOOL_UNIT, 30.0/config.PENSOOL_UNIT, 0,0))
  # TextEditMorph creates it's own selection
  atext = morph.textmorph.TextEditMorph("Most relationships seem so transitory")
  atext.set_dimensions(Rectangle(150.0/config.PENSOOL_UNIT, 30.0/config.PENSOOL_UNIT, 200.0/config.PENSOOL_UNIT, 200.0/config.PENSOOL_UNIT))
  config.scheme.model.append(atext)

  """
  # Make a group
  arect = morph.morph.RectMorph()
  arect.set_dimensions(Rectangle(50.0/config.PENSOOL_UNIT, 50, 50, 50))
  acirc = morph.morph.CircleMorph()
  acirc.set_dimensions(Rectangle(0, 0, 50, 50))

  agroup = morph.morph.Morph()
  agroup.append(arect)
  agroup.append(acirc)
  # Group at 30,30, scale 1
  agroup.set_dimensions(Rectangle(30,30,1,1))
  # agroup.append(atext)

  config.scheme.model.append(agroup)
  """

  

if __name__ == "__main__":
  main()

