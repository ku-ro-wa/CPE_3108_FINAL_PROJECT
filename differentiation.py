import numpy as np
import matplotlib.pyplot as plt


def forward_difference(f, x, h):
    """
    Calculates the derivative of function f at point x using the
    forward difference method with step size h.
    """
    return (f(x + h) - f(x)) / h


def backward_difference(f, x, h):
    """
    Calculates the derivative of function f at point x using the
    backward difference method with step size h.
    """
    return (f(x) - f(x - h)) / h


def central_difference(f, x, h):
    """
    Calculates the derivative of function f at point x using the
    central difference method with step size h.
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def plot(f, x, h, method):
    """Plot the function and numerical derivative approximation.

    Args:
        f: callable, function f(x)
        x: float, center point to view around
        h: float, step size used by numerical method
        method: callable(f, x_point, h) -> derivative estimate
    """
    # Choose a window for plotting around the chosen x
    span = max(1.0, 10.0 * abs(h))
    xs = np.linspace(x - span / 2.0, x + span / 2.0, 400)

    # function values and derivative approximations
    fxs = np.array([f(xi) for xi in xs])
    approx_deriv = np.array([method(f, xi, h) for xi in xs])

    # Numerical derivative (reference) computed from the sampled f values
    # using central differences on the dense grid
    num_deriv = np.gradient(fxs, xs)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax1.plot(xs, fxs, label="Temperature f(x)")
    ax1.scatter([x], [f(x)], color="k", zorder=5, label="Evaluation Point")
    ax1.set_ylabel("Temperature")
    ax1.legend()

    ax2.plot(xs, num_deriv, label="Numerical d/dx (gradient)")
    ax2.plot(xs, approx_deriv, '--', label=f"Approx ({method.__name__})")
    ax2.scatter([x], [method(f, x, h)], color="k", zorder=5, label="Approx at x")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("dT/dt")
    ax2.legend()

    fig.suptitle(f"Derivative approximation using {method.__name__}")
    plt.tight_layout()
    plt.show()