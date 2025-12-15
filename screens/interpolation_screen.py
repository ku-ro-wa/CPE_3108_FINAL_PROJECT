from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import VerticalScroll
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import interpolation as interp 

class InterpolationScreen(Screen):
    CSS_PATH = str(Path(__file__).parent / "static_and_label.tcss")
    """A screen for entering data points and calculating the interpolated/extrapolated value."""

    def compose(self):
        
        # VerticalScroll guarantees scrolling
        with VerticalScroll(id="menu-container"):

            yield Label("Estimate / Predict Temperature of Body of Mass", id="title")     

            # Context Box
            yield Static(
                "[bold]Interpolation/Extrapolation Context[/bold]\n"
                "This page estimates the temperature of a body at a specified point in time.\n"
                "It can also estimate temperature at times outside the known data range.\n",
                classes="context-box"
            )
        
            yield Label("Note: For temperature prediction, enter time value to evaluate outside the range of the time data points.")

            # Inputs for the known data points (X and Y)
            self.x_data_input = Input(placeholder="Time data (s) (comma-separated, e.g., 1, 2, 3)")
            self.y_data_input = Input(placeholder="Temperature data (°C) (comma-separated, e.g., 0, 1, 0)")
            
            # New input for the single point to evaluate (x)
            self.x_eval_input = Input(placeholder="Time value to evaluate at (e.g., 1.5)")
            
            yield self.x_data_input
            yield self.y_data_input 
            yield self.x_eval_input
            

            yield Button("Estimate/Predict Temperature Using Divided Differences Method", id="compute_divided")
            yield Button("Estimate/Predict Temperature Using Lagrange Method", id="compute_lagrange")
            yield Button("Show Plot", id="show_plot")

            yield Label("---") 
            yield Button("Back to Main Menu", id="back_to_main")
            
            self.output = Static("Waiting for input...", classes="status")
            yield self.output


    def on_button_pressed(self, event):
        if event.button.id == "back_to_main":
            self.app.pop_screen()
            return
        
        try:
            # Parse the data points X and Y
            X = list(map(float, self.x_data_input.value.split(",")))
            Y = list(map(float, self.y_data_input.value.split(",")))

            # Error checking for data points
            if len(X) != len(Y):
                raise ValueError("Time and Temperature data points must have the same length.")
            if len(X) < 2:
                raise ValueError("At least two data points are required.")
            if len(set(X)) != len(X):
                raise ValueError("Time values must be distinct.")

            # Parse the single evaluation point x
            x_eval = float(self.x_eval_input.value)
            result_value = 0
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

            # Determine Heating or Cooling state
            state = "Stable"

            if (result_value > 0):
                state = "Heating"
            elif (result_value < 0):
                state = "Cooling"

            # Show plot if requested
            if event.button.id == "show_plot":
                # Check if a method was previously computed and stored
                if not hasattr(self, 'last_method'):
                     self.output.update("❌ **Error:** Please compute an interpolation/extrapolation first before plotting.")
                     return # Exit function before formatting block

                # Use the last computed method for plotting
                interp.plot(X, Y, self.last_method)
                self.output.update(f"📈 Plot opened in a separate window using the {self.last_method_name} method.")
                return

            # Update Output 
            output_text = (
                f"Method: {method_name}\n"
                f"Operation: {mode}\n"
                f"Polynomial degree: {degree}\n"
                f"Time data points: {X}\n"
                f"Temperature data points: {Y}\n"
                f"Interpolated/Extrapolated value at time: {x_eval}\n"
                f"Result: {result_value:0.6f}"
                f"\nThe body is currently {state}"
            )
            self.output.update(output_text)

        except ValueError:
            self.output.update("❌  **Error:** Please ensure all inputs are valid numbers separated by commas (or a single number for evaluated time).")
        except IndexError:
            self.output.update("❌  **Error:** Please ensure you have entered an equal number of time and temperature data points.")
        except ZeroDivisionError:
            self.output.update("❌  **Error:** Time data points must be unique. The current data points will cause division by zero.")