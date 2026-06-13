"""
tasks.py — Task & deadline manager.
Owned by: Member C (Tasks)

Screen 3 of 5. Add tasks with a due date, mark them done, delete them.
Uses grid() layout and a ttk.Treeview to list tasks responsively.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db


class TasksScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app

        # Make the table area expand when the window resizes
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Button(header, text="← Back", command=lambda: app.show_screen("dashboard")).pack(side="left")
        ttk.Label(header, text="Task Manager", font=("Helvetica", 18, "bold")).pack(side="left", padx=12)

        # --- Input row ---
        form = ttk.Frame(self)
        form.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(form, text="Task").grid(row=0, column=0, padx=4)
        self.title = ttk.Entry(form, width=30)
        self.title.grid(row=0, column=1, padx=4)
        ttk.Label(form, text="Due (YYYY-MM-DD)").grid(row=0, column=2, padx=4)
        self.due = ttk.Entry(form, width=14)
        self.due.grid(row=0, column=3, padx=4)
        ttk.Button(form, text="Add", command=self.add).grid(row=0, column=4, padx=4)

        # --- Task list ---
        self.tree = ttk.Treeview(
            self, columns=("title", "due", "status"), show="headings", height=10
        )
        self.tree.heading("title", text="Task")
        self.tree.heading("due", text="Due date")
        self.tree.heading("status", text="Status")
        self.tree.column("status", width=90, anchor="center")
        self.tree.grid(row=2, column=0, sticky="nsew")

        # --- Action buttons ---
        actions = ttk.Frame(self)
        actions.grid(row=3, column=0, sticky="ew", pady=12)
        ttk.Button(actions, text="Toggle Done", command=self.toggle).pack(side="left", padx=4)
        ttk.Button(actions, text="Delete", command=self.remove).pack(side="left", padx=4)

    def on_show(self):
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for t in db.get_tasks(self.app.user_id):
            status = "✓ Done" if t["done"] else "Pending"
            self.tree.insert("", "end", iid=t["id"], values=(t["title"], t["due_date"], status))

    def add(self):
        title = self.title.get().strip()
        if not title:
            messagebox.showwarning("Missing", "Please enter a task title.")
            return
        db.add_task(self.app.user_id, title, self.due.get().strip())
        self.title.delete(0, tk.END)
        self.due.delete(0, tk.END)
        self.refresh()

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select a task first.")
            return None
        return int(sel[0])

    def toggle(self):
        task_id = self._selected_id()
        if task_id:
            db.toggle_task(task_id)
            self.refresh()

    def remove(self):
        task_id = self._selected_id()
        if task_id:
            db.delete_task(task_id)
            self.refresh()
