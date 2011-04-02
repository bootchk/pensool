
# No compiling, but clean, etc.

clean:
  find . -name *.pyc -exec rm {}+
  rind . -name *.py~ -exec rm {}+


