#!/usr/bin/env python

'''
Items in a handle menu.
'''

import gui.itemcontrol
import coordinates
import dropmanager
from decorators import *


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
  These are all
  filtered events from superclass GuiControl.
  '''
  
  @dump_event
  def button_press_left(self, event):
    '''
    Mouse button pressed inside.
    This defines that handle items are draggable.
    '''
    # TODO drag any button?
    # TODO drag 3 pixels first ie distinguish drag from click
    assert(not self.is_dragging)
    self.is_dragging = True
    self.start_drag(event)


  @dump_event
  def start_drag(self, event):
    '''
    Mouse departed item with button down.
    Start drag with:
      event
      controlee is the drawable controlled by this control
      source is self control
    '''
    dropmanager.dropmgr.begin(event, self.controlee, self)
 
    
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
    if pixels_off_axis > MOUSE_OFF_AXIS_PIXELS \
      or pixels_off_axis < -MOUSE_OFF_AXIS_PIXELS:
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
    # Calculate the vector of mouse exit.
    center = coordinates.center_of_dimensions(self.get_dimensions())
    exit_vector = coordinates.vector_from_points(center, event)
    # Tell manager, let the manager figure out if
    # the vector is in the next or previous direction.
    self.group_manager.do_item_exit(event, exit_vector)
    return
    
    """
    # OLD
    
    bounds = self.get_bounds()
    # If exited forward or backward
    if event.x <= bounds.x:
      # the *next* exit side
      self.group_manager.next(event)
    else:
      # the *previous* exit side
      self.group_manager.previous(event)
    """
  
  
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
  
  def anti_orthogonal(self, event):
    '''
    Return coords projected onto a line orthogonal to axis.
    Event is unchanged.
    FIXME clarify name
    '''
    """
    Dummy, sorta works for horizonatal menu.
    # ie, y is the y of the event, x is the current x
    # return coordinates.dimensions(self.get_center().x, event.y, 0, 0)
    """
    return foo
  
  
  @dump_return
  def pixels_off_menu_axis(self, event):
    '''
    Is mouse motion orthogonal (sideways) to menu axis?
    Returns count of pixels off axis.
    !!! Note that the sign indicates left(countercw) or right (clockwise)
    of the menu axis, not a direction along the coordinate system.
    '''
    """
    Dummy that sorta works for horizontal menus.
    # return not event.y == self.get_center().y
    """
    # vector from menu origin to mouse event
    menu_vector = self.group_manager.layout_vector
    menu_origin = self.group_manager.get_origin()
    mouse_vector = coordinates.vector_from_points(menu_origin, event)
    # normalize to menu vector
    normal_vector = coordinates.normalize_vector_to_vector(mouse_vector, 
      menu_vector)
    return normal_vector.y
  
  
