"""
main.py — Application entry point for StudyHub.

Run with:   python3 main.py

This file creates the main window and manages switching between the five
screens. Each screen is a separate module owned by a different team member,
so everyone can work on their own file / feature branch without conflicts.
"""

import tkinter as tk
from tkinter import ttk

import db
from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.tasks import TasksScreen
from screens.notes import NotesScreen
from screens.stats import StatsScreen


class StudyHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StudyHub")
        self.geometry("780x560")
        self.minsize(640, 480)

        # Make the app theme a little nicer where available
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        # Session state, set after a successful login
        self.user_id = None
        self.username = None

        # A single container holds whichever screen is active
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.screens = {}
        self.show_login()

    # ---------- Screen management ----------

    def _clear(self):
        for child in self.container.winfo_children():
            child.destroy()
        self.screens = {}

    def show_login(self):
        self._clear()
        screen = LoginScreen(self.container, self)
        screen.grid(row=0, column=0, sticky="nsew")

    def _build_main_screens(self):
        """Create the post-login screens once the user is known."""
        self._clear()
        self.screens = {
            "dashboard": DashboardScreen(self.container, self),
            "tasks": TasksScreen(self.container, self),
            "notes": NotesScreen(self.container, self),
            "stats": StatsScreen(self.container, self),
        }
        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

    def show_screen(self, name):
        """Raise a screen to the front and refresh its data."""
        screen = self.screens[name]
        if hasattr(screen, "on_show"):
            screen.on_show()
        screen.tkraise()

    # ---------- Auth callbacks ----------

    def login_success(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self._build_main_screens()
        self.show_screen("dashboard")

    def logout(self):
        self.user_id = None
        self.username = None
        self.show_login()


if __name__ == "__main__":
    db.init_db()
    app = StudyHubApp()
    app.mainloop()
