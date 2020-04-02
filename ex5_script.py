import robotics as rb
import visualize as viz
import vision as vsn
import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

#viz.defaultAxisSetup(ax)


# a_i = R @ b_i

b1 = np.array([1.0, 0.0, 0.0])
b2 = np.array([1.0,1.0,0.0])

print("b1")
print(b1)

print("b2")
print(b2)

a1 = np.array([0.5, 0.866, 0.0])
a2 = np.array([-0.25, 1.299, 0.5])

print("a1")
print(a1)
print("a2")
print(a2)

A = np.stack((a1, a2)).transpose()
B = np.stack((b1, b2)).transpose()

H = B @ A.transpose()

print(H)

U, S, VT = np.linalg.svd(H)
V = VT.transpose()
S = np.diag(S)

print("U")
print(U)
print("S")
print(S)
print("V")
print(V)

R = V @ U.transpose()

print("R")
print(R)

print("Determinant R:")
print(np.linalg.det(R))

S = np.diag(np.array([1,1, np.linalg.det(V@U.transpose())]))
print("S")
print(S)

#R = V @ S @U.transpose()
print("Determinant R:")
print(np.linalg.det(R))

### Verify solution
print("a1")
print(a1)
print("R@b_1")
print(R@b1)

print("a2")
print(a2)
print("R@b_2")
print(R@b2)


#plt.show()
