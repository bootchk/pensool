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
    open(), close()
    add()
    next(), previous()
    
  Menu subclasses differ in their layout.
  '''
  
  def __init__(self, viewport):
    compound.Compound.__init__(self, viewport)
    self.active_index = 0
    '''
    !!! an ItemGroup has a controlee that initializes the controlees
    of its items.  Its items can later change themselves to other controlees.
    '''
    self.controlee = None
    '''
    An ItemGroup is laid out on a vector.
    Often, but not necessarily, linear along this vector.
    '''
    self.layout_vector = None


  def open(self, event, controlee=None):
    '''
    Make visible at event coords.
    Focus item at event.
    '''
    print "Open menu *********************", repr(self)
    # Set the new controlee, since the layout may use it.
    self.controlee = controlee
    # Position whole menu group.  Does a layout.???
    rect = coordinates.coords_to_bounds(event)
    self.set_origin(rect) ## was event
    # TODO center of first item?
    ## self.layout(event)
    
    scheme.widgets.append(self)
    
    self.invalidate()
    self.active_index = 0 # activate first
    # !!! Pass the controlee to the items
    self._activate_current(event, controlee)
    self._highlight_current(event, True)
  
  
  def layout(self, event):
    ''' Layout (position) all items in group'''
    print "???Virtual layout method called"
    
    
  def close(self, event):
    print "Closing menu *****************"
    # TODO delete only self, if many widgets can be visible
    del scheme.widgets[-1:]
    self.invalidate()
    focusmgr.feedback_focus_cancel()  # Unhighlight any controlee
    
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
    rect = coordinates.normalize_vector_to_vector(exit_vector, self.layout_vector)
    
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
    Slide this menu orthogonally to original axis
    by magnitude pixels_off_axis
    in the angle left or right indicated by sign of pixels_off_axis.
    Changes the origin of the menu and the layout.
    '''
    # Right handed vector orthogonal to menu's vector
    vector = coordinates.vector_orthogonal(self.layout_vector, pixels_off_axis)
    ### if pixels_off_axis < 0 :
    # scale by magnitude of pixels_off_axis
    coordinates.vector_multiply_scalar(vector, math.fabs(pixels_off_axis))
    # Add to menu origin
    coordinates.vector_add(vector, self.dimensions)
    self.invalidate()   # invalidate current layout
    # Change origin, triggers layout
    ## Was dimensions = 
    self.set_origin(vector)
    
    # Redo layout
    ##self.layout(vector)  # vector is ignored
    ##self.invalidate()
    
    
   
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
    
    
  def _activate_current(self, event, controlee):
    print "Activate current", self.active_index
    # print self.[self.active_index].get_rect()
    guicontrolmgr.control_manager.activate_control(self[self.active_index], 
      event, controlee)
    
    
  def _deactivate_current(self, event):
    guicontrolmgr.control_manager.deactivate_control(self[self.active_index],
       event)


  def _highlight_current(self, event, direction):
    # 
    print "Highlighting", self.active_index, direction
    self[self.active_index].highlight(direction)



class MenuGroup(ItemGroup):
  '''
  Traditional menu, layout is:
    fixed position,
    vertical, 
    all items visible
  '''
  
  @dump_event
  def layout(self, event):
    '''
    Layout (position) all items in group
    in vertical, rectangular table.
    Event is ignored, use dimensions,
    which is the event from the opening,
    or from a slide.
    '''
    # Layout first item centered on opening event
    temp_rect = self.dimensions
    for item in self:
      item.center_at(temp_rect)
      # Layout next item downward
      temp_rect.y += item.dimensions.height




class HandleGroup(ItemGroup):
  '''
  Handle menu, layout is:
    moveable,
    layout reorients
    !!! only one item shown, as mouseovered
  '''
  @dump_event
  def layout(self, event):
    '''
    Layout (position) all items in group
    in a line orthogonal to the glyph
    in an order towards the center of the glyph
    (anti direction of orthogonal vector.)
    
    A handle group is laid out every time it slides.
    When exit an item, other items are already laid out.
    '''
    print "Laying out handle group"
    # Layout first item centered on event
    temp_rect = coordinates.dimensions(event.x, event.y, 0, 0)
    
    # get vector for direction of menu: orthogonal to the controlee eg glyph
    layout_vector = self.controlee.orthogonal(event)
    self.layout_vector = layout_vector  # Remember it, items can ask for it
    
    # layout all items
    for item in self:
      item.center_at(temp_rect)
      
      ''' Dumbed down version
      # Layout next item leftward
      temp_rect.x -= item.dimensions.width/2
      '''
      # Multiply unit ortho vector by dimension vector; add/sub to previous coords
      # FIXME vector scale, translate
      temp_rect.x -= layout_vector.x * item.dimensions.width/2
      temp_rect.y -= layout_vector.y * item.dimensions.height/2
      
      
      
   
  def draw(self, context):
    '''
    Draw only the current item.
    !!! Overrides group draw.
    '''
    self[self.active_index].draw(context)
 
