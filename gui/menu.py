#!/usr/bin/env python


'''
Managers of groups of controls.
Enforces a policy on the group.
Here the policy is for menus: one active item.
There is another manager that enforces a policy over the whole application.
'''


import drawable
import compound
import coordinates
import focusmgr
import scheme
import guicontrolmgr
from decorators import *
import math
import layout
import base.vector as vector
import copy

# FIXME
import textselectmanager



# TODO abstract ControlGroup from Menu and HandleMenu and Dock

# TODO a single GuiControl

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
  
    An ItemGroup is laid out on a vector from an origin.
    Often, but not necessarily, linear along this vector.
    The origin is where the user clicked.
  '''
  
  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)
    self.active_index = 0
    '''
    !!! an ItemGroup has a controlee that initializes the controlees
    of its items.  Its items can later change themselves to other controlees.
    '''
    self.controlee = None
    #self.layout_spec = None
    


  @dump_event
  def open(self, event, controlee=None):
    '''
    Make visible at event coords.
    Focus item at event.
    '''
    # Set new controlee, since new_layout_spec may use it.
    self.controlee = controlee
    
    self.new_layout_spec(event)
    
    # Position whole menu group.  Lays out members!!!
    rect = coordinates.copy(self.layout_spec.benchmark)
    self.set_origin(rect) ## was event
    
    scheme.widgets.append(self)
    
    self.invalidate()
    self.active_index = 0 # activate first
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
    print "???Virtual layout method called"
    
    
  @dump_event
  def close(self, event):
    # TODO delete only self, if many widgets can be visible
    del scheme.widgets[-1:]
    self.invalidate()   # menu
    focusmgr.unfocus()  # any controlee, should invalidate
    
    # Deactivate current item.  This activates the background manager.
    self._deactivate_current(event)
    
    # FIXME for now, deactivate text select when handle menu closes
    textselectmanager.deactivate_select_for_text()
    
    
  def add(self, item):
    self.append(item)
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
    rect = coordinates.normalize_vector_to_vector(exit_vector, self.layout_spec.vector)
    
    # Seems backwards, but since menu vector is opposite direction to layout,
    # inverse the sign
    if rect.x < 0 :
      self._change_item(event, 1)
    else :
      self._change_item(event, -1)
    #  TODO recode this without an if
    # direction = - ( rect.x/rect.x)  # TODO is the normal already unit vector?
    
    
    
  @dump_event
  def slide(self, pixels_off_axis):
    '''
    Slide menu orthogonally to original axis.
    
    By magnitude pixels_off_axis
    in angle left or right indicated by sign of pixels_off_axis.
    Changes layout spec.
    '''
    
    # Calculate new layout_spec
    
    # Right handed unit vector orthogonal to menu's vector.
    vect = self.layout_spec.vector.orthogonal(pixels_off_axis)
    ### if pixels_off_axis < 0 :
    # Scale by magnitude of pixels_off_axis
    vect = vect * math.fabs(pixels_off_axis)
    # Offset prior benchmark
    # !!! In-place vector addition
    coordinates.vector_add(self.layout_spec.benchmark, vect)
    # FIXME should be: self.layout_spec.benchmark += vect
    
    self.invalidate()
    self.layout() ## OLD vector
    self.invalidate()
    
    
   
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
      self.close(event)
    else:
      self._highlight_current(event, False)
      current_controlee = self[self.active_index].controlee  # TODO property
      self.active_index = next_item_index
      # Assert group already laid out
      # Next control controls current controlee ???
      ## Was self.controlee
      self._activate_current(event, current_controlee) # Side affect: deactivate current control
      self._highlight_current(event, True)

  def next(self, event):
    self._change_item(event, 1)
   
  def previous(self, event):
    self._change_item(event, -1)
    
    
  @dump_event
  def _activate_current(self, event, controlee):
    # print self.[self.active_index].get_rect()
    guicontrolmgr.control_manager.activate_control(self[self.active_index], 
      event, controlee)
      
  def _deactivate_current(self, event):
    guicontrolmgr.control_manager.deactivate_control(self[self.active_index],
       event)

  def _highlight_current(self, event, direction):
    self[self.active_index].highlight(direction)

  def __repr__(self):
    return "Menu"


class MenuGroup(ItemGroup):
  '''
  Traditional menu, layout is:
    fixed position,
    vertical orientations, 
    all items visible concurrently
  '''
  
  def new_layout_spec(self, event):
    # Menu benchmark is event
    self.layout_spec.benchmark = coordinates.coords_to_bounds(event)
    # Menu vector is None (its hardcoded in layout)
    self.layout_spec.vector = None
    
    
  @dump_event
  def layout(self, event=None):
    '''
    Layout (position) all items in group in vertical, rectangular table.
    Event is ignored, use coords of most recent event (open, slide, etc.)
    '''
    # Center first item on benchmark.
    # (Which is the same as opening event?)
    temp_rect = coordinates.copy(self.layout_spec.benchmark)
    for item in self:
      item.center_at(temp_rect)
      # Next item downward
      temp_rect.y += item.get_dimensions().height




class HandleGroup(ItemGroup):
  '''
  Handle menu, layout is:
    moveable,
    layout reorients
    !!! only one item shown, as mouseovered
  '''
  
  def new_layout_spec(self, event):
    """
    Create layout_spec based on this event.
    Event opens the menu.
    TODO abstract opening with moving.
    """
    """
    OLD
    """
    #  benchmark is event
    self.layout_spec.benchmark = coordinates.coords_to_bounds(event)
    
    assert self.controlee
    
    if self.controlee is scheme.glyphs:
      # Handle menu opened on background, controls the document
      self.layout_spec.vector = vector.downward_vector()
    else:
      # axis is orthogonal to controlee
      self.layout_spec.vector = self.controlee.get_orthogonal(event)
      
    """
    NEW
    # center menu on the edge of controlee
    # center is intersection of orthogonal and controlee edge
    ray tracing algorithm
    # benchmark: from center proceed half menu length in direction of orthogonal
    """
    
  @dump_event
  def layout(self, event=None):
    '''
    Layout (position) all items in group
    in a line orthogonal to the glyph
    in an order towards the center of the glyph
    (anti direction of orthogonal vector.)
    
    A handle group is laid out every time it slides.
    When exit an item, other items are already laid out.
    '''
    # Center first item on benchmark.  Ignore the event.
    ## OLD temp_rect = coordinates.dimensions(event.x, event.y, 0, 0)
    ### !!! This causes a seg fault temp_rect = copy.copy(self.layout_spec.benchmark)
    temp_rect = self.layout_spec.benchmark.copy()
    '''
    # get vector for direction of menu: orthogonal to the controlee eg glyph
    layout_vector = self.controlee.get_orthogonal(event)
    self.layout_spec.vector = layout_vector  # Remember it, items can ask for it
    '''
    layout_vector = self.layout_spec.vector.copy()
    
    # layout all items
    for item in self:
      item.center_at(temp_rect)
      ''' Dumbed down version
      # Layout next item leftward
      temp_rect.x -= item.dimensions.width/2
      '''
      # Multiply unit ortho vector by dimension vector; add/sub to previous coords
      # FIXME vector scale, translate
      temp_rect.x -= self.layout_spec.vector.x * item.get_dimensions().width/2
      temp_rect.y -= self.layout_spec.vector.y * item.get_dimensions().height/2
    print "returned from layout"
      
      
      
   
  def draw(self, context):
    '''
    Draw only the current item.
    !!! Overrides group draw.
    '''
    self[self.active_index].draw(context)
 
