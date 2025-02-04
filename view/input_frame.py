import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk


class ModernEntry(ttk.Frame):
    def __init__(self, parent, label_text, **kwargs):
        super().__init__(parent)
        self.label_text = label_text
        self._create_widgets()
        self._setup_style()

    def _create_widgets(self):
        self.canvas = tk.Canvas(self, height=48, highlightthickness=0, bg='#2d2d2d',width=400)
        self.canvas.pack(fill=tk.X)

        self.entry_frame = ttk.Frame(self.canvas)
        self.entry = ttk.Entry(
            self.entry_frame,
            font=('Segoe UI', 10),
            style='Modern.TEntry',
            width=40,
        )

        self.label = ttk.Label(
            self.entry_frame,
            text=self.label_text,
            font=('Segoe UI', 9),
            foreground='#888888',
            background='#2d2d2d',
            wraplength=400,
            justify=tk.LEFT,
        )

        self.canvas.create_window(10, 24, window=self.entry_frame, anchor=tk.W)
        self.label.place(x=12, y=14)
        self.entry.pack(fill=tk.X, padx=10, pady=(20, 5), ipady=3)

        # Bind events
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<KeyRelease>', self._update_label_position)

    def _setup_style(self):
        style = ttk.Style()
        style.configure('Modern.TEntry',
                        foreground='white',
                        fieldbackground='#3d3d3d',
                        borderwidth=0,
                        relief='flat',
                        padding=(5, 8)
                        )
        style.map('Modern.TEntry',
                  fieldbackground=[('active', '#454545')],
                  foreground=[('active', 'white')]
                  )

    def _on_focus_in(self, event):
        self.label.config(foreground='#4ecdc4', font=('Segoe UI', 8))
        self.label.place(y=8)
        self.canvas.config(bg='#454545')

    def _on_focus_out(self, event):
        if not self.entry.get():
            self.label.config(foreground='#888888', font=('Segoe UI', 9))
            self.label.place(y=14)
        self.canvas.config(bg='#2d2d2d')

    def _update_label_position(self, event):
        if self.entry.get():
            self.label.place(y=8)
        else:
            self.label.place(y=14)

    def get(self):
        return self.entry.get()


class InputFrame(ttk.LabelFrame):
    def __init__(self, parent, calculate_callback):
        super().__init__(parent, text="Eingabeparameter")
        self.calculate_callback = calculate_callback
        self._create_widgets()

    def _create_widgets(self):
        # Arrival Rate
        self.arrival_entry = ModernEntry(self, "Ankunftsrate (λ)")
        self.arrival_entry.pack(fill=tk.X, padx=15, pady=5)

        # Service Rate
        self.service_entry = ModernEntry(self, "Bedienrate (μ)")
        self.service_entry.pack(fill=tk.X, padx=15, pady=5)

        # Optional n
        self.n_entry = ModernEntry(self, "Wahrscheinlichkeit n Kunden in System (optional)")
        self.n_entry.pack(fill=tk.X, padx=15, pady=5)

        # Modern Button
        btn = ttk.Button(
            self,
            text="Berechnen",
            style='Modern.TButton',
            command=self._on_calculate
        )
        btn.pack(pady=15, padx=15, fill=tk.X)

        # Configure styles
        self._setup_styles()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure('Modern.TButton',
                        font=('Segoe UI', 10, 'bold'),
                        foreground='white',
                        background='#4ecdc4',
                        borderwidth=0,
                        padding=8,
                        relief='flat'
                        )
        style.map('Modern.TButton',
                  background=[('active', '#45b7d1'), ('disabled', '#3d3d3d')]
                  )

    def _on_calculate(self):
        try:
            params = {
                'arrival_rate': float(self.arrival_entry.get()),
                'service_rate': float(self.service_entry.get()),
                'n': self.n_entry.get() or None
            }
            if params['n'] is not None:
                params['n'] = int(params['n'])
            self.calculate_callback(params)
        except ValueError as e:
            self._show_error(str(e))

    def _show_error(self, message):
        tk.messagebox.showerror("Eingabefehler", message)
