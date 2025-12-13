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