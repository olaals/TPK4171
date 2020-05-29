import addPathToModules
import robotics as rb
import visualize as viz
import vision as vsn
import numpy as np
import matplotlib.pyplot as plt

# ax + by + c = 0
# y = Ax + B
# A = -c/b
# B = -a/b

def f(x, A, B):
    return A*x + B


a = 2
b = -5
c = 2

A = -a/b
B = -c/b

print(A, B)

x_range = np.linspace(-10, 10, 100)

plt.arrow(0,0, a, b)
plt.plot(x_range, f(x_range, A, B))
plt.axis('equal')
plt.grid('on')
plt.show()


