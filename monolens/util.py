import os
import sys
from PySide6 import QtGui
import numpy as np
import numba as nb

DEBUG = int(os.environ.get("DEBUG", "0"))

if sys.byteorder == "little":
    argb = (3, 2, 1, 0)
else:
    argb = (0, 1, 2, 3)

cb_lms = np.array(
    [
        [[1, 0, 0], [1.10104433, 0, -0.00901975], [0, 0, 1]],
        [[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 1, 0], [-0.15773032, 1.19465634, 0]],
    ],
)
rgb2lms = np.array(
    [
        [0.3904725, 0.54990437, 0.00890159],
        [0.07092586, 0.96310739, 0.00135809],
        [0.02314268, 0.12801221, 0.93605194],
    ],
)
lms2rgb = np.linalg.inv(rgb2lms)
cb_full = [np.linalg.multi_dot((lms2rgb, cbi, rgb2lms)) for cbi in cb_lms]


def clip(x, xmin, xmax):
    if x < xmin:
        return xmin
    return min(x, xmax)


class QImageArrayInterface:
    __slots__ = ("__array_interface__",)

    def __init__(self, image):
        format = image.format()
        assert format == QtGui.QImage.Format_RGB32

        self.__array_interface__ = {
            "shape": (image.width() * image.height(), 4),
            "typestr": "|u1",
            "data": image.bits(),
            "version": 3,
        }


def qimage_array_view(image):
    return np.asarray(QImageArrayInterface(image))


@nb.njit
def _grayscale(d, s):
    a, r, g, b = argb
    for i, p in enumerate(s):
        c = 0.299 * p[r] + 0.587 * p[g] + 0.114 * p[b]
        d[i][r] = c
        d[i][g] = c
        d[i][b] = c


def grayscale(dest, source):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    assert s.shape == d.shape
    _grayscale(d, s)


@nb.njit
def _colorblindness(d, s, cb):
    a, r, g, b = argb
    for i, p in enumerate(s):
        d[i, r] = cb[0, 0] * p[r] + cb[0, 1] * p[g] + cb[0, 2] * p[b]
        d[i, g] = cb[1, 0] * p[r] + cb[1, 1] * p[g] + cb[1, 2] * p[b]
        d[i, b] = cb[2, 0] * p[r] + cb[2, 1] * p[g] + cb[2, 2] * p[b]


def colorblindness(dest, source, type):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    cb = cb_full[type]
    _colorblindness(d, s, cb)
