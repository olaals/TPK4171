import numpy as np

def rotx(rad):
    R = np.array([[1, 0, 0], [0, np.cos(rad), -np.sin(rad)], [0, np.sin(rad), np.cos(rad)]])
    #R  = np.round(R, 10)
    return R

def roty(rad):
    R = np.array([[np.cos(rad), 0, np.sin(rad)], [0, 1, 0], [-np.sin(rad), 0, np.cos(rad)]])
    #R = np.round(R, 10)
    return R

def rotz(rad):
    R = np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0,0,1]])
    #R = np.round(R,10)
    return R

def makeTrans(R,t):
    T = np.zeros((4,4))
    T[3,3] = 1.0
    T[0:3, 0:3] = R
    T[0:3, 3] = t
    return T

def invertTrans(T):
    R = T[0:3, 0:3]
    t = T[0:3, 3]
    R_inv = R.transpose()
    t_inv = -R_inv@t
    T_inv = np.zeros((4,4))
    T_inv[0:3,0:3] = R_inv
    T_inv[0:3, 3] = t_inv
    T_inv[3,3] = 1.0
    return T_inv

def homgLineFrom2Points(p1, p2):

    l = p1[3]*p2[0:3] - p2[3]*p1[0:3]
    l_dash = np.cross(p1[0:3], p2[0:3])

    homg_line = np.concatenate((l,l_dash))
    print(homg_line)

    return homg_line
    
def homgPlaneFrom3Points(p1, p2, p3):
    n = np.cross((p1[0:3]-p3[0:3]), (p2[0:3] - p3[0:3]))
    d = -np.dot(p3[0:3], np.cross(p1[0:3], p2[0:3]))
    d = np.array([d])
    homg_plane = np.concatenate((n,d))
    return homg_plane

def skew(v):
    if len(v) == 4: v = v[:3]/v[3]
    v1 = v[0]
    v2 = v[1]
    v3 = v[2]
    mat = np.array([[0, -v3, v2],[v3, 0, -v1],[-v2, v1, 0]])
    return mat

"""

did not get this to work
def getRotMatFrom2Vec(a, b):
    print("hei")
    v = np.cross(a,b)
    s = np.linalg.norm(v)
    c = np.dot(a,b)

    R = np.eye(3) + skew(v) + skew(v)@skew(v) /(1+c)

    return R
"""

# this one works
def getRotMatFrom2Vec(a, b):
    x = np.cross(a, b) 
    x = x / np.linalg.norm(x)

    theta = np.arccos(np.dot(a,b)/np.dot(np.linalg.norm(a), np.linalg.norm(b)))

    A = skew(x)

    R = np.eye(3) + np.sin(theta) * A + (1 - np.cos(theta)) * A@A

    return R

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

