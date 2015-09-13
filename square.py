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

def remove_array(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not (id(L[ind]) == id(arr)):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')

def sq(data):
    """Split an image into squares. If the image's greatest common divisor is
    <64, just quarter it. If x == y, also quarter. Returns them in some order,
    can't remember which (figure it out yourself)"""
    data_size   = Vector2(*data.shape[:2])
    edge_length = gcd(data_size.x, data_size.y)

    if (data_size.x == data_size.y):
        return quarter(data)

    if (edge_length < 64):
        return quarter(data)

    n_squares = Vector2(data_size.x / edge_length, data_size.y / edge_length)

    slices = []

    for i in range(int(n_squares.y)):
        for j in range(int(n_squares.x)):
            print("Slicing from [%d:%d] (x) and [%d:%d] (y)" % (i*edge_length,
                i*edge_length + edge_length, j * edge_length, j*edge_length+edge_length))
            slices.append(get_slice(data, Area(i * edge_length, j * edge_length,
                edge_length, edge_length)))

    return slices
