import math

def rgb2xyz(arr):
    """Convert RGB color representation to CIE XYZ"""
    arr = [((it + 0.055) / 1.055) ** 2.4 if it > 0.04045 else it / 12.92 for it in arr]
    arr = [it * 100 for it in arr]

    X = arr[0] * 0.4124 + arr[1] * 0.3576 + arr[2] * 0.1805
    Y = arr[0] * 0.2126 + arr[1] * 0.7152 + arr[2] * 0.0722
    Z = arr[0] * 0.0193 + arr[1] * 0.1192 + arr[2] * 0.9505
    return [X,Y,Z]

def xyz2lab(arr):
    """ Convert CIE XYZ to CIE L* a* b* """
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
    """ RGB -> LAB """
    return xyz2lab(rgb2xyz(arr))

def cie76_deltaE(lab1, lab2):
    """ Delta-Empfindung calculation according to the Commission internationale de l'éclairage, '76
    basically just the euclidean distance """
    return math.sqrt((lab2[0] - lab1[0])**2 + (lab2[1] - lab1[1])**2 + (lab2[2] - lab1[2])**2)

def cie94_deltaE(lab1, lab2):
    """ Delta-Empfindung calculation according to the CIE, '94 """
    delta_l = lab1[0] - lab2[0]
    c1 = math.sqrt(lab1[1]**2 + lab1[2]**2)
    c2 = math.sqrt(lab2[1]**2 + lab2[2]**2)
    delta_c = c1 - c2
    delta_h = math.sqrt(cie76_deltaE(lab1, lab2)**2 - delta_l**2 - delta_c**2)
    s_l = 1
    s_c = 1 + (0.045 * c1)
    s_h = 1 + (0.015 * c1)

    return math.sqrt((delta_l / s_l)**2 + (delta_c / s_c)**2 + (delta_h/s_h)**2)

def rgbdiff(rgb1, rgb2):
    """ Calculates RGB color "distance", using L* a* b* conversions """
    return cie76_deltaE(rgb2lab(rgb1), rgb2lab(rgb2))
