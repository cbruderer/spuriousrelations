import numpy as np


def get_keys(path='../docs/keywords.txt'):
    keys = np.genfromtxt(path, dtype="|S20", delimiter='#', autostrip=True)
    return keys

# test
# keys = get_keys()
# print type(keys[0]), type(keys)
# for i in keys:
# 	print i, len(i)
