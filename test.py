import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import utils as ut
import math
import numpy as np


T = np.zeros((4,4))

T[3,3] = 1.0
R = ut.rotx(math.pi*1.1)
T[0:3,0:3] = R
t = np.array([1,1,1])
T[0:3,3] = t
print(T)

T_inv = ut.invertTrans(T)
print(T_inv)