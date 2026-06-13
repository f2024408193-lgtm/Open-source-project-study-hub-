"""
login.py — Login / Register screen.
Owned by: Member A (Authentication)

Screen 1 of 5. Uses grid() layout. Lets a user register or log in.
On success it calls app.login_success(user_id, username) to switch screens.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db


class LoginScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=40)
        self.app = app

        # Let the single column stretch when the window is resized (responsive)
        self.columnconfigure(0, weight=1)

        title = ttk.Label(self, text="StudyHub", font=("Helvetica", 28, "bold"))
        title.grid(row=0, column=0, pady=(0, 4))

        subtitle = ttk.Label(self, text="Your study companion", font=("Helvetica", 12))
        subtitle.grid(row=1, column=0, pady=(0, 24))

        form = ttk.Frame(self)
        form.grid(row=2, column=0)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=4)
        self.username = ttk.Entry(form, width=28)
        self.username.grid(row=1, column=0, pady=(0, 12))

        ttk.Label(form, text="Password").grid(row=2, column=0, sticky="w", pady=4)
        self.password = ttk.Entry(form, width=28, show="*")
        self.password.grid(row=3, column=0, pady=(0, 20))

        ttk.Button(form, text="Log In", command=self.handle_login).grid(
            row=4, column=0, sticky="ew", pady=4
        )
        ttk.Button(form, text="Register", command=self.handle_register).grid(
            row=5, column=0, sticky="ew", pady=4
        )

        # Pressing Enter logs in
        self.password.bind("<Return>", lambda event: self.handle_login())

    def handle_login(self):
        user_id = db.login_user(self.username.get().strip(), self.password.get())
        if user_id:
            self.app.login_success(user_id, self.username.get().strip())
        else:
            messagebox.showerror("Login failed", "Invalid username or password.")

    def handle_register(self):
        ok, message = db.register_user(
            self.username.get().strip(), self.password.get()
        )
        if ok:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Could not register", message)
