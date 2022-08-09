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

# matrix values from colorblind package
_CB_MATRIX_LMS = [
    # Protanopia (red weakness)
    [[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]],
    # Deuteranopia (green weakness)
    [[1, 0, 0], [1.10104433, 0, -0.00901975], [0, 0, 1]],
    # Tritanopia (blue weakness)
    [[1, 0, 0], [0, 1, 0], [-0.15773032, 1.19465634, 0]],
]
_RGB2LMS = [
    [0.3904725, 0.54990437, 0.00890159],
    [0.07092586, 0.96310739, 0.00135809],
    [0.02314268, 0.12801221, 0.93605194],
]
_lms2rgb = np.linalg.inv(_RGB2LMS)
_CB_MATRIX_RGB = [
    np.linalg.multi_dot((_lms2rgb, cbi, _RGB2LMS)) for cbi in _CB_MATRIX_LMS
]


def qimage_array_view(image):
    format = image.format()
    assert format == QtGui.QImage.Format_RGB32
    return np.frombuffer(image.bits(), dtype="|u1").reshape(
        (image.width() * image.height(), 4)
    )


@nb.njit(parallel=False, cache=True)
def _grayscale(d, s, argb, nthreads):
    a, r, g, b = argb
    block = s.shape[0] // nthreads
    for i in nb.prange(nthreads):
        sl = slice(i * block, min((i + 1) * block, s.shape[0]))
        sr = s[sl, r]
        sg = s[sl, g]
        sb = s[sl, b]
        c = np.clip(0.299 * sr + 0.587 * sg + 0.114 * sb, 0, 255)
        d[sl, a] = 255
        d[sl, r] = c
        d[sl, g] = c
        d[sl, b] = c


def grayscale(dest, source):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    _grayscale(d, s, argb, nb.get_num_threads())


@nb.njit(parallel=True, cache=True)
def _colorblindness(d, s, cb, argb, nthreads):
    a, r, g, b = argb
    block = s.shape[0] // nthreads
    for i in nb.prange(nthreads):
        sl = slice(i * block, min((i + 1) * block, s.shape[0]))
        sr = s[sl, r]
        sg = s[sl, g]
        sb = s[sl, b]
        dr = cb[0, 0] * sr + cb[0, 1] * sg + cb[0, 2] * sb
        dg = cb[1, 0] * sr + cb[1, 1] * sg + cb[1, 2] * sb
        db = cb[2, 0] * sr + cb[2, 1] * sg + cb[2, 2] * sb
        d[sl, a] = 255
        d[sl, r] = np.clip(dr, 0, 255)
        d[sl, g] = np.clip(dg, 0, 255)
        d[sl, b] = np.clip(db, 0, 255)


def colorblindness(dest, source, kind):
    s = qimage_array_view(source)
    d = qimage_array_view(dest)
    cb = _CB_MATRIX_RGB[kind]
    _colorblindness(d, s, cb, argb, nb.get_num_threads())
