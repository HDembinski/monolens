from monolens import util
import numpy as np
import numba as nb

src = np.empty((2073600, 4), np.uint8)
dst = np.empty((2073600, 4), np.uint8)
cb = util.cb_full[0]
a, r, g, b = util.argb


def _colorblindness_np(d, s, cb):
    d[:, r] = cb[0, 0] * s[:, r] + cb[0, 1] * s[:, g] + cb[0, 2] * s[:, b]
    d[:, g] = cb[1, 0] * s[:, r] + cb[1, 1] * s[:, g] + cb[1, 2] * s[:, b]
    d[:, b] = cb[2, 0] * s[:, r] + cb[2, 1] * s[:, g] + cb[2, 2] * s[:, b]


@nb.njit
def _colorblindness_nb(d, s, cb):
    for i, p in enumerate(s):
        d[i, r] = cb[0, 0] * p[r] + cb[0, 1] * p[g] + cb[0, 2] * p[b]
        d[i, g] = cb[1, 0] * p[r] + cb[1, 1] * p[g] + cb[1, 2] * p[b]
        d[i, b] = cb[2, 0] * p[r] + cb[2, 1] * p[g] + cb[2, 2] * p[b]


@nb.njit(parallel=True)
def _colorblindness_nbp(d, s, cb):
    for i in nb.prange(len(s)):
        p = s[i]
        d[i, r] = cb[0, 0] * p[r] + cb[0, 1] * p[g] + cb[0, 2] * p[b]
        d[i, g] = cb[1, 0] * p[r] + cb[1, 1] * p[g] + cb[1, 2] * p[b]
        d[i, b] = cb[2, 0] * p[r] + cb[2, 1] * p[g] + cb[2, 2] * p[b]


def test_colorblindness_np(benchmark):
    benchmark(lambda: _colorblindness_np(dst, src, cb))


def test_colorblindness_nb(benchmark):
    benchmark(lambda: _colorblindness_nb(dst, src, cb))


def test_colorblindness_nbp(benchmark):
    benchmark(lambda: _colorblindness_nbp(dst, src, cb))
