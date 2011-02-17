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

def build_handle_menu(edit_menu):
  '''
  Handle menu that pops up on edges of graphics.
  '''
  handle_group = gui.menuhandle.HandleGroup()
  handle_control = gui.itemhandleline.LineHandleItem( command.NULL_COMMAND )
  handle_group.add(handle_control)
  handle_control = gui.itemhandlecoords.MoveHandleItem( command.Command(edit_menu.open))
  handle_group.add(handle_control)
  handle_control = gui.itemhandlecoords.ResizeHandleItem( command.NULL_COMMAND )
  handle_group.add(handle_control)
  return handle_group
  

def build_popup_menu(printerport, fileport):
  '''
  Classic style pop-up menu
  '''
  menu_item = gui.itemmenu.IconMenuItem( command.NULL_COMMAND )
  menu_item2 = gui.itemmenu.IconMenuItem( command.NULL_COMMAND )
  menu_item3 = gui.itemmenu.TextMenuItem("Save", command.Command(fileport.do_save))
  menu_item4 = gui.itemmenu.TextMenuItem("Print", command.Command(printerport.do_print))
  
  menu_group = gui.menutraditional.MenuGroup()
  menu_group.add(menu_item)
  menu_group.add(menu_item2)
  menu_group.add(menu_item3)
  menu_group.add(menu_item4)
  return menu_group
  

def build_edit_menu(printerport, fileport):
  '''
  Build context menu (RMB) for morphs.
  Style: Classic pop-up menu
  '''
  menu_item = gui.itemmenu.TextMenuItem("Cut", command.Command(edit.do_cut))
  menu_item2 = gui.itemmenu.TextMenuItem("Copy", command.Command(edit.do_copy))
  menu_item3 = gui.itemmenu.TextMenuItem("Paste", command.Command(edit.do_paste))
  '''menu_item4 = gui.itemmenu.TextMenuItem("Print", 
    command.Command(printerport.do_print))
    fileport.do_save
  '''
  
  menu_group = gui.menutraditional.MenuGroup()
  menu_group.add(menu_item)
  menu_group.add(menu_item2)
  menu_group.add(menu_item3)
  # menu_group.add(menu_item4)
  return menu_group

