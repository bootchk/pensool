#!/usr/bin/env python

'''
Items in a handle menu.
These items move and resize the controlee.
'''

import itemhandle
import coordinates
from decorators import *
import focusmgr

# TODO isolate these
import cairo
import math
from gtk import gdk   


class MoveHandleItem(itemhandle.HandleItem):
  '''
  A handle that moves the controlee, when a drag starts within.
  Another control is involved when a drag moves out of this item control.
  
  Scrolling descends/rises into controlee when it is composite(compound.)
  '''
  
  def put_path_to(self, context):
    """
    #context.save()
    saved = context.get_matrix()
    transformation = cairo.Matrix()
    transformation.rotate(0.5)
    print ">>>>>>>>>", self.dimensions
    transformation.scale(self.dimensions.width, self.dimensions.height)
    transformation.translate(self.dimensions.x, self.dimensions.y)
    context.transform(transformation)
    # context.set_matrix(transformation)
    context.rectangle(-0.5, -0.5, 1, 1)
    #context.restore()
    context.set_matrix(saved)
    """
    
    context.rectangle(self.get_dimensions())
  
  @dump_event
  def scroll_down(self, event):
    '''
    Filtered event from GuiControl: scroll wheel down in a handle item.
    Make operand a child of composite that is at benchmark of handle menu
    to which this item belongs.
    '''
    print "Old controlee", self.controlee
    if len(self.controlee) > 1:
      # Iterate children to find first at benchmark of handle menu.
      # TODO If more than one at benchmark?
      # Then cycle through siblings ie walk depth first
      for child in self.controlee:
        print "Child ....", repr(child)
        # TODO this is too strict
        # Coords of the benchmark of the handle menu
        print "TODO Benchmark.........."
        ## Bounding box of handle menu : need intersection of boxes
        ## get_dimensions()
        # 
        if child.is_inpath(self.group_manager.layout_spec.benchmark):
          focusmgr.focus(child)
          self.controlee = child
          return
      # One must be at this event
      raise RuntimeError("No morph found for handle menu")
    else:
    ## OLD except TypeError: # if not iterable
      gdk.beep()
      print "Can't scroll past primitive morph"
  
  
  @dump_event
  def continue_drag(self, event, offset, increment):
    '''
    animate/ghost controlee being dragged
    '''
    # TODO look for suitable target
    
    # Display at new coords, same width and height
    # Since moving in real time, use the increment from previous continue
    self.controlee.move_relative(event, increment)
 

  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    Leave the ghosted move in last position
    '''
    ## OLD source.move_relative(event, offset)
    


  
class ResizeHandleItem(itemhandle.HandleItem):
  '''
  A handle that resizes the controlee, when a drag starts within.
    Another control is involved when drag exits this item control.
  
  Scrolling alters constraints on resize. TODO
  '''

  def put_path_to(self, context):
    centerx, centery, radius = coordinates.circle_from_dimensions(self.get_dimensions())
    context.arc(centerx, centery, radius, 0, 2.0*math.pi)

  def drop(self, source, event, offset, source_control):
    '''
    Some control was the target of a drop that started in this control.
    This control resizes source.
    '''
    source.resize(event, offset)

