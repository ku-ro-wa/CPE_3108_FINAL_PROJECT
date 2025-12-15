from textual.screen import Screen
from textual.widgets import Label, Button, Static
from textual.containers import VerticalScroll
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import utils

class ErrorScreen(Screen):
    CSS_PATH = str(Path(__file__).parent / "static_and_label.tcss")
    """A screen for displaying error analysis results."""

    def compose(self):

            yield Label("Error Analysis Results", id="title")
            yield Label("Comparison of Numerical Results")

            self.output = Static("No data available.", id="error_output")
            yield self.output

            yield Button("Back to Main Menu", id="back_to_main")
            # Only one output widget should exist; keep the initial one above


    async def on_mount(self):

        """Populate the error analysis when screen loads."""
        # Debug message to confirm the handler runs when the screen mounts
        print("[debug] ErrorScreen.on_mount called")

        a = utils.latest_results.get("method_a")
        b = utils.latest_results.get("method_b")
        desc = utils.latest_results.get("description", "")

        if a is None or b is None:
            # Update the existing output widget
            self.output.update("⚠️  No numerical results available for error analysis. Please perform computations first.")
            return

        abs_error = utils.absolute_error(a, b)
        rel_error = utils.relative_error(a, b) if b != 0 else float("inf")

        loss_msg = ""
        if abs_error < 1e-6 and abs(a) > 1:
            loss_msg = "\n⚠️    Possible loss of significance detected."

        rel_error_percent = rel_error * 100 if b != 0 else float("inf")

        # Update the already-mounted widget instead of creating a new one
        self.output.update(
            f"{desc}\n\n"
            f"Symbolic Calculation Result: {a:.6f}\n"
            f"Numerical Calculation Result: {b:.6f}\n\n"
            f"Temperature Error (°C): {abs_error:.6e}\n"
            f"Thermal Model Deviation (%): {rel_error:.6e}, ({rel_error_percent}%)\n"
            f"{loss_msg}"
        )


    def on_button_pressed(self, event):
        if event.button.id == "back_to_main":
            self.app.pop_screen()