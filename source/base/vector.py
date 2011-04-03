''' 2D vector math'''

'''
Copyright 2010, 2011 Lloyd Konneker

This file is part of Pensool.

Pensool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

import math
import cairo  # FIXME

class Vector(object):
    '''
    2D mathematical vectors (Not in the sense of sequence or array.)
    
    Note all operators except increment, decrement return a copy.
    
    Examples:
    
    # Test setup
    >>> a = Vector(1,1)
    >>> b = Vector(0,1)
    >>> c = Vector(0,-1)
    
    >>> b.scalar_projection(a)
    0.70710678118654746
    
    >>> c.scalar_projection(a)
    -0.70710678118654746
    
    '''
    
    def __init__(self, x = 0, y = 0):
        self.x = float(x)
        self.y = float(y)
        
    def __add__(self, val):
        return Point( self[0] + val[0], self[1] + val[1] )
    
    def __sub__(self,val):
        return Point( self[0] - val[0], self[1] - val[1] )
    
    def __iadd__(self, val):
        self.x = val[0] + self.x
        self.y = val[1] + self.y
        return self
        
    def __isub__(self, val):
        self.x = self.x - val[0]
        self.y = self.y - val[1]
        return self
    
    def __div__(self, val):
        return Point( self[0] / val, self[1] / val )
    
    def __mul__(self, val):
        return Point( self[0] * val, self[1] * val )
    
    def __idiv__(self, val):
        self[0] = self[0] / val
        self[1] = self[1] / val
        return self
        
    def __imul__(self, val):
        self[0] = self[0] * val
        self[1] = self[1] * val
        return self
                
    def __getitem__(self, key):
        if( key == 0):
            return self.x
        elif( key == 1):
            return self.y
        else:
            raise Exception("Invalid key to Point")
        
    def __setitem__(self, key, value):
        if( key == 0):
            self.x = value
        elif( key == 1):
            self.y = value
        else:
            raise Exception("Invalid key to Point")
        
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def __repr__(self):
      return str(self)
      
    def copy(self):
      return Vector(self.x, self.y)
    
    def orthogonal(self, handedness):
      '''
      Return some vector orthogonal to self.
      Swap x, y and negate one.
      Note that there are many orthogonal vectors to a line, 
      this is an orthogonal vector to a vector (from the origin.)
      Note also that there are two handednesses: right and left handed.
      Handeness negative is left, postive is right.
      Alternative implementation is to use rotate by an angle, +-
      '''
      if handedness < 0: # left
        return Vector(self.y, -self.x)
      else :
        return Vector(-self.y, self.x)

    def length(self):
      '''
      Return scalar distance length.
      Distance is non-negative.
      '''
      return math.sqrt( self.x**2 + self.y**2 )
      
    def normal( self ):
      'Return new vector that has same direction as vec, but has length of one.'
      if( self[0] == 0. and self[1] == 0. ):
          return Vector(0.,0.)
      return self / self.length()

    def angle(self):
      ''' 
      Return scalar angle in radians [-pi, pi] to the x-axis.
      '''
      # !!! atan2(y,x)
      return math.atan2(self.y, self.x)
    
    def angle_to(self, b):
      '''
      Return scalar angle in radians of self to vector b.
      '''
      return b.angle() - self.angle()
      
    def dot( self, b ):
      '''Return scalar dot product of self and b'''
      return self[0]*b[0] + self[1]*b[1]
      
    def scalar_projection(self, b):
      '''
      Return scalar projection of self onto b.
      Scalar projection is the magnitude of the projection of a onto b.
      The sign is significant:  Negative means in the opposite direction of b.
      '''
      return self.dot(b/b.length())
      
      '''
      Alternate implementation?
      For three points p0, p1, p2.
      p1 and p2 define a line.
      (p0.x-p1.x)*(p2.y-p1.y) - (p2.x-p1.x)*(p0.y-p1.y)
      Yields:
        0 p0 on line
        + p0 left of line
        - p0 right of line
      '''
    
    
# Point is a synonym for the Vector class: they behave the same.
Point = Vector

# Constant vectors
# NOT singleton, a new instance each call
# (If a singleton, insure it is read-only.
def downward_vector():
  return Vector(0, 1)

ORIGIN = Vector(0,0)
ONES = Vector(1,1)
UNIT_X_AXIS = Vector(1,0)
UNIT_Y_AXIS = Vector(0,1)
  
# FIXME do it without cairo
def normalize_vector_to_vector(vector1, vector2):
  '''
  Normalize first vector to second.
  Assert both vectors have same origin (0,0)?
  Transform (rotate) second vector to x-axis.
  Return second vector with same rotation.
  '''
  # Make transform to normalize and align vector2 with x-axis
  angle = vector2.angle()
  # inverse the angle.  Cairo's sign for angle is opposite of conventional.
  rotate_transform = cairo.Matrix().init_rotate(-angle)
  # Not scaled, but if would transform.scale, the scale done before rotation
  # Transform exit_vector
  (x,y) = rotate_transform.transform_point(vector1.x, vector1.y)
  vect = Vector(x, y)
  # print "Angle", angle, "Vect1", vector1, "Vect2", vector2, "Normalized:", vect
  return vect
  
  
  
  
"""
        
def DistanceSqrd( point1, point2 ):
    'Return the distance between two points squared. Marginally faster than Distance()'
    return ( (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    
def Distance( point1, point2 ):
    'Return the distance between two points'
    return math.sqrt( DistanceSqrd(point1,point2) )
    
def Dot( a,b ):
    'Computes the dot product of a and b'
    return a[0]*b[0] + a[1]*b[1]
    
def ProjectOnto( w,v ):
    'Projects w onto v.'
    return v * Dot(w,v) / LengthSqrd(v)
"""
  

  

  

