import numpy as np
import matplotlib.pyplot as plt

def divided_differences(X, Y):
    """
    Calculates the divided difference coefficients for Newton's form.
    
    Args:
        X (list/np.array): x-coordinates of data points.
        Y (list/np.array): y-coordinates of data points.
        
    Returns:
        np.array: The coefficients (f[x0], f[x0, x1], f[x0, x1, x2], ...)
    """
    n = len(X)
    # Create the divided difference table (size n x n)
    F = np.zeros((n, n))
    # The first column is the y-values (zeroth-order differences)
    F[:, 0] = Y
    
    # Calculate higher-order differences
    for j in range(1, n):
        for i in range(n - j):
            # The general formula for the k-th order difference:
            # F[i, k] = ( F[i+1, k-1] - F[i, k-1] ) / ( X[i+k] - X[i] )
            numerator = F[i + 1, j - 1] - F[i, j - 1]
            denominator = X[i + j] - X[i]
            F[i, j] = numerator / denominator
            
    # The coefficients are the top diagonal of the table
    return F[0, :]

def newton_interpolation(x, X, Y):
    """
    Evaluates the Newton interpolating polynomial at a given point x.
    
    Args:
        x (float): The point at which to evaluate the polynomial.
        X (list/np.array): x-coordinates of data points.
        Y (list/np.array): y-coordinates of data points.
        
    Returns:
        float: The interpolated value at x.
    """
    n = len(X)
    coeffs = divided_differences(X, Y)
    
    # Evaluate the Newton polynomial using Horner's method
    result = coeffs[-1]
    for k in range(n - 2, -1, -1):
        result = result * (x - X[k]) + coeffs[k]
        
    return result


def lagrange_interpolation(x, X, Y):
    total = 0
    n = len(X)
    for i in range(n):
        term = Y[i]
        for j in range(n):
            if j != i:
                term *= (x - X[j]) / (X[i] - X[j])
        total += term
    return total


def plot(X, Y, method):
    xs = np.linspace(min(X), max(X), 100)
    ys = [method(x, X, Y) for x in xs]

    plt.scatter(X, Y, label="Data")
    plt.plot(xs, ys, label="Interpolation / Extrapoolation")
    plt.xlabel("Time")
    plt.ylabel("Temperature")   
    plt.legend()
    plt.show()
