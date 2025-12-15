import numpy as np
import differentiation as diff
import integration as integ

# Example 1: Differentiation
# f(x) = sin(x), center x=1.0, h=0.1
f = np.sin
x0 = 1.0
h = 0.05
print("Showing differentiation plot...")
diff.plot(f, x0, h, diff.central_difference)

# Example 2: Integration from points
X = np.array([0.0, 1.0, 2.0, 3.0])
Y = np.array([0.0, 1.0, 4.0, 9.0])
print("Showing integration plot from points...")
integ.plot(X, Y, method_name="trapezoidal")

# Example 3: Integration of function
print("Showing integration plot for function x**2 on [0,3] with h=1.0...")
integ.plot(lambda t: t**2, 0.0, 3.0, 1.0, method_name="trapezoidal")
        