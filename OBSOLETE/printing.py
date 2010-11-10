#!/usr/bin/env python

# TODO Obsolete see viewport.py

import gtk

settings = None


def do_print(port):
  # print_op is ephemeral 
  print_op = gtk.PrintOperation()

  global settings
  if settings != None: 
    print_op.set_print_settings(settings)

  print_op.connect("begin_print", port.begin_print)
  print_op.connect("draw_page", port.draw_page)

 
  # Second parameter is the parent widget of the print dialog.
  # Here None means top level, ie not a child of the app window or viewport.
  # viewport.surface did not work.
  res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)
  
  # Signals are emitted here at the conclusion of the print dialog

  if res == gtk.PRINT_OPERATION_RESULT_APPLY:
      settings = print_op.get_print_settings()

