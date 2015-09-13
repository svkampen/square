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



def quarter(data):
    """Split an image into four quarters. Return them in order topleft, topright, botleft, botright.
    If the image has an odd number of pixels on an axis, have one half be +0.5px, the other -0.5px.
    """

    size = Vector2(*data.shape[:2])
    x_pair = [size.x / 2, size.x / 2]
    y_pair = [size.y / 2, size.y / 2]

    if (size.x % 2 == 1):
        x_pair[0] = floor(x_pair[0])
        x_pair[1] = ceil(x_pair[1])

    if (size.y % 2 == 1):
        y_pair[0] = floor(y_pair[0])
        y_pair[1] = ceil(y_pair[1])

    return [data[:y_pair[0],:x_pair[1]],
            data[:y_pair[0],x_pair[0]:],
            data[y_pair[1]:,:x_pair[1]],
            data[y_pair[1]:,x_pair[0]:]]
def process_area(thresh, area):
    """Process an Area. Returns True if the area's max_deviation is < thresh,
    False otherwise."""
    if 0 in area.shape:
        return [True, numpy.array([0,0,0])]
    average = area.mean(0).mean(0)
    pixel_list = area.reshape(reduce(mul, area.shape[:2]), 3)
    max_deviation = max(map(partial(rgbdiff, average), pixel_list))

    if (max_deviation > thresh):
        return [False, average]

    return [True, average]

def calculate_percentage(id, a, part):
    total = id.size
    return 100 - ((part / total) * 100.0)

def transform_image(input, output, thresh):
    original_image = Image.open(input)

    # When indexing, instead of doing [x,y], remember to do [y,x]
    imagedata = numpy.array(original_image,dtype=numpy.float64)
    imagedata /= 255.0

    areas = sq(imagedata)
    areas_size = imagedata.size

    while areas:
        for area in areas:
            assert area.base is imagedata
            area_done, average = process_area(thresh, area)
            if area.shape[0] < 3 or area.shape[1] < 3:
                area_done = True
            if (area_done):
                print("Finished area with size: (%d, %d)\t\t%.2f"
                        % (*area.shape[:2], calculate_percentage(imagedata,
                            areas, areas_size)))
                remove_array(areas, area)
                areas_size -= area.size
                numpy.copyto(area, numpy.full(area.shape, average, dtype=numpy.float64))
            else:
                print("Splitting area with size: (%d, %d)\t\t%.2f"
                        % (*area.shape[:2], calculate_percentage(imagedata,
                            areas, areas_size)))
                remove_array(areas, area)
                for q in quarter(area):
                    areas.append(q)

    new_image = Image.fromarray((imagedata * 255).round().astype(numpy.uint8))
    new_image.save(output)


if __name__ == "__main__":
    print("Square, version 0 - (c) 2015 Sam van Kampen")
    print("Licensed under the GNU GPL version 3.0")

    if len(sys.argv) == 1:
        print("Usage: sq <input> <output> [delta-e threshold]")
    else:
        transform_image(sys.argv[1], sys.argv[2], float(sys.argv[3]))
