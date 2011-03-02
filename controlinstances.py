#!/usr/bin/env python

'''
Builds controls for the app.
'''

import gui.menutraditional
import gui.menuhandle
import gui.itemmenu
import gui.itemhandleline
import gui.itemhandlecoords
import gui.backgroundcontrol
import base.command as command
import edit

handle_menu = None
bkgd_control = None
document_menu = None

def build_all(a_printerport, a_fileport):
  global document_menu
  
  # Menu items
  build_traditional_items(a_printerport, a_fileport)
  
  # Context menus of traditional menu style
  edit_menu = build_edit_menu(a_printerport, a_fileport)
  document_menu = build_document_menu(a_printerport, a_fileport)

  # Handle menu type
  global handle_menu
  handle_menu = build_handle_menu(edit_menu)

  # Control for the document, the background
  global bkgd_control
  bkgd_control = gui.backgroundcontrol.BackgroundControl(a_printerport, a_fileport)
  # Controls self?? bkgd_control.set_controlee(document)
  

def build_traditional_items(printerport, fileport):
  '''
  Menu items represent functionality.
  They can be in many menus, or arranged by preference or dynamically.
  '''
  # menu_item = gui.itemmenu.IconMenuItem( command.NULL_COMMAND )
  global save_mi, print_mi
  global cut_mi, copy_mi, paste_mi
  
  save_mi = gui.itemmenu.TextMenuItem("Save", command.Command(fileport.do_save))
  print_mi = gui.itemmenu.TextMenuItem("Print", command.Command(printerport.do_print))
  
  cut_mi = gui.itemmenu.TextMenuItem("Cut", command.Command(edit.do_cut))
  copy_mi = gui.itemmenu.TextMenuItem("Copy", command.Command(edit.do_copy))
  paste_mi = gui.itemmenu.TextMenuItem("Paste", command.Command(edit.do_paste))
  
  
def build_handle_menu(edit_menu):
  '''
  Handle menu that pops up on edges of graphics.
  '''
  handle_group = gui.menuhandle.HandleGroup()
  
  handle_control = gui.itemhandlecoords.ResizeHandleItem( command.NULL_COMMAND )
  handle_group.add(handle_control)
  handle_control = gui.itemhandlecoords.MoveHandleItem( command.Command(edit_menu.open))
  handle_group.add(handle_control)
  handle_control = gui.itemhandleline.DrawHandleItem( command.NULL_COMMAND )  # FIXME
  handle_group.add(handle_control)
  
  return handle_group
  

def build_document_menu(printerport, fileport):
  '''
  Classic style pop-up menu
  '''
  menu_group = gui.menutraditional.MenuGroup()
  menu_group.add(cut_mi)
  menu_group.add(copy_mi)
  menu_group.add(paste_mi)
  # TODO separator
  menu_group.add(save_mi)
  menu_group.add(print_mi)
  return menu_group
  

def build_edit_menu(printerport, fileport):
  '''
  Build context menu (RMB) for morphs.
  Style: Classic pop-up menu
  '''
  menu_group = gui.menutraditional.MenuGroup()
  menu_group.add(cut_mi)
  menu_group.add(copy_mi)
  menu_group.add(paste_mi)
  return menu_group

