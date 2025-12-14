import numpy as np


# =====================================================
# TABULATED DATA METHODS (x, y arrays)
# =====================================================

def trapezoidal_from_points(x, y):
    """Composite trapezoidal rule for tabulated data (non-uniform spacing allowed)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be 1D arrays")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("At least two points are required")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x values must be strictly increasing (no duplicates)")

    dx = np.diff(x)
    return float(np.sum(dx * (y[:-1] + y[1:]) * 0.5))


def simpsons_from_points(x, y, tol=1e-9):
    """Composite Simpson's 1/3 rule for tabulated data (uniform spacing required)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be 1D arrays")
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 3:
        raise ValueError("At least three points are required for Simpson's rule")
    if (len(x) - 1) % 2 != 0:
        raise ValueError("Simpson's rule requires an even number of subintervals (odd number of points)")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x values must be strictly increasing (no duplicates)")

    h = x[1] - x[0]
    if not np.all(np.isclose(np.diff(x), h, atol=tol, rtol=0)):
        raise ValueError("Simpson's rule requires uniformly spaced x values")

    return float(
        (h / 3.0)
        * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-1:2]))
    )


# =====================================================
# FUNCTION-BASED METHODS (f(x), [a,b], N)
# =====================================================

def trapezoidal_rule(f, a: float, b: float, N: int) -> float:
    """Composite trapezoidal rule for a function f on [a,b] using N subintervals."""
    if N <= 0:
        raise ValueError("N must be a positive integer")

    h = (b - a) / N
    x = np.linspace(a, b, N + 1)
    y = f(x)

    return float((h / 2.0) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1]))


def simpsons_rule(f, a: float, b: float, N: int) -> float:
    """Composite Simpson's 1/3 rule for a function f on [a,b] (N must be even)."""
    if N <= 0:
        raise ValueError("N must be a positive integer")
    if N % 2 != 0:
        raise ValueError("Simpson's rule requires N to be even")

    h = (b - a) / N
    x = np.linspace(a, b, N + 1)
    y = f(x)

    return float(
        (h / 3.0) * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-1:2]))
    )


# =====================================================
# STEP SIZE → N
# =====================================================

def n_from_step(a: float, b: float, h: float) -> int:
    """Convert step size h into number of subintervals N. Requires (b-a)/h to be an integer."""
    if h <= 0:
        raise ValueError("h must be positive")
    length = b - a
    if length <= 0:
        raise ValueError("b must be greater than a")

    N_float = length / h
    N = int(round(N_float))

    if N <= 0:
        raise ValueError("Computed N is not positive")
    if not np.isclose(N_float, N, atol=1e-9, rtol=1e-9):
        raise ValueError("h must evenly divide the interval (b-a)")

    return N
