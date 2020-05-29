
def dual_angle(l_1, l_2):

    a_1 = l_1[0:3] / np.linalg.norm(l_1[0:3])
    m_1 = l_1[3:6] / np.linalg.norm(l_1[0:3])

    a_2 = l_2[0:3] / np.linalg.norm(l_2[0:3])
    m_2 = l_2[3:6] / np.linalg.norm(l_2[3:6])

    # normal part
    norm_part = np.dot(a_1, a_2)

    # dual part
    dual_part = np.dot(a_1, m_2) + np.dot(a_2, m_2)


    return theta, d