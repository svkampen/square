import numpy
from geometry import Area, Vector2, get_slice
from PIL import Image
import sys

from math import floor, ceil
from fractions import gcd
from functools import reduce, partial, lru_cache
from operator import mul

from typing import Optional, Callable
import ctypes

sq_c = ctypes.CDLL("./square.so")
sq_c.rgbdiff_p.restype = ctypes.c_double
sq_c.rgbdiff_p.argtypes = [ctypes.c_double] * 6

def rgbdiff(arr1: numpy.ndarray, arr2: numpy.ndarray) -> float:
    """ Get the color difference for two RGB colors. """
    return sq_c.rgbdiff_p(arr1[0], arr1[1], arr1[2],
            arr2[0], arr2[1], arr2[2])
