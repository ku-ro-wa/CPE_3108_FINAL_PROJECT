from textual.app import App
from textual.widgets import Static, Label, Button, Input

class TextualApp(App):
    CSS_PATH = "static_and_label.tcss"

    def compose(self):
        #Title
        yield Label("Thermal Simulation Operations", id="title")
        # Buttons
        yield Button("1. Interpolation")
        yield Button("2. Extrapolation")
        yield Button("3. Numerical Differentiation")
        yield Button("4. Numerical Integration")
        yield Button("5. Error Analysis")
        yield Button("0. Exit")
        # Inputs
        self.static = Static(
            "[bold] Alternatively, you can enter the number of the desired operation: [/bold]"

        )
        yield self.static
        yield Input(
            placeholder="Enter the number of the desired operation",
            type="number",
            tooltip="Enter a number between 0 and 5",
        )
        

if __name__ == "__main__":
    app = TextualApp()
    app.run()