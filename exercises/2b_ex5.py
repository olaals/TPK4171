import numpy as np
import robotics as rb
import math
import time

#calculate avrage rotatioin matrix using chordal distance

u1 = np.array([0.0, 0.0, 0.5])
u2 = np.array([0.2, 0.0, 0.5])
u3 = np.array([-0.1, 0.0, 0.5])
u4 = np.array([0.0, 0.05, 0.5])
u5 = np.array([0.0,-0.15, 0.5])

R1 = rb.exponentialRotToRot2(u1)
R2 = rb.exponentialRotToRot2(u2)
R3 = rb.exponentialRotToRot2(u3)
R4 = rb.exponentialRotToRot2(u4)
R5 = rb.exponentialRotToRot2(u5)

R_stack = np.stack((R1, R2, R3, R4, R5))
#print(R_stack)

print(R_stack[0, :, :])


n = 5

R = np.eye(3)
r = np.ones(3)
print(r)

norm = np.linalg.norm

while norm(r) > 0.001:
   r = 0
   for i in range(n):
       r = r + rb.matrixLog3AngAx(R.transpose()@R_stack[i,:,:])
   R = R@rb.exponentialRotToRot2(r/n)
   print(norm(r))
   #ime.sleep(0.1)
R_grad_search = R

Ce = np.zeros((3,3))
for i in range(n):
    Ce += R_stack[i, :, :].transpose()

U, S, VT = np.linalg.svd(Ce)
V = VT.transpose()
Rsvd = V@np.diag(np.array([1.0, 1.0, np.linalg.det(U@VT)]))@U.transpose()
print(Rsvd)


