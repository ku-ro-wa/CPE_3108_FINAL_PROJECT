from textual.app import App
from textual.widgets import Static, Label, Button, Input
from textual.containers import Container
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import interpolation_screen as interp_screen
import differentiation_screen as diff_screen
import integration_screen as integ_screen



class TextualApp(App):
    CSS_PATH = str(Path(__file__).parent / "static_and_label.tcss")

    def compose(self):
        
        with Container(id="menu-container"):
            # Title
            yield Label("Thermal Simulation Operations", id="title")
            
            # Buttons
            yield Button("1. Interpolation", id="interp-btn")
            yield Button("2. Extrapolation", id="extrap-btn")
            yield Button("3. Numerical Differentiation", id="diff-btn")
            yield Button("4. Numerical Integration", id="integ-btn")
            yield Button("5. Error Analysis", id="error-btn")
            yield Button("0. Exit", id="exit-btn")
            
            # Inputs
            self.status_display = Static("Waiting for selection...", classes="status")
            yield self.status_display
            
            yield Static(
                "[bold] Alternatively, enter the number: [/bold]",
                id="static_prompt"
            )

            # Store the input field reference for later
            self.operation_input = Input( 
                placeholder="Enter 0-5 and press Enter",
                type="number",
                tooltip="Enter a number between 0 and 5",
            )
            yield self.operation_input


            # --- 1. Define the Action for Button Presses ---
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called automatically when any Button is pressed."""
        
        # event.button is the actual Button widget that was pressed
        button_id = event.button.id
        
        if button_id == "btn_exit":
            self.exit("Application manually exited.")
        else:
            # Update the status display (the 'self.status_display' Static widget)
            self.status_display.update(f"You selected: **{event.button.label}** (ID: {button_id})")
            

            # Button logic (function calling, etc)
            match button_id:
                case "interp-btn":
                    self.push_screen(interp_screen.InterpolationScreen())
                case "extrap-btn":
                    self.push_screen(interp_screen.InterpolationScreen())
                case "diff-btn":
                    self.push_screen(diff_screen.DifferentiationScreen())
                case "integ-btn":
                    self.push_screen(integ_screen.IntegrationScreen())



    # --- 2. Define the Action for Input Submission ---
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Called automatically when the user presses Enter in the Input field."""
        
        # event.value contains the text/number the user entered
        user_input = event.value
        
        # Basic validation (e.g., checking if it's a number between 0 and 5)
        try:
            op_num = int(user_input)
        except ValueError:
            self.status_display.update(f"[red]Error:[/red] '{user_input}' is not a valid number.")
            return

        # Handle the selection based on the number
        if 0 <= op_num <= 5:
            if op_num == 0:
                self.exit("Application exited via number input.")
            else:
                operation_names = {
                    1: "Interpolation", 2: "Extrapolation", 3: "Numerical Differentiation",
                    4: "Numerical Integration", 5: "Error Analysis"
                }
                
                operation_name = operation_names.get(op_num, "Unknown Operation")
                
                self.status_display.update(
                    f"You entered option **{op_num}**: {operation_name}."
                )
                
        else:
            self.status_display.update(
                f"[red]Error:[/red] The number {op_num} is outside the valid range (0-5)."
            )
        
        # Clear the input field after submission
        self.operation_input.clear()      


if __name__ == "__main__":
    app = TextualApp()
    app.run()
