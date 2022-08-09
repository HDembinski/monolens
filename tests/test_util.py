from monolens import util
from monolens.lens import RGB32
from PySide6 import QtGui
import pytest


@pytest.fixture
def images():
    a = QtGui.QImage(1000, 1000, RGB32)
    b = QtGui.QImage(1000, 1000, RGB32)
    return a, b


def test_grayscale(benchmark, images):
    a, b = images
    benchmark(lambda: util.grayscale(a, b))


def test_colorblindness(benchmark, images):
    a, b = images
    benchmark(lambda: util.colorblindness(a, b, 0))
