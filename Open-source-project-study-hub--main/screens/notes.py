"""
notes.py — Notes / flashcards screen.
Owned by: Member D (Notes)

Screen 4 of 5. Create notes with a title + body, search them, delete them.
Uses grid() layout with a Listbox + Text editor side by side.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db


class NotesScreen(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=20)
        self.app = app

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ttk.Button(header, text="← Back", command=lambda: app.show_screen("dashboard")).pack(side="left")
        ttk.Label(header, text="Notes", font=("Helvetica", 18, "bold")).pack(side="left", padx=12)

        # --- Search ---
        search_row = ttk.Frame(self)
        search_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        ttk.Label(search_row, text="Search").pack(side="left", padx=4)
        self.search = ttk.Entry(search_row)
        self.search.pack(side="left", padx=4)
        self.search.bind("<KeyRelease>", lambda e: self.refresh())

        # --- Note list (left) ---
        self.listbox = tk.Listbox(self, width=28, exportselection=False)
        self.listbox.grid(row=2, column=0, sticky="ns", padx=(0, 12))
        self.listbox.bind("<<ListboxSelect>>", self.show_selected)

        # --- Editor (right) ---
        editor = ttk.Frame(self)
        editor.grid(row=2, column=1, sticky="nsew")
        editor.columnconfigure(0, weight=1)
        editor.rowconfigure(1, weight=1)

        self.title_entry = ttk.Entry(editor)
        self.title_entry.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        self.title_entry.insert(0, "Title...")

        self.body = tk.Text(editor, height=12, wrap="word")
        self.body.grid(row=1, column=0, sticky="nsew")

        btns = ttk.Frame(self)
        btns.grid(row=3, column=1, sticky="ew", pady=8)
        ttk.Button(btns, text="Save New", command=self.save).pack(side="left", padx=4)
        ttk.Button(btns, text="Delete Selected", command=self.remove).pack(side="left", padx=4)

        self._rows = []  # keeps id <-> listbox index mapping

    def on_show(self):
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self._rows = db.get_notes(self.app.user_id, self.search.get().strip())
        for note in self._rows:
            self.listbox.insert(tk.END, note["title"])

    def show_selected(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        note = self._rows[sel[0]]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note["title"])
        self.body.delete("1.0", tk.END)
        self.body.insert("1.0", note["body"] or "")

    def save(self):
        title = self.title_entry.get().strip()
        if not title or title == "Title...":
            messagebox.showwarning("Missing", "Please enter a note title.")
            return
        db.add_note(self.app.user_id, title, self.body.get("1.0", tk.END).strip())
        self.refresh()

    def remove(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Select", "Select a note first.")
            return
        db.delete_note(self._rows[sel[0]]["id"])
        self.refresh()
