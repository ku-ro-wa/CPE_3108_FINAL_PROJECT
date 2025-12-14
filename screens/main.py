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

            # Status display
            self.status_display = Static("Waiting for selection...", classes="status")
            yield self.status_display

            yield Static("[bold] Alternatively, enter the number: [/bold]", id="static_prompt")

            # Input field
            self.operation_input = Input(
                placeholder="Enter 0-5 and press Enter",
                type="number",
                tooltip="Enter a number between 0 and 5",
            )
            yield self.operation_input

    # --- Button presses ---
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        # Exit
        if button_id == "exit-btn":
            self.exit("Application manually exited.")
            return

        # Update status display
        self.status_display.update(f"You selected: **{event.button.label}** (ID: {button_id})")

        # Route to screens
        match button_id:
            case "interp-btn":
                self.push_screen(interp_screen.InterpolationScreen())
            case "extrap-btn":
                # Using same screen for now (your current setup)
                self.push_screen(interp_screen.InterpolationScreen())
            case "diff-btn":
                self.push_screen(diff_screen.DifferentiationScreen())
            case "integ-btn":
                self.push_screen(integ_screen.IntegrationScreen())
            case "error-btn":
                self.status_display.update("Error Analysis screen not implemented yet.")

    # --- Input submission (press Enter) ---
    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()

        try:
            op_num = int(user_input)
        except ValueError:
            self.status_display.update(f"[red]Error:[/red] '{user_input}' is not a valid number.")
            self.operation_input.clear()
            return

        if op_num < 0 or op_num > 5:
            self.status_display.update(
                f"[red]Error:[/red] The number {op_num} is outside the valid range (0-5)."
            )
            self.operation_input.clear()
            return

        # Route based on number
        match op_num:
            case 0:
                self.exit("Application exited via number input.")
                return
            case 1:
                self.status_display.update("Opening Interpolation...")
                self.push_screen(interp_screen.InterpolationScreen())
            case 2:
                self.status_display.update("Opening Extrapolation...")
                self.push_screen(interp_screen.InterpolationScreen())
            case 3:
                self.status_display.update("Opening Numerical Differentiation...")
                self.push_screen(diff_screen.DifferentiationScreen())
            case 4:
                self.status_display.update("Opening Numerical Integration...")
                self.push_screen(integ_screen.IntegrationScreen())
            case 5:
                self.status_display.update("Error Analysis screen not implemented yet.")

        # Clear the input after handling
        self.operation_input.clear()


if __name__ == "__main__":
    app = TextualApp()
    app.run()
