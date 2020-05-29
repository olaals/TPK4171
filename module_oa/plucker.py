import numpy as np


def homgLineFrom2Points(p1, p2):
    print(len(p1))
    if len(p1) > 3:

        l = p1[3]*p2[0:3] - p2[3]*p1[0:3]
    else:
        l = p2[0:3] - p1[0:3]
    l_dash = np.cross(p1[0:3], p2[0:3])

    homg_line = np.concatenate((l,l_dash))
    print(homg_line[0:3])
    homg_line = homg_line / np.linalg.norm(homg_line[0:3])
    print(homg_line)

    return homg_line


