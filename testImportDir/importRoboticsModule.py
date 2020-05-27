import sys
import os

path = os.path.abspath('..')
print(path)

path = path + '/module_oa'

sys.path.append(path)

import robotics as rb

print(rb.rotx(3.4))
