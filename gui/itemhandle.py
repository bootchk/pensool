#!/usr/bin/env python

'''
Items in a handle menu.
'''

import gui.itemcontrol
import gui.manager.drop
from decorators import *
import base.vector as vector


# Count pixels mouse must leave axis before menu slides
# Prevents jitter
# TODO use one constant for all jitter prevention
MOUSE_OFF_AXIS_PIXELS = 2



class HandleItem(gui.itemcontrol.ItemControl):
  '''
  A handle control:
    -appears on the edge of a controlee
    -mouseover appearance and dissappearance, without a click
    -not usually clickable (drag is preferred) ???
    -tracks mouse: moveable along the path of its controlee (without a button press)
    -starts drag (after a press)
  
  Singleton subclasses with different look and behavior:
    on end drag
    on scroll
  '''


  '''
  Filtered events from superclass GuiControl.
  '''
  
  @dump_event
  def button_press_left(self, event):
    '''
    LMB pressed inside handle item.
    Handle items enact drag on LMB.
    '''
    # TODO drag any button?
    # TODO drag 3 pixels first ie distinguish drag from click
    self.start_drag(event)

  @dump_event
  def button_press_right(self, event):
    '''
    RMB pressed inside handle item.
    Handle items enact context menu on RMB.
    '''
    print "Handle context menu"
    # Close the open handle menu.
    # The drag for the context menu takes the mouse away from the morph.
    self.group_manager.close(event)
    # Note focus is not changed if a context menu is opened.
    # Open context menu on controlee
    ## control_instances.edit_menu.open(event, self.controlee)
    # More generally, execute command
    # where the command is to open another menu
    # but this command is not undoable?
    # self.command(event, self.controlee)
    
    # For now, do nothing except...
    gui.manager.control.control_manager.activate_root_control()
    
    
  @dump_event
  def start_drag(self, event):
    ''' Mouse departed item with button down. '''
    self.group_manager.close(event)  # close menu
    # Remain focused on operand morph while dragging?
    gui.manager.control.control_mgr.activate_root_control() # backgroundmgr
    gui.manager.drop.dropmgr.begin(event, self.controlee, self)
    # After this, events go to backgroundmgr, passed to dragee.continue_drag()
  
    
  @dump_event
  def mouse_move(self, event):
    '''
    Mouse moved inside this control.
    This defines that items decide how a handle menu behaves:
    can slide orthogonally, or next/previous item anti-orthogonal.
    '''
    # if orthogonal, move the menu ( the *control* group)
    pixels_off_axis = self.pixels_off_menu_axis(event)
    # allow for jitter
    # TODO isolate this
    if abs(pixels_off_axis) > MOUSE_OFF_AXIS_PIXELS :
      # Layout my whole group, which will redraw this item
      self.group_manager.slide(pixels_off_axis)
    else:
      # moving along (parallel to) menu towards next item and mouse_exit
      pass
  
  
  @dump_event
  def mouse_exit(self, event):
    '''
    Mouse exited item.
    This is a filtered event from super GuiControl.
    Assert no button down (not a drag.)
    
    Dynamic orthogonality.
    Since a handle menu follows the mouse in orthogonal directions,
    this must mean mouse moved in axial *exit* direction.
    '''
    # Calculate vector in DCS of mouse exit.
    center = self.bounds.center_of()
    exit_vector = vector.Point(event.x, event.y) - center
    
    # Tell manager, let the manager figure out if
    # the vector is in the next or previous direction in seq of items.
    self.group_manager.do_item_exit(event, exit_vector)
    return
    
  def control_key_release(self, event):
    print "Control key released in handle item"
  
  def bland_key_release(self, event):
    print "Bland key released in handle item"
    # FIXME for the move item, if this is text box, take key
  
  '''
  Virtual: should be overridden
  '''
  # TODO @virtual
  @dump_event
  def scroll_down(self, event):
    '''
    Filtered event from GuiControl: scroll wheel down in an item.
    '''
    print "??????Virtual scroll down"
  
  
  '''
  Utility routines for deciding the alignment of the menu.
  '''
  
  
  # @dump_return
  def pixels_off_menu_axis(self, event):
    '''
    Is mouse motion orthogonal (sideways) to menu axis?
    Returns count of pixels off axis.
    !!! Note that the sign indicates left(countercw) or right (clockwise)
    of the menu axis, not a direction along the coordinate system.
    '''
    # Specific for horiz menus: return not event.y == self.get_center().y
 
    # vector from menu origin to mouse event
    menu_vector = self.group_manager.layout_spec.vector
    menu_benchmark = self.group_manager.layout_spec.benchmark
    mouse_vector = vector.Point(event.x, event.y) - menu_benchmark
    # normalize to menu vector
    normal_vector = vector.normalize_vector_to_vector(mouse_vector, 
      menu_vector)
    # print "mouse", mouse_vector, "menu", menu_vector, "normal", normal_vector
    return normal_vector.y
  
  
