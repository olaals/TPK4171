import robotics as rb
import visualize as viz
import vision as vsn
import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

viz.defaultAxisSetup(ax)



a = np.array([4.0, 3.0, 1.0])
viz.plotHomgPoint(ax, a)



R = rb.roty(math.pi/8)
print("R fasit")
print(R)

print("b = R@a")
b = R@a
viz.plotHomgPoint(ax, b, color = 'b')

print(f'b: {b}')

R_rec1 = rb.rotation_matrix_from_vectors(a,b)

print("R_rec")
print(R_rec1)


print("b_new = R_rec1@a")
b_new = R_rec1@a
print("b_new")
print(b_new)


#plt.show()
