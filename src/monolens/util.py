import os
import sys
from PySide6 import QtGui
import numpy as np
import numba as nb

DEBUG = int(os.environ.get("DEBUG", "0"))


def clip(x, xmin, xmax):
    if x < xmin:
        return xmin
    return min(x, xmax)


class QImageArrayInterface:
    __slots__ = ("__array_interface__",)

    def __init__(self, image):
        format = image.format()
        assert format == QtGui.QImage.Format_RGB32
        bytes_per_pixel = 4
        bytes_per_line = image.bytesPerLine()
        print(bytes_per_line)

        self.__array_interface__ = {
            "shape": (image.width() * image.height(),),
            "typestr": "|u4",
            "data": image.bits(),
            "strides": (bytes_per_pixel,),
            "version": 3,
        }


def qimage_array_view(image):
    if sys.byteorder == "little":
        bgra = (0, 1, 2, 3)
    else:
        bgra = (3, 2, 1, 0)

    dtype = {
        "b": (np.uint8, bgra[0], "blue"),
        "g": (np.uint8, bgra[1], "green"),
        "r": (np.uint8, bgra[2], "red"),
        "a": (np.uint8, bgra[3], "alpha"),
    }
    raw = np.asarray(QImageArrayInterface(image))
    return raw.view(dtype, np.recarray)


@nb.njit
def _grayscale(d, s):
    g = 0.299 * s.r + 0.587 * s.g + 0.114 * s.b
    d.r = g
    d.g = g
    d.b = g


def grayscale(dest, source):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    assert s.shape == d.shape
    _grayscale(d, s)


def to_lms(a):
    out = np.empty((3,) + a.shape, np.float16)
    out[0] = 0.3904725 * a.r + 0.54990437 * a.g + 0.00890159 * a.b
    out[1] = 0.07092586 * a.r + 0.96310739 * a.g + 0.00135809 * a.b
    out[2] = 0.02314268 * a.r + 0.12801221 * a.g + 0.93605194 * a.b
    return out


def from_lms(rgb, a):
    rgb.r = np.einsum("i,...i", [2.85831110e00, -1.62870796e00, -2.48186967e-02], a)
    rgb.g = np.einsum("i,...i", [-2.10434776e-01, 1.15841493e00, 3.20463334e-04], a)
    rgb.b = np.einsum("i,...i", [-4.18895045e-02, -1.18154333e-01, 1.06888657e00], a)


def colorblindness(dest, source, type):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    lms = to_lms(s)
    if type == 0:  # protanopia
        lms[0] = 0.90822864 * lms[1] + 0.008192 * lms[2]
    elif type == 1:  # deuteranopia
        lms[1] = 1.10104433 * lms[0] - 0.00901975 * lms[2]
    elif type == 2:  # tritanopia
        lms[2] = -0.15773032 * lms[0] + 1.19465634 * lms[1]
    from_lms(d, lms)
