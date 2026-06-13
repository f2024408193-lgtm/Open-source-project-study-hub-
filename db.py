"""
db.py — Shared SQLite data layer for StudyHub.
Owned by: Member E (Database / Stats)

All screens import from this module so the database logic lives in one place.
This keeps feature branches independent and avoids merge conflicts.
"""

import os
import sqlite3
import hashlib

# Database file lives next to this script
DB_PATH = os.path.join(os.path.dirname(__file__), "studyhub.db")


def get_connection():
    """Return a SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they do not exist. Safe to call on every startup."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL,
            title    TEXT NOT NULL,
            due_date TEXT,
            done     INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title   TEXT NOT NULL,
            body    TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()


# ---------- Auth helpers (Member A) ----------

def _hash(password):
    """Hash a password so plain text is never stored in the database."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(username, password):
    """Create a new user. Returns (ok, message)."""
    if not username or not password:
        return False, "Username and password are required."
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, _hash(password)),
        )
        conn.commit()
        return True, "Account created. You can log in now."
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    finally:
        conn.close()


def login_user(username, password):
    """Validate credentials. Returns user_id on success, else None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT id, password FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    if row and row["password"] == _hash(password):
        return row["id"]
    return None


# ---------- Task helpers (Member C) ----------

def add_task(user_id, title, due_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (user_id, title, due_date) VALUES (?, ?, ?)",
        (user_id, title, due_date),
    )
    conn.commit()
    conn.close()


def get_tasks(user_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY done, due_date", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def toggle_task(task_id):
    conn = get_connection()
    conn.execute("UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# ---------- Note helpers (Member D) ----------

def add_note(user_id, title, body):
    conn = get_connection()
    conn.execute(
        "INSERT INTO notes (user_id, title, body) VALUES (?, ?, ?)",
        (user_id, title, body),
    )
    conn.commit()
    conn.close()


def get_notes(user_id, search=""):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM notes WHERE user_id = ? AND title LIKE ? ORDER BY id DESC",
        (user_id, f"%{search}%"),
    ).fetchall()
    conn.close()
    return rows


def delete_note(note_id):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


# ---------- Stats helpers (Member E) ----------

def get_stats(user_id):
    """Return counts used by the Stats screen."""
    conn = get_connection()
    tasks_total = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    tasks_done = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND done = 1", (user_id,)
    ).fetchone()[0]
    notes_total = conn.execute(
        "SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    conn.close()
    return {
        "tasks_total": tasks_total,
        "tasks_done": tasks_done,
        "tasks_pending": tasks_total - tasks_done,
        "notes_total": notes_total,
    }
