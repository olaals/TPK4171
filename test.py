import numpy as np
import robotics as rb
import math

R = rb.rotx(math.pi/8)
print(R)
print(math.pi/8)
R_log = rb.matrixLog3AngAx(R)
print(R_log)
