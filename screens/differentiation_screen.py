from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import Container
from textual.containers import VerticalScroll
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import differentiation as diff 
import utils
import numpy as np
import sympy as sp


class DifferentiationScreen(Screen):
    """A screen for entering data points and calculating the differentiated value."""

    def compose(self):
        # VerticalScroll guarantees scrolling
        with VerticalScroll(id="menu-container"):
            yield Label("Numerical Differentiation – Enter Data Points")

            # Context Box
            yield Static(
                """
                [bold]Numerical Differentiation Context[/bold]
                This page estimates the Cooling/Heating rate of a body.
                Newton's Law of Cooling: dT/dt ∝ (T - Tₐ)
                The numerical derivative approximates this rate using experimental data.
                """,
                classes="context-box"
            )
            
            # Inputs for the known data points (X and Y)
            self.f_data_input = Input(placeholder="Temperature at time x (f(x)) (SymPy format, e.g., sin(x), x**2 + 3*x + 2)")
            yield Label(
                "Note: Use SymPy syntax (e.g., sin(x), exp(x), x**2). Avoid prefixing with 'np.'."
            )
            self.x_data_input = Input(placeholder="Data point time (s) (e.g., 1.0)")
            self.h_data_input = Input(placeholder="Time interval between measurements (s) (e.g., 0.01)")
            
            yield self.f_data_input
            yield self.x_data_input
            yield self.h_data_input
            yield Label("---") 

            yield Button("Cooling / Heating Rate (dT/dt) using Backward Divided Difference", id="compute_backward")
            yield Button("Cooling / Heating Rate (dT/dt) using Forward Divided Difference", id="compute_forward")
            yield Button("Cooling / Heating Rate (dT/dt) usingCentral Divided Difference", id="compute_central")

            yield Label("---") 
            yield Button("Back to Main Menu", id="back_to_main")

            self.output = Static("")
            yield self.output

    def on_button_pressed(self, event):
        if event.button.id == "back_to_main":
            self.app.pop_screen()
            return
        
        
        try:
            X = float(self.x_data_input.value)
            H = float(self.h_data_input.value)
            
            # Convert the function string input into a callable function
            f_str = self.f_data_input.value

            # Symbolic (True) differentiation setup
            # Define the symbol 'x' for SymPy
            x_sym = sp.symbols('x') 

            # Attempt to parse the user's input as a SymPy expression.
            # If the user prepended 'np.' (from NumPy), try to strip it before parsing.
            if 'np.' in f_str:
                # Convert np.sin(x) -> sin(x) for SymPy parsing
                f_str_for_sympy = f_str.replace('np.', '')
            else:
                f_str_for_sympy = f_str

            # Convert the user's string to a SymPy expression
            f_expr = sp.sympify(f_str_for_sympy)

            # Symbolic derivative expression
            df_expr = sp.diff(f_expr, x_sym)

            # Convert SymPy expressions into NumPy-callable functions for numerical work and evaluation
            f_np = sp.lambdify(x_sym, f_expr, 'numpy')
            f_prime_np = sp.lambdify(x_sym, df_expr, 'numpy')

            # Calculate the exact derivative value at point X
            exact_value = float(f_prime_np(X))

            approx_value = 0
            method_name = ""

            if event.button.id == "compute_backward":
                approx_value = diff.backward_difference(f_np, X, H)
                method_name = "Backward Divided Difference"
                utils.latest_results["method_b"] = approx_value
                utils.latest_results["description"] = "Symbolic vs Backward Divided Difference"

            elif event.button.id == "compute_forward":
                approx_value = diff.forward_difference(f_np, X, H)
                method_name = "Forward Divided Difference"
                utils.latest_results["method_b"] = approx_value
                utils.latest_results["description"] = "Symbolic vs Forward Divided Difference"
            
            elif event.button.id == "compute_central":
                approx_value = diff.central_difference(f_np, X, H)
                method_name = "Central Divided Difference"
                utils.latest_results["method_b"] = approx_value
                utils.latest_results["description"] = "Symbolic vs Central Divided Difference"
                

            # Calculate the relative error (after approx_value set)
            relative_err = utils.relative_error(approx_value, exact_value)

            utils.latest_results["method_a"] = exact_value

            # Determine Heating or Cooling state
            state = "Stable"

            if (approx_value > 0 or exact_value > 0):
                state = "Heating"
            elif (approx_value < 0 or exact_value < 0):
                state = "Cooling"
            

            output_text = (
                f"Method: {method_name}\n"
                f"Temperature at Time x, Function f(x) = {f_expr}\n"
                f"Rate of Temperature Change, True Derivative f'(x) = {df_expr}\n"
                f"--- \n"
                f"At Time={X} with Time Interval={H}:\n"
                f"Approximate Rate of Temperature Change ≈ {approx_value:0.8f}\n"
                f"Exact Rate of Temperature Change = {exact_value:0.8f}\n"
                f"Relative Error: {relative_err:0.4e}\n"
                f"The body is currently: {state} at a rate of {approx_value:0.8f} (°C/s)\n"
            )
            self.output.update(output_text)

        except (ValueError, NameError, TypeError, SyntaxError, sp.SympifyError) as e:
            # Catches errors from float conversion, or eval() parsing the function string
            error_message = f"❌ **Error:** Invalid input.\nDetails: {e}"
            self.output.update(error_message)