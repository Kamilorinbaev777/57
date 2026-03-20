from storage.user_group import conn, cursor

def add_user_group(user_id, group_id, title):
    cursor.execute("""
    INSERT OR REPLACE INTO user_groups (user_id, group_id, title) VALUES (?, ?, ?)    
    """, (user_id, group_id, title))
    conn.commit()

def get_user_group(user_id, group_id):
    cursor.execute("""
    SELECT * FROM user_groups WHERE user_id = ? AND group_id = ?
    """, (user_id, group_id))
    
    user_group = cursor.fetchone()

    if user_group:
        return {
            "user_id": user_group[0],
            "group_id": user_group[1],
            "title": user_group[2]
            }
    return {}

def get_users_groups(user_id):
    cursor.execute("""
    SELECT * FROM user_groups WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchall()

def delete_user_group(user_id, group_id):
    cursor.execute("""
    DELETE FROM user_groups WHERE user_id = ? AND group_id = ?
    """,(user_id, group_id))
    conn.commit()