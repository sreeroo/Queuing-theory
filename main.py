import tkinter as tk
from tkinter import ttk
from view.input_frame import InputFrame
from view.result_frame import ResultFrame
from view.plot_frame import PlotFrame
from controller.queue_controller import QueueController


class QueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warteschlangentheorie-Analysator")
        self.plot_frame = None
        self._configure_styles()
        self._create_scrollable_ui()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#2d2d2d', foreground='white')
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TButton', background='#3d3d3d')
        style.configure('TEntry', fieldbackground='white', foreground='black')
        style.map('TButton', background=[('active', '#4d4d4d')])

    def _create_scrollable_ui(self):
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(container, bg='#2d2d2d', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all"))
                                   )

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_frame = InputFrame(self.scrollable_frame, self._on_calculate)
        self.result_frame = ResultFrame(self.scrollable_frame)
        self.plot_container = ttk.Frame(self.scrollable_frame)

        self.input_frame.pack(pady=10, padx=15, fill=tk.X)
        self.result_frame.pack(pady=10, padx=15, fill=tk.X)
        self.plot_container.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_calculate(self, params):
        if self.plot_frame:
            self.plot_frame.get_tk_widget().destroy()
        self.plot_frame = PlotFrame(self.plot_container)
        self.controller = QueueController(self.input_frame, self.result_frame, self.plot_frame)
        self.controller.handle_calculation(params)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.configure(bg='#2d2d2d')
    app = QueueApp(root)
    root.mainloop()