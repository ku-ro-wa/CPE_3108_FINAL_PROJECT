from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import Container
import integration as integ 

class IntegrationScreen(Screen):

    def compose(self):
        yield Label("Numerical Integration – Enter Data Points")
        
        # Inputs for the known data points (X and Y)
        self.x_data_input = Input(placeholder="X data points (comma-separated, e.g., 1, 2, 3)")
        self.y_data_input = Input(placeholder="Y data points (comma-separated, e.g., 0, 1, 0)")
        
        # New input for the limits of integration
        self.a_input = Input(placeholder="Lower limit of integration (a)")
        self.b_input = Input(placeholder="Upper limit of integration (b)")
        
        yield self.x_data_input
        yield self.y_data_input
        yield Label("---") 
        yield self.a_input
        yield self.b_input
        
        yield Button("Compute Integral", id="compute")
        
        self.output = Static("")
        yield self.output