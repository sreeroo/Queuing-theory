import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

class PlotFrame:
    def __init__(self, parent):
        plt.style.use('dark_background')
        self.figure = plt.figure(
            figsize=(10, 8),
            facecolor='#2d2d2d',
            constrained_layout=True
        )
        self.figure.set_constrained_layout_pads(
            w_pad=0.3,
            h_pad=0.3,
            hspace=0.3,
            wspace=0.3
        )
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self._create_subplots()
        self._setup_responsiveness(parent)

    def _create_subplots(self):
        self.ax1 = self.figure.add_subplot(221)
        self.ax2 = self.figure.add_subplot(222)
        self.ax3 = self.figure.add_subplot(223)
        self.ax4 = self.figure.add_subplot(224)
        self._configure_axes()

    def _configure_axes(self):
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_facecolor('#3d3d3d')
            ax.title.set(color='white', fontsize=9)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(colors='white', labelsize=7)
            for spine in ax.spines.values():
                spine.set_color('white')

    def _setup_responsiveness(self, parent):
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        parent.bind("<Configure>", self._on_resize)

    def _on_resize(self, event=None):
        if event:
            width = event.width / 100
            height = event.height / 100
            self.figure.set_size_inches(width, height)
            self.canvas.draw_idle()

    def update_plots(self, model, n=None):
        self._clear_plots()
        self._plot_probability_distribution(model)
        self._plot_utilization_effects(model)
        self._plot_waiting_time_curve(model)
        self._plot_metrics_comparison(model)
        self.canvas.draw()

    def _clear_plots(self):
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            self._configure_axes()

    def _plot_probability_distribution(self, model):
        n_values = np.arange(0, 15)
        probabilities = [model.probability(n) for n in n_values]
        self.ax1.bar(n_values, probabilities, color='#4ecdc4')
        self.ax1.set_title("Wahrscheinlichkeitsverteilung", pad=10)
        self.ax1.set_xlabel("Anzahl Kunden im System")
        self.ax1.set_ylabel("Wahrscheinlichkeit")


    def _plot_utilization_effects(self, model):
        ρ_values = np.linspace(0.1, 0.95, 50)
        Lq_values = (ρ_values ** 2) / (1 - ρ_values)
        self.ax2.plot(ρ_values, Lq_values, color='#ff6b6b')
        self.ax2.set_title("Auslastung vs Warteschlangenlänge", pad=10)
        self.ax2.set_xlabel("Auslastung (ρ)")
        self.ax2.set_ylabel("Durchschn. Schlangenlänge(n_schlange)")



    def _plot_waiting_time_curve(self, model):
        λ_values = np.linspace(0.1, model.μ * 0.95, 50)
        valid_values = λ_values[λ_values < model.μ]
        Wq_values = valid_values / (model.μ * (model.μ - valid_values))
        self.ax3.plot(valid_values, Wq_values, color='#ffe66d')
        self.ax3.set_title("Ankunftsrate vs Wartezeit", pad=10)
        self.ax3.set_xlabel("Ankunftsrate (λ)")
        self.ax3.set_ylabel("Mittlere. Wartezeit (W)")

    def _plot_metrics_comparison(self, model):
        metrics = [
            'Mittlere Kundenzahl',
            'Durchschn. Schlangenlänge',
            'Mittlere Aufenthaltsdauer',
            'Mittlere. Wartezeit'
        ]
        values = [
            model.avg_system_customers,
            model.avg_queue_length,
            model.avg_time_system,
            model.avg_waiting_time
        ]
        self.ax4.bar(metrics, values, color=['#4ecdc4', '#ff6b6b', '#ffe66d', '#45b7d1'])
        self.ax4.set_title("Systemkennzahlen Vergleich", pad=10)
        self.ax4.set_xlabel("Kennzahl")
        self.ax4.set_ylabel("Wert")

        self.ax4.tick_params(axis='x', rotation=15)

        for i, v in enumerate(values):
            self.ax4.text(i, v + 0.05, f"{v:.2f}",
                          color='white', ha='center', fontsize=8)

    def get_tk_widget(self):
        return self.canvas.get_tk_widget()