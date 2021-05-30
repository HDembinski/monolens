import os

DEBUG = int(os.environ.get("DEBUG", "0"))


def clip(x, xmin, xmax):
    if x < xmin:
        return xmin
    return min(x, xmax)
