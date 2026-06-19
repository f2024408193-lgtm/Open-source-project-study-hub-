"""
tasks.py

Unit Tests and Documentation for the StudyHub Task Manager Module
Owned By: Member F (Testing & Quality Assurance)

This file validates:

1. User Registration
2. User Authentication
3. Task CRUD Operations
4. Notes Management
5. Statistics Generation
6. SQL Injection Protection
7. Multi-User Data Isolation
8. Database Initialization




def test_notes_creation(self):
    """
    Verify note creation and retrieval.
    """

    ok, _ = db.register_user("note_user", "pass")
    self.assertTrue(ok)

    user_id = db.login_user("note_user", "pass")
    self.assertIsNotNone(user_id)

    db.add_note(
        user_id,
        "Meeting Notes",
        "Discuss project milestones"
    )

    notes = db.get_notes(user_id)

    self.assertEqual(len(notes), 1)
    self.assertEqual(
        notes[0]["title"],
        "Meeting Notes"
    )


def test_multiple_tasks(self):
    """
    Verify multiple tasks can be added.
    """

    ok, _ = db.register_user("multi_user", "pass")
    self.assertTrue(ok)

    user_id = db.login_user("multi_user", "pass")

    db.add_task(user_id, "Task 1", "2026-01-01")
    db.add_task(user_id, "Task 2", "2026-01-02")
    db.add_task(user_id, "Task 3", "2026-01-03")

    tasks = db.get_tasks(user_id)

    self.assertEqual(len(tasks), 3)


def test_user_data_isolation(self):
    """
    Ensure users only see their own tasks.
    """

    db.register_user("user1", "pass")
    db.register_user("user2", "pass")

    user1 = db.login_user("user1", "pass")
    user2 = db.login_user("user2", "pass")

    db.add_task(
        user1,
        "Private Task",
        "2026-05-01"
    )

    tasks_user1 = db.get_tasks(user1)
    tasks_user2 = db.get_tasks(user2)

    self.assertEqual(len(tasks_user1), 1)
    self.assertEqual(len(tasks_user2), 0)
