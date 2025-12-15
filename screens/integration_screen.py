from textual.screen import Screen
from textual.widgets import Label, Input, Button, Static
from textual.containers import VerticalScroll
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import sympy as sp

import integration as integ
import utils


class IntegrationScreen(Screen):
    CSS_PATH = str(Path(__file__).parent / "static_and_label.tcss")
    """A screen for entering data points and calculating the integrated value."""

    def compose(self):

        # VerticalScroll guarantees scrolling
        with VerticalScroll(id="menu-container"):

            yield Label("Estimate Rate of a Body of Mass' Change in Temperature", id="title") 

            # Context Box
            yield Static(
                "[bold]Numerical Integration Context[/bold]\n"
                "This page estimates the rate of a body's change in thermal energy.\n",
                classes="context-box"
            )

            # -------- Mode A: Experimental Data --------
            yield Label("Mode A: Experimental Data (Time and Temperature values)")
            self.x_input = Input(placeholder="Time values (s) (e.g., 0, 1, 2, 3)")
            self.y_input = Input(placeholder="Temperature values (°C) (e.g., 0, 1, 4, 9)")
            yield self.x_input
            yield self.y_input


            # -------- Mode B: Analytical Model --------
            yield Label("Mode B: Analytical Model (Temperature Model f(x), Start Time, End Time, Time Step)")
            yield Static(
                "Use SymPy syntax: sin(x), exp(x), x**2\n"
                "(avoid np.sin / np.exp in input)",
                classes="status",
            )

            self.f_input = Input(placeholder="Temperature Model f(x) (e.g., x**2, sin(x))")
            self.a_input = Input(placeholder="Start Time (e.g., 0)")
            self.b_input = Input(placeholder="End Time (e.g., 3)")
            self.h_input = Input(placeholder="Time Step h (e.g., 0.5)")
            yield self.f_input
            yield self.a_input
            yield self.b_input
            yield self.h_input


            # -------- Method Buttons --------
            yield Button("Estimate Change in Thermal Energy (Trapezoidal Rule)", id="trap")
            yield Button("Estimate Change in Thermal Energy (Simpson's 1/3 Rule)", id="simp")
            yield Button("Show Plot", id="show_plot")
            yield Label("---") 
            yield Button("Back to Main Menu", id="back")

            self.output = Static("Waiting for input...", classes="status")
            yield self.output

    # =====================================================
    # HELPERS
    # =====================================================

    def _parse_cs_string(self, text: str) -> np.ndarray:
        vals = [v.strip() for v in text.split(",") if v.strip() != ""]
        if not vals:
            raise ValueError("Input cannot be empty.")          
        return np.array([float(v) for v in vals], dtype=float)

    def _has_points_mode(self) -> bool:
        return bool(self.x_input.value.strip()) and bool(self.y_input.value.strip())

    def _has_function_mode(self) -> bool:
        return (
            bool(self.f_input.value.strip())
            and bool(self.a_input.value.strip())
            and bool(self.b_input.value.strip())
            and bool(self.h_input.value.strip())
        )

    # =====================================================
    # EVENTS
    # =====================================================

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
            return

        try:
            points = self._has_points_mode()
            func = self._has_function_mode()

            if points and func:
                raise ValueError("Use only ONE mode: clear either (Time and Temperature values) OR (Temperature Model f(x), Start Time, End Time, Time Step).")

            # If the user wants to view the plot, require a previously computed result
            if event.button.id == "show_plot":
                if not hasattr(self, "last_plot"):
                    self.output.update("❌ **Error:** Please compute an integration first before plotting.")
                    return

                if self.last_plot[0] == "points":
                    _, Xp, Yp, mname = self.last_plot
                    integ.plot(Xp, Yp, method_name=mname)
                    self.output.update(f"📈 Plot opened in a separate window using the {mname} method.")
                    return

                if self.last_plot[0] == "function":
                    _, f_np_p, a_p, b_p, h_p, mname = self.last_plot
                    integ.plot(f_np_p, a_p, b_p, h_p, method_name=mname)
                    self.output.update(f"📈 Plot opened in a separate window using the {mname} method.")
                    return

            if not points and not func:
                raise ValueError("Provide either (Time and Temperature values) OR (Temperature Model f(x), Start Time, End Time, Time Step).")

            # -------- Mode A: Experimental Data --------
            if points:
                X = self._parse_cs_string(self.x_input.value)
                Y = self._parse_cs_string(self.y_input.value)

                if len(X) != len(Y):
                    raise ValueError("Time and Temperature must have the same number of values.")
                if len(X) < 2:
                    raise ValueError("At least two data points are required.")

                order = np.argsort(X)
                X = X[order]
                Y = Y[order]

                if np.any(np.diff(X) <= 0):
                    raise ValueError("Time values must be strictly increasing.")

                if event.button.id == "trap":
                    approx = integ.trapezoidal_from_points(X, Y)
                    method = "Trapezoidal Rule (points)"
                    utils.latest_results["method_b"] = approx
                    utils.latest_results["description"] = "Symbolic vs Trapezoidal Rule (points)"
                    # Store last plot args for Show Plot
                    self.last_plot = ("points", X, Y, method)
                    self.last_plot_name = method

                else:
                    approx = integ.simpsons_from_points(X, Y)
                    method = "Simpson's 1/3 Rule (points)"
                    utils.latest_results["method_b"] = approx
                    utils.latest_results["description"] = "Symbolic vs Simpson's 1/3 Rule (points)"
                    # Store last plot args for Show Plot
                    self.last_plot = ("points", X, Y, method)
                    self.last_plot_name = method



                # No exact solution for arbitrary data → use trapezoid as reference
                ref = integ.trapezoidal_from_points(X, Y)
                err = utils.relative_error(approx, ref)

                utils.latest_results["method_a"] = ref

                self.output.update(
                    f"Method: {method}\n"
                    f"Time: {X.tolist()}\n"
                    f"Temperature: {Y.tolist()}\n"
                    f"---\n"
                    f"Approx Area: {approx:.10f}\n"
                    f"Reference (Trapezoid): {ref:.10f}\n"
                    f"Relative Error (vs ref): {err:.4e}"
                )
                return

            # -------- Mode B: Function --------
            f_str = self.f_input.value.strip().replace("np.", "")
            a = float(self.a_input.value)
            b = float(self.b_input.value)
            h = float(self.h_input.value)

            x = sp.symbols("x")
            f_expr = sp.sympify(f_str)
            f_np = sp.lambdify(x, f_expr, "numpy")

            N = integ.n_from_step(a, b, h)

            if event.button.id == "trap":
                approx = integ.trapezoidal_rule(f_np, a, b, N)
                method = "Trapezoidal Rule (function)"
                utils.latest_results["method_b"] = approx
                utils.latest_results["description"] = "Symbolic vs Trapezoidal Rule (function)"
                # Store last plot args for Show Plot
                self.last_plot = ("function", f_np, a, b, h, method)
                self.last_plot_name = method

            else:
                approx = integ.simpsons_rule(f_np, a, b, N)
                method = "Simpson's 1/3 Rule (function)"
                utils.latest_results["method_b"] = approx
                utils.latest_results["description"] = "Symbolic vs Simpson's 1/3 Rule (function)"
                # Store last plot args for Show Plot
                self.last_plot = ("function", f_np, a, b, h, method)
                self.last_plot_name = method


            exact = float(sp.N(sp.integrate(f_expr, (x, a, b))))
            err = utils.relative_error(approx, exact)

            utils.latest_results["method_a"] = exact

            self.output.update(
                f"Method: {method}\n"
                f"Temperature Model = {f_expr}\n"
                f"Time Interval: [{a}, {b}]\n"
                f"Time Step = {h}  (N = {N})\n"
                f"---\n"
                f"Approx Area: {approx:.10f}\n"
                f"Exact Area: {exact:.10f}\n"
                f"Relative Error: {err:.4e}"
            )
            return

        except Exception as e:
            self.output.update(f"[red]Error:[/red] {e}")
