import numpy as np

def trapezoidal_rule(f, a, b, N):
    """
    Calculates the definite integral of function f from a to b 
    using the compound Trapezoidal Rule with N subintervals.
    
    Args:
        f (function): The function to integrate.
        a (float): The lower limit of integration.
        b (float): The upper limit of integration.
        N (int): The number of subintervals (trapezoids).
        
    Returns:
        float: The approximate value of the integral.
    """
    if N <= 0:
        raise ValueError("N must be a positive integer.")
    
    # Calculate the width of each subinterval
    h = (b - a) / N
    
    # Generate the points (x_0, x_1, ..., x_N)
    x = np.linspace(a, b, N + 1)
    
    # Calculate the function values at these points
    y = f(x)
    
    # The sum formula: f(x_0) + 2*sum(f(x_1) to f(x_{N-1})) + f(x_N)
    # The middle terms (y[1] to y[N-1]) are multiplied by 2
    integral = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    
    return integral


def simpsons_rule(f, a, b, N):
    """
    Calculates the definite integral of function f from a to b 
    using the compound Simpson's 1/3 Rule with N subintervals.
    
    NOTE: N must be an even number.
    
    Args:
        f (function): The function to integrate.
        a (float): The lower limit of integration.
        b (float): The upper limit of integration.
        N (int): The number of subintervals (must be EVEN).
        
    Returns:
        float: The approximate value of the integral.
    """
    if N % 2 != 0 or N <= 0:
        raise ValueError("N must be an even positive integer for Simpson's 1/3 Rule.")
        
    # Calculate the width of each subinterval
    h = (b - a) / N
    
    # Generate the points
    x = np.linspace(a, b, N + 1)
    y = f(x)
    
    # Simpson's sum formula: coefficients are (1, 4, 2, 4, 2, ..., 4, 1)
    # y[0] and y[-1] are 1 (endpoints)
    # y[1::2] are odd indices (coefficient 4)
    # y[2:-1:2] are even indices excluding endpoints (coefficient 2)
    
    integral = (h / 3) * (y[0] + 
                          4 * np.sum(y[1:-1:2]) +  # Sum of f(x) at odd indices
                          2 * np.sum(y[2:-1:2]) +  # Sum of f(x) at even indices
                          y[-1])
    
    return integral

