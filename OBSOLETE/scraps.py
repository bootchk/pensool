"""
  @dump_event
  def invalidate_will_draw(self):
    pass

  
  @dump_return
  def invalidate(self, context):
    ''' 
    Invalidate means queue a region to redraw at expose event.
    GUI specific, not applicable to all surfaces.
    '''
    user_bounds = self.get_inked_bounds()
    ##device_coords = self.viewport.user_to_device(user_bounds.x, user_bounds.y)
    ##device_distance = self.viewport.user_to_device_distance(user_bounds.width, user_bounds.height)
    device_coords = vector.Vector(*context.user_to_device(user_bounds.x, user_bounds.y))
    device_distance = vector.Vector(*context.user_to_device_distance(user_bounds.width, user_bounds.height))
    device_bounds = coordinates.dimensions(device_coords.x, device_coords.y, 
      device_distance.x, device_distance.y)
    self.viewport.surface.invalidate_rect( device_bounds, True )
    return device_bounds
  """
  
  """    
  def get_drawn_extents(self, context):
    '''
    Extents in UCS as drawn (subject to any transformations.)
    '''
    extents = context.path_extents()
    # stroke_extents are float, avert deprecation warning
    # Truncate upper left via int()
    map(math.ceil, extents[2:3])  # ceiling bottom right
    return [int(x) for x in extents]
  """   

  """
  def _get_bounds(self, context, extent_func):
    '''
    '''
    context = self.viewport.user_context()
    self.put_path_to(context)   # recursive
    extents = extent_func()  # inked or ideal, UCS, float
    int_extents = coordinates.integral_extents(*extents)
    bounds = coordinates.dimensions_from_extents(*int_extents)
    return bounds # UCS integral rect
    
 
  def get_bounds(self, context):
    '''
    Return calculated rect of ideal bounding box in UCS.
    !!! Note path_extents is not ink, excludes the width of lines.
    Contrast to stroke_extents.
    '''
    return self._get_bounds(context, context.path_extents)
  
  def get_inked_bounds(self):
    '''
    Return calculated rect of inked bounding box in UCS.
    !!! Note stroke_extents includes the width of lines.
    '''
    return self._get_bounds(context, context.stroke_extents)
  """   
  """
    # stroke_extents are float, avert deprecation warning
    # Truncate upper left via int()
    map(math.ceil, extents[2:3])  # ceiling bottom right
    int_extents = [int(x) for x in extents] 
    bounds = coordinates.dimensions_from_extents(*int_extents)
    # print "Bounds", bounds
    return bounds
  """

for dimensioned drawing  
"""
    rect = self.get_dimensions()
    context.move_to(rect.x, rect.y)
    context.rel_line_to(rect.width, rect.height)
    """

