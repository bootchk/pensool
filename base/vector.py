#!/usr/bin/env python

import math

class Vector:
    ''''
    2D mathematical vectors
    
    (Not a vector in the sense of a sequence or array.)
    
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
      ''' Return scalar angle in radians [-pi, pi] '''
      # !!! atan2(y,x)
      return math.atan2(self.y, self.x)
    
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
      
    
    
# Point is a synonym for the Vector class: they behave the same.
Point = Vector

# Constant vector
def downward_vector():
  return Vector(0, 1)
  
  
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
  

  

  

