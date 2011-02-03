#!/usr/bin/env python

'''
Builds controls for the app.
'''

import gui.menutraditional
import gui.menuhandle
import gui.itemmenu
import gui.itemhandleline
import gui.itemhandlecoords
import base.command as command
import clipboard
import edit

def build_handle_menu(viewport, edit_menu):
  '''
  Handle menu that pops up on edges of graphics.
  '''
  handle_group = gui.menuhandle.HandleGroup(viewport)
  handle_control = gui.itemhandleline.LineHandleItem(viewport,
    command.NULL_COMMAND )
  handle_group.add(handle_control)
  handle_control = gui.itemhandlecoords.MoveHandleItem(viewport,
    command.Command(edit_menu.open))
  handle_group.add(handle_control)
  handle_control = gui.itemhandlecoords.ResizeHandleItem(viewport,
    command.NULL_COMMAND )
  handle_group.add(handle_control)
  return handle_group
  

def build_popup_menu(viewport, printerport, fileport):
  '''
  Classic style pop-up menu
  '''
  menu_item = gui.itemmenu.IconMenuItem(viewport,
    command.NULL_COMMAND )
  menu_item2 = gui.itemmenu.IconMenuItem(viewport,
    command.NULL_COMMAND )
  menu_item3 = gui.itemmenu.TextMenuItem(viewport, "Save", 
    command.Command(fileport.do_save))
  menu_item4 = gui.itemmenu.TextMenuItem(viewport, "Print", 
    command.Command(printerport.do_print))
  
  menu_group = gui.menutraditional.MenuGroup(viewport)
  menu_group.add(menu_item)
  menu_group.add(menu_item2)
  menu_group.add(menu_item3)
  menu_group.add(menu_item4)
  return menu_group
  

def build_edit_menu(viewport, printerport, fileport):
  '''
  Build context menu (RMB) for morphs.
  Style: Classic pop-up menu
  '''
  menu_item = gui.itemmenu.TextMenuItem(viewport, "Cut", 
    command.Command(fileport.do_save))
  menu_item2 = gui.itemmenu.TextMenuItem(viewport, "Copy", 
    command.Command(edit.do_copy))
  menu_item3 = gui.itemmenu.TextMenuItem(viewport, "Paste", 
    command.Command(edit.do_paste))
  '''menu_item4 = gui.itemmenu.TextMenuItem(viewport, "Print", 
    command.Command(printerport.do_print))
  '''
  
  menu_group = gui.menutraditional.MenuGroup(viewport)
  menu_group.add(menu_item)
  menu_group.add(menu_item2)
  menu_group.add(menu_item3)
  # menu_group.add(menu_item4)
  return menu_group

