'''
Build control instances for the app.
'''

'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
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
document_handle_menu = None
bkgd_control = None
document_menu = None


def build_all(a_printerport, a_fileport):
  global document_menu
  
  # Menu items
  build_traditional_items(a_printerport, a_fileport)
  
  # Context menus of traditional menu style
  edit_menu = build_edit_menu(a_printerport, a_fileport)
  document_menu = build_document_menu(a_printerport, a_fileport)
  resize_menu = build_dummy_menu(resize_mi)
  draw_menu = build_dummy_menu(draw_mi)

  # Handle menu type
  global handle_menu
  handle_menu = build_handle_menu(edit_menu, resize_menu, draw_menu)
  global document_handle_menu
  document_handle_menu = build_document_handle_menu(edit_menu, resize_menu, draw_menu)

  # Control for the document, the background
  global bkgd_control
  bkgd_control = gui.backgroundcontrol.BackgroundControl(a_printerport, a_fileport)
  # Controls self?? bkgd_control.set_controlee(document)
  

def build_traditional_items(printerport, fileport):
  '''
  Menu items represent functionality.
  Their functionality (commands) can be in many menus,
  but items themselves must be in only one menu,
  since items call on their unique parent.
  TODO: arranged by preference or dynamically?
  '''
  # menu_item = gui.itemmenu.IconMenuItem( command.NULL_COMMAND )
  global save_mi, print_mi
  global cut_mi, copy_mi, paste_mi
  global doc_cut_mi, doc_copy_mi, doc_paste_mi
  global resize_mi, draw_mi
  
  save_mi = gui.itemmenu.TextMenuItem("Save", command.Command(fileport.do_save))
  print_mi = gui.itemmenu.TextMenuItem("Print", command.Command(printerport.do_print))
  
  # TODO share commands
  cut_mi = gui.itemmenu.TextMenuItem("Cut", command.Command(edit.do_cut))
  copy_mi = gui.itemmenu.TextMenuItem("Copy", command.Command(edit.do_copy))
  paste_mi = gui.itemmenu.TextMenuItem("Paste", command.Command(edit.do_paste))
  
  doc_cut_mi = gui.itemmenu.TextMenuItem("Cut", command.Command(edit.do_cut))
  doc_copy_mi = gui.itemmenu.TextMenuItem("Copy", command.Command(edit.do_copy))
  doc_paste_mi = gui.itemmenu.TextMenuItem("Paste", command.Command(edit.do_paste))
  
  resize_mi = gui.itemmenu.TextMenuItem("Resize TODO", command.NULL_COMMAND)
  draw_mi = gui.itemmenu.TextMenuItem("Draw TODO", command.NULL_COMMAND)


def build_handle_menu(edit_menu, resize_menu, draw_menu):
  '''
  Handle menu that pops up on edges of graphic symbols (morphs.)
  It tracks the pointer along an edge.
  Each has a RMB popup menu.
  '''
  handle_group = gui.menuhandle.TrackingHandleGroup("MorphHandle")
  
  handle_control = gui.itemhandlecoords.ResizeHandleItem(resize_menu)
  handle_group.add(handle_control)
  handle_control = gui.itemhandlecoords.MoveHandleItem(edit_menu)
  handle_group.add(handle_control)
  handle_control = gui.itemhandleline.DrawHandleItem(draw_menu)
  handle_group.add(handle_control)
  
  return handle_group
  

def build_document_handle_menu(edit_menu, resize_menu, draw_menu):
  '''
  Handle menu that pops up in background (on the document.)
  It does not track.
  Each item has a RMB popup menu.
  '''
  handle_group = gui.menuhandle.StationedHandleGroup("DocumentHandle")
  
  handle_control = gui.itemhandlecoords.ResizeHandleItem(resize_menu)
  handle_group.add(handle_control)
  # Move item on document has different RMB context menu than on morph
  handle_control = gui.itemhandlecoords.MoveHandleItem(document_menu)
  handle_group.add(handle_control)
  handle_control = gui.itemhandleline.DrawHandleItem(draw_menu)
  handle_group.add(handle_control)
  
  return handle_group


def build_document_menu(printerport, fileport):
  '''
  Classic style pop-up menu
  '''
  menu_group = gui.menutraditional.MenuGroup("Document")
  menu_group.add(doc_cut_mi)
  menu_group.add(doc_copy_mi)
  menu_group.add(doc_paste_mi)
  # TODO separator
  menu_group.add(save_mi)
  menu_group.add(print_mi)
  return menu_group
  

def build_edit_menu(printerport, fileport):
  '''
  Build context menu (RMB) for morphs.
  Style: Classic pop-up menu
  '''
  menu_group = gui.menutraditional.MenuGroup("Edit")
  menu_group.add(cut_mi)
  menu_group.add(copy_mi)
  menu_group.add(paste_mi)
  return menu_group
  
  
def build_dummy_menu(item):
  menu_group = gui.menutraditional.MenuGroup("Dummy")
  menu_group.add(item)
  return menu_group
  

