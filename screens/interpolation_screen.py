from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import Container
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import interpolation as interp 

class InterpolationScreen(Screen):
    """A screen for entering data points and calculating the interpolated value."""

    def compose(self):
        yield Label("Lagrange Interpolation – Enter Data Points")
        
        # Inputs for the known data points (X and Y)
        self.x_data_input = Input(placeholder="X data points (comma-separated, e.g., 1, 2, 3)")
        self.y_data_input = Input(placeholder="Y data points (comma-separated, e.g., 0, 1, 0)")
        
        # New input for the single point to evaluate (x)
        self.x_eval_input = Input(placeholder="x value to evaluate at (e.g., 1.5)")
        
        yield self.x_data_input
        yield self.y_data_input
        yield Label("---") 
        yield self.x_eval_input
        
        yield Button("Compute Interpolated Value", id="compute")
        
        self.output = Static("")
        yield self.output

    def on_button_pressed(self, event):
        if event.button.id == "compute":
            try:
                # 1. Parse the data points X and Y
                X = list(map(float, self.x_data_input.value.split(",")))
                Y = list(map(float, self.y_data_input.value.split(",")))

                # 2. Parse the single evaluation point x
                x_eval = float(self.x_eval_input.value)

                # --- 3. Function Call ---
                result_value = interp.lagrange_interpolation(x_eval, X, Y)

                # --- 4. Update Output ---
                output_text = (
                    f"**Result**\n"
                    f"Interpolated value at $\\mathbf{{x={x_eval}}}$:\n"
                    f"$\\mathbf{{P({x_eval}) \\approx {result_value:0.6f}}}$"
                )
                self.output.update(output_text)

            except ValueError:
                self.output.update("❌ **Error:** Please ensure all inputs are valid numbers separated by commas (or a single number for x).")
            except IndexError:
                self.output.update("❌ **Error:** Please ensure you have entered an equal number of X and Y data points.")
            except ZeroDivisionError:
                self.output.update("❌ **Error:** X data points must be unique. The current data points will cause division by zero.")