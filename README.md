# CPE 3108: Programming Project

## Thermal Cooling and Heating Analysis Tool

The Thermal Cooling and Heating Analysis Tool is a Python-based numerical methods application that analyzes the thermal behavior of a body over time using numerical techniques when closed-form analytical solutions are difficult or unavailable. It focuses on estimating temperature values, rates of temperature change, and thermal energy variation using interpolation, differentiation, and integration methods, with additional error analysis for model accuracy.
The application is implemented as an interactive Textual (TUI) program, allowing users to select different numerical operations through a menu-driven interface.

### Features
Interpolation & Extrapolation:
  - Newton’s Divided Differences Method (supports higher-degree polynomials using multiple data points)
  - Lagrange Interpolation Method
  - Graphical visualization of interpolated or extrapolated temperature profiles
Numerical Differentiation:
  - Forward Divided Difference Method
  - Backward Divided Difference Method
  - Central Divided Difference Method
  - Comparison between numerical derivative and symbolic derivative using SymPy
Numerical Integration:
  - Trapezoidal Rule (tabulated data and function-based)
  - Simpson’s 1/3 Rule (tabulated data and function-based)
  - Automatic conversion of step size to number of subintervals
Error Analysis:
  - Absolute error computation
  - Relative error computation
  - Comparison between numerical and symbolic (exact) solutions

### Limitations
  - Numerical accuracy depends on step size and number of data points
  - Simpson’s Rule requires evenly spaced data and an even number of subintervals
  - Extrapolation may produce large errors outside the known data range
  - Graph plots open in a separate window and require a graphical backend

### Input
  The program accepts the following inputs depending on the selected module:
  - Time and temperature data points (comma-separated)
  - Analytical temperature models using SymPy syntax (e.g., x**2, sin(x))
  - Time interval, step size, and evaluation point

### Output
  The program outputs:
  - Estimated temperature values
  - Estimated cooling/heating rates (dT/dt)
  - Estimated thermal energy change (area under curve)
  - Absolute and relative errors
  - Heating or cooling state interpretation
  - Graphical plots for interpolation and extrapolation
