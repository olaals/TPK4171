import numpy as np
import matplotlib.pyplot as plt


def plot_homg_line2d(ax, l, start, end):
    if len(l) != 3:
        raise Exception('l must be of length 3')
    if l[1] == 0:
        raise Exception('cant plot horizontal lines')

    a = l[0]
    b = l[1]
    c = l[2]

    

    A = -a/b
    B = -c/b
    f = lambda x: A*x + B
    x_range = np.linspace(start, end, 100)
    ax.plot(x_range, f(x_range))
        