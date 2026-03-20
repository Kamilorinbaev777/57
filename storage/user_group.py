import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def create_usergroup_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_groups (
        user_id INTEGER,
        group_id INTEGER,
        title TEXT,
        PRIMARY KEY (user_id, group_id)
    )
    """)
    conn.commit()