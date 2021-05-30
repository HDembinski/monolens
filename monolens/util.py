import os
import sys
from PySide6 import QtGui
import numpy as np

# import numba as nb

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


# @nb.njit
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


cb = np.array(
    [
        [[1, 0, 0], [1.10104433, 0, -0.00901975], [0, 0, 1]],
        [[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 1, 0], [-0.15773032, 1.19465634, 0]],
    ],
    dtype=np.float16,
)
rgb2lms = np.array(
    [
        [0.3904725, 0.54990437, 0.00890159],
        [0.07092586, 0.96310739, 0.00135809],
        [0.02314268, 0.12801221, 0.93605194],
    ],
    dtype=np.float16,
)
lms2rgb = np.linalg.inv(rgb2lms)

cb_full = [np.linalg.multi_dot(lms2rgb, cbi, rgb2lms) for cbi in cb]


def colorblindness(dest, source, type):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    d.r = (
        cb_full[type][0, 0] * s.r
        + cb_full[type][0, 1] * s.g
        + cb_full[type][0, 2] * s.b
    )
    d.g = (
        cb_full[type][1, 0] * s.r
        + cb_full[type][1, 1] * s.g
        + cb_full[type][1, 2] * s.b
    )
    d.b = (
        cb_full[type][2, 0] * s.r
        + cb_full[type][2, 1] * s.g
        + cb_full[type][2, 2] * s.b
    )
