

# scraps

'''
def draw_background(self, acv, dw, x, y, ww, hh, pb):
   gc = dw.new_gc()
   pw = pb.get_width()
   ph = pb.get_height()
   offset_x = x % pw
   offset_y = y % ph
   dw_y = -offset_y
   while dw_y < hh:
       dw_x = -offset_x
       while dw_x < ww:
           dw.draw_pixbuf(gc, pb, 0, 0, dw_x, dw_y)
           dw_x += pw
       dw_y += ph
       
  # load graphic
  # pb = gdk.pixbuf_new_from_file('ufo-input.png')
  #w, h = pb.get_width(), pb.get_height()

 
 '''

def foo(accel_group, acceleratable, keyval, modifier):
  print "Accelerator", keyval, modifier
  return True
  
accelerators = gtk.AccelGroup()
  window.add_accel_group(accelerators)
  accelerators.connect_group(122, gdk.CONTROL_MASK, accel_flags=gtk.ACCEL_VISIBLE, callback=foo)
  # gdk.GDK_Left


