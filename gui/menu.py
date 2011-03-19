#!/usr/bin/env python


'''
Managers of groups of controls.
Enforces a policy on the group.
Here the policy is for menus: one active item.
There is another manager that enforces a policy over the whole application.
'''

import logging

import compound
## import gui.manager.focus
import gui.manager.control
from decorators import *
import layout
import base.vector as vector
## import config

# FIXME
import gui.manager.textselect



# TODO abstract ControlGroup from Menu and HandleMenu and Dock

# TODO a single, ungrouped GuiControl

class ItemGroup(compound.Compound):
  '''
  A manager of a group of control items, e.g. group of menu items.
  Sequence and tree like aspects.
  
  Drawing behavior is inherited.
  Currently, drawing may invalidate more than is necessary.
  
  Menu behavior, knows:
    one item should be active and highlighted.
    items are GuiControls managed by GuiControlManager.
    layout of the items.
    highlight mouseover and sensitive items.
    which items are sensitive.
    
  !!! ItemGroup not is-a GuiControl but has-a
  !!! ItemGroup is-a Drawable
  
  A menu is ordered, thus next() and previous().
  The items themselves decide when they are exited, and call next and previous.
  
  A menu has items that can be added, thus add():
  
  A menu has one active item highlighted.
  
  The items of a menu have object controlees.
  The menu as a whole does not.
  Each item may control a different object.
  
  API:
    open(), close() from a manager
    add() creation time
    next(), previous() from items
    
  Menu subclasses differ in their layout.
  A layout_spec specifies a layout.
  Subclasses must implement:
    new_layout_spec()
    layout()
    
  For moveable menus, events change the layout_spec, then call layout().
  Moveable menus implement slide() or similar.
  
  An ItemGroup is laid out on a vector from an origin.
  Often, but not necessarily, linear along this vector.
  The origin is where the user clicked.
  '''
  
  def __init__(self, name):
    compound.Compound.__init__(self)
    self.active_index = 0
    '''
    !!! an ItemGroup has a controlee that initializes the controlees
    of its items.  Its items can later change themselves to other controlees.
    '''
    self.controlee = None
    self.layout_spec = layout.LayoutSpec()
    self.name = name
    

  #@dump_event
  def position(self):
    '''
    Position menu according to layout spec.
    Called on opening and on movement (slide.)
    # TODO Differ for subclasses.
    
    Position is a change to this menu's transform, translate and rotate.
    A menu group rotates and translates  the group of its items.
    
    Scaling: A menu is scaled by parent transform (the user-preference controls transform.)
    Rotation: A menu is layout'd along the X-axis, horizontally.
    A traditional menu is rotated to the vertical position.
    Handle menus are rotated to any angle.
    Translation: Most menus are also translated so that the center of some item is at
    the opening event.
    
    The layout spec embodies all the transforms, this is generic for all menu subclasses.
    This is view_altering, but caller must do view_altering
    '''
    unit_vect = vector.ONES.copy()  # unit scaling
    self.set_transform(self.layout_spec.benchmark, unit_vect, self.layout_spec.vector.angle())
    
    
  @view_altering
  @dump_event
  def open(self, event, controlee=None):
    '''
    Make visible at event coords.
    Put default item at event.
    '''
    logging.getLogger("pensool").debug("Open menu" + self.name)
    # Set new controlee, since new_layout_spec may use it.
    assert controlee is not None
    self.controlee = controlee
    
    self.new_layout_spec(event) # Set data for position and layout.
    self.position() # Set transform for menu group
    
    # A menu must layout at least when opened.
    # Some menu types can layout only at creation time.
    # Some menu types layout after open time.
    self.layout(event)  # FIXME is event needed
    
    gui.manager.control.control_manager.add_to_drawlist(self)
    
    # Make open menu display an active item.
    self.active_index = self.layout_spec.opening_item   # not necessarily first
    # !!! Pass the controlee to the items
    self._activate_current(event, controlee)
    self._highlight_current(event, True)
  
  
  def layout(self, event=None):
    ''' 
    Layout (position) all items in composite (group).
    
    Input is a self.layout_spec, which specifies position of the group.
    Should be relative positions of items.
    Event precipitated layout, but ordinarily should not be used in layout.
    '''
    raise RuntimeError( "Virtual method called: layout()" )
    
    
  @view_altering
  @dump_event
  def close(self, event):
    '''
    Close this menu.
    Note another menu may replace this one: caller must activate some
    next control, typically the background manager or another menu.
    Note that focus is not necessarily lost: caller must unfocus if appropriate.
    '''
    gui.manager.control.control_manager.remove_from_drawlist(self)
    ## gui.manager.focus.unfocus()  # any controlee, should invalidate
    # Deactivate current menu item, which is receiving events
    self._deactivate_current() # leaves no control active
    ## OLD automatically activates the background manager.
    # FIXME for now, deactivate text select when handle menu closes
    gui.manager.textselect.activate_select_for_text(False)
    
  
  # TODO this is duplicative: use parent attribute instead
  def add(self, item):
    ''' Append item.
    Overrides composite.append() make item reference its manager.
    '''
    self.append(item) # super ? list or composite
    item.set_group_manager(self)
  
  
  def do_item_exit(self, event, exit_vector):
    '''
    The mouse has exited an item in exit_vector.
    Do next or previous.
    (Next or previous might do open, or close.)
    
    !!! Note that handle menus slide sideways,
    should not get an exit orthogonal to the menu vector.
    FIXME make a handle menu slide around a corner
    and make the menu_vector change as the menu slides
    along a curve.
    '''
    vect = vector.normalize_vector_to_vector(exit_vector, self.layout_spec.vector)
    
    # Seems backwards, but since menu vector is opposite direction to layout,
    # inverse the sign
    if vect.x > 0 :  # Jan. 8
      self._change_item(event, 1)
    else :
      self._change_item(event, -1)
    #  TODO recode this without an if
    # direction = - ( rect.x/rect.x)  # TODO is the normal already unit vector?

   
  @dump_event
  def _change_item(self, event, direction):
    '''
    A menu item has detected mouse moving out of item 
    (without button down, i.e. not a drag)
    in direction (+1 or -1)
    Change to another menu item, or close menu.
    '''
    next_item_index = self.active_index + direction
    # Close menu if at menu boundary, out of range
    if next_item_index >= len(self) or next_item_index < 0 :
      self.close(event) # deactivates item control
      gui.manager.focus.unfocus()
      gui.manager.control.control_manager.activate_root_control()
    else:
      self._highlight_current(event, False)
      current_controlee = self[self.active_index].controlee
      self.active_index = next_item_index
      # Assert group already laid out
      # Next control controls current controlee ???
      ## Was self.controlee
      gui.manager.control.control_manager.deactivate_current_control()
      # TODO clarify difference between current control and current item
      self._activate_current(event, current_controlee)
      self._highlight_current(event, True)

  @dump_event
  def next(self, event):
    self._change_item(event, 1)
   
  @dump_event
  def previous(self, event):
    self._change_item(event, -1)
    
    
  #@dump_event
  def _activate_current(self, event, controlee):
    '''
    Make current menu item receive events.
    This is separate from drawing: the menu draws current item.
    '''
    # print self.[self.active_index].get_rect()
    gui.manager.control.control_manager.activate_control(self[self.active_index], controlee)
      
  def _deactivate_current(self):
    # assert current item of menu is current control
    gui.manager.control.control_manager.deactivate_current_control()

  def _highlight_current(self, event, direction):
    self[self.active_index].highlight(direction)

  def __repr__(self):
    return self.__class__.__name__ + self.name + str(id(self))










