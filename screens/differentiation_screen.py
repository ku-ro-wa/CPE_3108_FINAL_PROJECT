from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import Container
import differentiation as diff 

class DifferentiationScreen(Screen):

    def compose(self):
        yield Label("Numerical Differentiation – Enter Data Points")
        
        # Inputs for the known data points (X and Y)
        self.x_data_input = Input(placeholder="X data points (comma-separated, e.g., 1, 2, 3)")
        self.y_data_input = Input(placeholder="Y data points (comma-separated, e.g., 0, 1, 0)")
        
        # New input for the single point to evaluate (x)
        self.x_eval_input = Input(placeholder="x value to evaluate derivative at (e.g., 1.5)")
        
        yield self.x_data_input
        yield self.y_data_input
        yield Label("---") 
        yield self.x_eval_input
        
        yield Button("Compute Derivative", id="compute")
        
        self.output = Static("")
        yield self.output