"""
From example on page 274
"""

import numpy as np
import robotics as rb
import math

#input data points
b1 = np.array([1.0, 0.0, 0.0])
b2 = np.array([1.0, 1.0, .0])
b3 = np.array([0.0, 1.0, .0])
b4 = np.array([0.0, 1.0, 1.0])

B = np.stack((b1, b2, b3, b4)).transpose()
print("B")
print(B)

pi = math.pi

Ra = rb.rotz(pi/9)@rb.roty(pi/4)@rb.rotx(pi/6)
print("Ra")
print(Ra)
print(np.linalg.det(Ra))


A = Ra@B
print("A")
print(A)

H = B@A.transpose()

U, S, VT = np.linalg.svd(H)
V = VT.transpose()

Rc = V@U.transpose()

deltaRtest = Rc@Ra.transpose()
print("DeltaRtest")
print(deltaRtest)

