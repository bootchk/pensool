#!/usr/bin/env python

'''
Main of drawing app
'''

import gtk
from gtk import gdk

import viewport
import drawable
import morph.morph
import morph.textmorph
import controlinstances
import guicontrolmgr
import gui.backgroundcontrol
import coordinates
import scheme




'''
TODO
file input using rsvg
'''

'''
def draw_background(self, acv, dw, x, y, ww, hh, pb):
   gc = dw.new_gc()
   pw = pb.get_width()
   ph = pb.get_height()
   offset_x = x % pw
   offset_y = y % ph
   dw_y = -offset_y
   while dw_y < hh:
       dw_x = -offset_x
       while dw_x < ww:
           dw.draw_pixbuf(gc, pb, 0, 0, dw_x, dw_y)
           dw_x += pw
       dw_y += ph
 '''




# window 
window = gtk.Window()
window.resize(400, 400) # TODO this resizes the surface and viewport?
window.move(400, 600)
window.connect('destroy', gtk.main_quit)
window.realize()

# load graphic
# pb = gdk.pixbuf_new_from_file('ufo-input.png')
#w, h = pb.get_width(), pb.get_height()

da = gtk.DrawingArea()

'''
This must precede realization of viewport? or use add_events().
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
Without this, the drawing area widget does not receive keyboard events:
focus_in, key_release, etc.
We are implementing our own widgets (controls) including text controls
that will receive keyboard.
Also, we implement our own *traversal* (via the tab key per convention)
among our controls that get the keyboard focus.
'''
da.set_flags( da.flags() | gtk.CAN_FOCUS )
  
window.add(da)

# Can draw to several ports.
a_viewport = viewport.ViewPort(da)
a_printerport = viewport.PrinterPort()
a_fileport = viewport.FilePort()

# Show so allocation becomes valid
window.show_all()


# The document, IE model.
''' morphs
Initial: load from file.
TODO
'''
scheme.initialize(a_viewport)

"""
# Make separate morphs
arect = morph.morph.RectMorph(a_viewport)
acirc = morph.morph.CircleMorph(a_viewport)

scheme.glyphs.append(arect)
scheme.glyphs.append(acirc)
for item in scheme.glyphs:
  item.set_dimensions(coordinates.dimensions(150, 150, 100, 100))
"""
# !!! Width, height of text are computed??
# atext.set_origin(coordinates.dimensions(150, 30, 0,0))
# TextMorph creates it's own selection
atext = morph.textmorph.TextMorph(a_viewport)
atext.set_dimensions(coordinates.dimensions(150, 30, 1, 1))
scheme.glyphs.append(atext)

"""
# Make a group
arect = morph.morph.RectMorph(a_viewport)
arect.set_dimensions(coordinates.dimensions(50, 50, 50, 50))
acirc = morph.morph.CircleMorph(a_viewport)
acirc.set_dimensions(coordinates.dimensions(0, 0, 50, 50))

agroup = morph.morph.Morph(a_viewport)
agroup.append(arect)
agroup.append(acirc)
# Group at 30,30, scale 1
agroup.set_dimensions(coordinates.dimensions(30,30,1,1))
# agroup.append(atext)

scheme.glyphs.append(agroup)
"""


''' 
Controls.
Build singletons (one instance) for each control type.
Exactly one control instance is active (has focus) at a time.
'''

# Enforces one control active
guicontrolmgr.control_manager = guicontrolmgr.ControlsManager(a_viewport)

# Handle menu type
handle_menu = controlinstances.build_handle_menu(a_viewport)

# Traditional menu type
popup_menu = controlinstances.build_popup_menu(a_viewport)

# Control for the document, the background
bkgd_control = gui.backgroundcontrol.BackgroundManager(
  handle_menu, popup_menu,
  a_viewport, a_printerport, a_fileport)
bkgd_control.dimensions = da.allocation
# Controls self?? bkgd_control.set_controlee(document)

guicontrolmgr.control_manager.set_root_control(bkgd_control)


'''
Initial active control is the background manager
None event is activating it.
Controlee is the bkgd_control itself.
'''
guicontrolmgr.control_manager.activate_control(bkgd_control, None, bkgd_control)

a_viewport.set_model(scheme.glyphs)
a_printerport.set_model(scheme.glyphs)
a_fileport.set_model(scheme.glyphs)

gtk.main()

