"""
stats.py — Statistics & settings screen.
Owned by: Member E (Stats / Database)

Screen 5 of 5. Shows simple stats from the database and draws a tiny
bar chart on a Canvas (no external charting library needed).
Uses pack() + grid() layout.
"""

import tkinter as tk
from tkinter import ttk

import db


class StatsScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 16))
        ttk.Button(header, text="← Back", command=lambda: app.show_screen("dashboard")).pack(side="left")
        ttk.Label(header, text="Statistics", font=("Helvetica", 18, "bold")).pack(side="left", padx=12)

        # Numeric summary cards
        self.cards = ttk.Frame(self)
        self.cards.pack(fill="x", pady=(0, 16))

        # Canvas bar chart drawn by hand
        self.canvas = tk.Canvas(self, height=220, background="#f4f4f8", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def on_show(self):
        self.render()

    def render(self):
        stats = db.get_stats(self.app.user_id)

        # Rebuild the summary cards
        for child in self.cards.winfo_children():
            child.destroy()
        labels = [
            ("Total tasks", stats["tasks_total"]),
            ("Completed", stats["tasks_done"]),
            ("Pending", stats["tasks_pending"]),
            ("Notes", stats["notes_total"]),
        ]
        for i, (label, value) in enumerate(labels):
            self.cards.columnconfigure(i, weight=1)
            card = ttk.Frame(self.cards, relief="ridge", padding=12)
            card.grid(row=0, column=i, padx=6, sticky="ew")
            ttk.Label(card, text=str(value), font=("Helvetica", 22, "bold")).pack()
            ttk.Label(card, text=label).pack()

        # Draw a simple bar chart
        self.canvas.delete("all")
        data = [
            ("Done", stats["tasks_done"], "#4caf50"),
            ("Pending", stats["tasks_pending"], "#ff9800"),
            ("Notes", stats["notes_total"], "#2196f3"),
        ]
        max_val = max((v for _, v, _ in data), default=0) or 1
        bar_width = 80
        gap = 60
        base_y = 190
        for i, (label, value, color) in enumerate(data):
            x0 = 60 + i * (bar_width + gap)
            x1 = x0 + bar_width
            height = int((value / max_val) * 150)
            y0 = base_y - height
            self.canvas.create_rectangle(x0, y0, x1, base_y, fill=color, width=0)
            self.canvas.create_text((x0 + x1) / 2, base_y + 14, text=label)
            self.canvas.create_text((x0 + x1) / 2, y0 - 12, text=str(value), font=("Helvetica", 11, "bold"))
