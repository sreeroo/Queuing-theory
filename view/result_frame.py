import tkinter as tk
from tkinter import ttk


class ResultFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Ergebnisse")
        self.metrics = {}
        self._create_widgets()

    def _create_widgets(self):
        # Configure column weights for expansion
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Increase label widths and use wraplength
        self._add_metric_row('Auslastung (ρ):', 'utilization', 0, 0)
        self._add_metric_row('Mittlere Kundenzahl (n_sys):', 'avg_system', 0, 1)
        self._add_metric_row('Durchschn. Schlangenlänge (n_schlange):', 'avg_queue', 1, 0)
        self._add_metric_row('Mittlere Aufenthaltsdauer (T):', 'time_system', 1, 1)
        self._add_metric_row('Mittlere. Wartezeit (W):', 'waiting_time', 2, 0)
        self._add_metric_row('Wahrscheinlichkeit n in System P(n):', 'prob_n', 2, 1)

    def _add_metric_row(self, label_text, key, row, column):
        frame = ttk.Frame(self)
        frame.grid(row=row, column=column, padx=10, pady=5, sticky=tk.W + tk.E)

        # Configure label with wrapping and proper alignment
        lbl = ttk.Label(
            frame,
            text=label_text,
            width=25,
            anchor=tk.W,
            wraplength=400,  # Allows text wrapping if needed
            font=('Segoe UI', 9)
        )
        lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.metrics[key] = ttk.Label(
            frame,
            text="",
            width=12,
            anchor=tk.E,
            font=('Segoe UI', 9, 'bold')
        )
        self.metrics[key].pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_results(self, results):
        for key, label in self.metrics.items():
            value = results.get(key)
            display_text = f"{value:.4f}" if isinstance(value, float) else str(value) if value else "N/A"
            label.config(text=display_text)