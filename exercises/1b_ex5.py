import numpy as np
import math
import robotics as rb

b1 = np.array([1.0, 0.0, 0.001])
b2 = np.array([1.0, 1.0, 0.0])
print(f'b1: {b1}')
print(f'b2: {b2}')

R = rb.rotz(math.pi/2)
print("Rotz(pi/2)")
print(R)

# noise vectors
n1 = np.array([0.0, 0.0, -0.01])
n2 = np.array([0.0, 0.0, 0.0])

a1 = R@b1 + n1
a2 = R@b2 + n2

# assemble matrices
A = np.stack((a1, a2)).transpose()
B = np.stack((b1, b2)).transpose()
print("A")
print(A)
print("B")
print(B)

H = B@A.transpose()

U, S, VT = np.linalg.svd(H)
V = VT.transpose()
S = np.diag(S)

# optimal solution
R = V@U.transpose()
print("Optimal R")
print(R)
print("Determinant of R")
print(np.linalg.det(R))
print("since determinant is negative, it is a reflection matrix")

print("need to use R = VSU^T to ensure it is a rotation matrix")
print("where S = diag[1,1,det(VU^T)]")

S = np.diag(np.array([1.0, 1.0, np.linalg.det(V@U.transpose())]))

R = V@S@U.transpose()

print("Optimal rot mat R")
print(R)
print("Determinant")
print(np.linalg.det(R))



