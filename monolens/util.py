def clip(x, xmin, xmax):
    if x < xmin:
        return xmin
    return min(x, xmax)
