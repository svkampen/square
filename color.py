import math

def rgb2xyz(arr):
    arr = [it/255 for it in arr]
    arr = [((it + 0.055) / 1.055) ** 2.4 if it > 0.04045 else it / 12.92 for it in arr]
    arr = [it * 100 for it in arr]

    X = arr[0] * 0.4124 + arr[1] * 0.3576 + arr[2] * 0.1805
    Y = arr[0] * 0.2126 + arr[1] * 0.7152 + arr[2] * 0.0722
    Z = arr[0] * 0.0193 + arr[1] * 0.1192 + arr[2] * 0.9505
    return [X,Y,Z]

def xyz2lab(arr):
    ref_x = 95.047
    ref_y = 100.000
    ref_z = 108.883

    arr[0] /= ref_x
    arr[1] /= ref_y
    arr[2] /= ref_z

    for n, item in enumerate(arr):
        if ( item > 0.008856 ):
            arr[n] **= (1/3)
        else:
            arr[n] = (7.787 * arr[n]) + (16 / 116)

    CIE_L = (116 * arr[1]) - 16
    CIE_a = 500 * (arr[0] - arr[1])
    CIE_b = 200 * (arr[1] - arr[2])

    return (CIE_L, CIE_a, CIE_b)

def rgb2lab(arr):
    return xyz2lab(rgb2xyz(arr))

def cie76_deltaE(lab1, lab2):
    return math.sqrt((lab2[0] - lab1[0])**2 + (lab2[1] - lab1[1])**2 + (lab2[2] - lab1[2])**2)

def rgbdiff(rgb1, rgb2):
    return cie76_deltaE(rgb2lab(rgb1), rgb2lab(rgb2))
