import os
import sys

abs_path = os.getcwd()

split_path = abs_path.split('TPK4171')


module_path = split_path[0] + 'TPK4171/module_oa'

sys.path.append(module_path)


