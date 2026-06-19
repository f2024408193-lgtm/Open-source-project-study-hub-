# 📚 StudyHub — Collaborative Tkinter Study Companion

> Final Term Project — Open Source Software Development (OSSD), CLO 4
> A multi-screen desktop GUI application built with Python + Tkinter, backed by SQLite,
> developed collaboratively on GitHub using feature branches, pull requests, and code reviews.

---

## 📖 Short Description
**StudyHub** is a desktop productivity app for students. After logging in, a user can manage
their tasks and deadlines, keep searchable notes, and view simple statistics about their
study progress — all from a clean, responsive Tkinter interface.

## ✨ Feature Summary
| Feature | Description |
|---|---|
| 🔐 **Login / Register** | Create an account and log in. Passwords are SHA-256 hashed. |
| 🏠 **Dashboard** | Central navigation hub with a personal greeting. |
| 📝 **Task Manager** | Add tasks with due dates, mark them done, delete them. |
| 📒 **Notes** | Create, search, and delete notes (title + body). |
| 📊 **Statistics** | Summary cards + a hand-drawn bar chart of your activity. |

- ✅ **5 screens** (exceeds the 3-screen minimum)
- ✅ Uses **all three layout managers** across screens (`pack`, `grid`, `place`-ready)
- ✅ **Responsive** — windows resize cleanly via `rowconfigure` / `columnconfigure`
- ✅ **Data persistence** with **SQLite**

## 🛠️ Tools & Technologies
- **Frontend:** Python **Tkinter** (`ttk` themed widgets)
- **Backend / Storage:** **SQLite** (via the standard-library `sqlite3` module)
- **Language:** Python 3.8+
- **Version Control:** Git + GitHub (public repo, feature branches, PRs, Issues)

## 🚀 Setup & Running

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/studyhub.git
cd studyhub

# 2. (Optional) create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. No external packages needed — stdlib only.
#    If tkinter is missing on Linux:  sudo apt-get install python3-tk

# 4. Run the app
python3 main.py
```

The SQLite database (`studyhub.db`) is created automatically on first run.

## 📂 Project Structure
```
studyhub/
├── main.py              # App entry point + screen router
├── db.py                # Shared SQLite data layer
├── requirements.txt
├── README.md
└── screens/
    ├── login.py         # Screen 1 — Auth
    ├── dashboard.py     # Screen 2 — Navigation
    ├── tasks.py         # Screen 3 — Task manager
    ├── notes.py         # Screen 4 — Notes
    └── stats.py         # Screen 5 — Statistics
```

## 🖼️ Screenshots / GIFs
> Add screenshots here before submission (rubric requires them).
> Suggested: `docs/login.png`, `docs/dashboard.png`, `docs/tasks.png`, `docs/notes.png`, `docs/stats.png`

| Login | Dashboard | Tasks |
|---|---|---|
| _screenshot_ | _screenshot_ | _screenshot_ |

## 👥 Contribution Credits
| Member | Role | Module(s) | Branch |
|---|---|---|---|
| Member A | Authentication | `screens/login.py` | `feature/auth` |
| Member B | **Group Lead** — Navigation & layout | `screens/dashboard.py`, `main.py` | `feature/dashboard` |
| Member C | Task Manager | `screens/tasks.py` | `feature/tasks` |
| Member D | Notes | `screens/notes.py` | `feature/notes` |
| Member E | Stats & Database | `screens/stats.py`, `db.py` | `feature/stats-db` |
| Member F | Documentation and Testing and Quality assurance| `reature/doc-testing`
> Replace "Member A–F" with real names + GitHub handles before submitting.

## 🔗 Major PRs & Issues
> Fill in after development (rubric requires these links):
- Issue #1 — Project plan & task breakdown
- PR #__ — Authentication screen
- PR #__ — Dashboard & navigation
- PR #__ — Task manager
- PR #__ — Notes
- PR #__ — Statistics & database layer

## 🗄️ Backend Explanation
StudyHub uses **SQLite**, a serverless file-based database bundled with Python.
All data access is centralized in [`db.py`](db.py), which exposes helper functions for
auth, tasks, notes, and stats. Three tables are used:

- `users (id, username, password)` — credentials, password stored as a SHA-256 hash
- `tasks (id, user_id, title, due_date, done)` — per-user tasks
- `notes (id, user_id, title, body)` — per-user notes

Foreign keys link tasks and notes to their owning user, so deleting a user cascades.

---
*Built for educational purposes as part of the OSSD course.*
# Open-source-project-study-hub-
