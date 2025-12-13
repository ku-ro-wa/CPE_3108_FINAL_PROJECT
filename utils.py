


def relative_error(approx, exact):
    """Calculate the relative error between an approximate and exact value."""
    if exact == 0:
        raise ValueError("Exact value cannot be zero for relative error calculation.")
    return abs((approx - exact) / exact)