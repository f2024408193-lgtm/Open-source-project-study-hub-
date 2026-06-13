"""
dashboard.py — Home / navigation screen.
Owned by: Member B (Group Lead — navigation & layout)

Screen 2 of 5. Shows a greeting and big buttons that navigate to the
Tasks, Notes, and Stats screens. Uses pack() layout.
"""

import tkinter as tk
from tkinter import ttk


class DashboardScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=40)
        self.app = app

        self.greeting = ttk.Label(self, text="", font=("Helvetica", 22, "bold"))
        self.greeting.pack(pady=(0, 6))

        ttk.Label(
            self, text="What would you like to do today?", font=("Helvetica", 12)
        ).pack(pady=(0, 30))

        # Navigation buttons — each opens another member's screen
        nav = ttk.Frame(self)
        nav.pack()

        buttons = [
            ("📝  Task Manager", "tasks"),
            ("📒  Notes", "notes"),
            ("📊  Statistics", "stats"),
        ]
        for text, screen_name in buttons:
            ttk.Button(
                nav,
                text=text,
                width=30,
                command=lambda s=screen_name: self.app.show_screen(s),
            ).pack(pady=8, ipady=8)

        ttk.Button(self, text="Log Out", command=self.app.logout).pack(pady=(30, 0))

    def on_show(self):
        """Called by the app each time this screen becomes visible."""
        self.greeting.config(text=f"Hello, {self.app.username} 👋")
