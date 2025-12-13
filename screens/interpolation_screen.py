from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import Container
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import interpolation as interp 
import utils

class InterpolationScreen(Screen):
    """A screen for entering data points and calculating the interpolated value."""

    def compose(self):
        yield Label("Lagrange Interpolation/Extrapolation – Enter Data Points")    
        yield Label("Note: For extrapolation, enter x value outside the range of X data points.")

        # Inputs for the known data points (X and Y)
        self.x_data_input = Input(placeholder="X data points (comma-separated, e.g., 1, 2, 3)")
        self.y_data_input = Input(placeholder="Y data points (comma-separated, e.g., 0, 1, 0)")
        
        # New input for the single point to evaluate (x)
        self.x_eval_input = Input(placeholder="x value to evaluate at (e.g., 1.5)")
        
        yield self.x_data_input
        yield self.y_data_input 
        yield self.x_eval_input
        

        yield Button("Compute Using Divided Differences Method", id="compute_divided")
        yield Button("Compute Using Lagrange Method", id="compute_lagrange")
        yield Button("Show Plot", id="show_plot")

        yield Label("---") 
        yield Button("Back to Main Menu", id="back_to_main")
        
        self.output = Static("")
        yield self.output


    def on_button_pressed(self, event):
        if event.button.id == "back_to_main":
            self.app.pop_screen()
            return
        
        try:
            # 1. Parse the data points X and Y
            X = list(map(float, self.x_data_input.value.split(",")))
            Y = list(map(float, self.y_data_input.value.split(",")))

            # Error checking for data points
            if len(X) != len(Y):
                raise ValueError("X and Y must have the same length.")
            if len(X) < 2:
                raise ValueError("At least two data points are required.")
            if len(set(X)) != len(X):
                raise ValueError("X values must be distinct.")


            # 2. Parse the single evaluation point x
            x_eval = float(self.x_eval_input.value)
            result_value = None
            method_name = ""
            degree = len(X) - 1


            if x_eval < min(X) or x_eval > max(X):
                mode = "Extrapolation"
            else:
                mode = "Interpolation"

            if event.button.id == "compute_divided":
                result_value = interp.newton_interpolation(x_eval, X, Y)
                method_name = "Divided Differences"
                # Store the last used method for plotting
                self.last_method = interp.newton_interpolation 
                self.last_method_name = method_name

            elif event.button.id == "compute_lagrange":
                result_value = interp.lagrange_interpolation(x_eval, X, Y)
                method_name = "Lagrange"
                # Store the last used method for plotting
                self.last_method = interp.lagrange_interpolation
                self.last_method_name = method_name

            # 3. Show plot if requested
            if event.button.id == "show_plot":
                # Check if a method was previously computed and stored
                if not hasattr(self, 'last_method'):
                     self.output.update("❌ **Error:** Please compute an interpolation/extrapolation first before plotting.")
                     return # Exit function before formatting block

                # Use the last computed method for plotting
                interp.plot(X, Y, self.last_method)
                self.output.update(f"📈 Plot opened in a separate window using the {self.last_method_name} method.")
                return

            # --- 4. Update Output ---
            output_text = (
                f"Method: {method_name}\n"
                f"Operation: {mode}\n"
                f"Polynomial degree: {degree}\n"
                f"X data points: {X}\n"
                f"Y data points: {Y}\n"
                f"Interpolated/Extrapolated value at x: {x_eval}\n"
                f"Result: {result_value:0.6f}"
            )
            self.output.update(output_text)

        except ValueError:
            self.output.update("❌ **Error:** Please ensure all inputs are valid numbers separated by commas (or a single number for x).")
        except IndexError:
            self.output.update("❌ **Error:** Please ensure you have entered an equal number of X and Y data points.")
        except ZeroDivisionError:
            self.output.update("❌ **Error:** X data points must be unique. The current data points will cause division by zero.")