import sqlite3

conn = sqlite3.connect("notifications.db")
cursor = conn.cursor()

def create_notifications_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_id INTEGER,
            content_type TEXT,
            content TEXT,
            caption TEXT,
            run_time TEXT,
            status TEXT,
            job_id TEXT
        )
    """)
    conn.commit()