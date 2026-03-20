from states import notification
from storage.notifications import conn, cursor

def add_notification(
    user_id,
    group_id,
    content_type,
    content,
    caption,
    run_time,
    status,
    job_id
    ):
    cursor.execute("""
        INSERT OR REPLACE INTO notifications (
            user_id, group_id, content_type, content,
            caption, run_time, status, job_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, group_id, content_type, content, caption, run_time, status, job_id))
    conn.commit()
    return cursor.lastrowid

def get_notification_byID(user_id, Notifid):
    cursor.execute("""
        SELECT * FROM notifications
        WHERE id = ? AND user_id = ?
    """, (Notifid, user_id,))
    notification = cursor.fetchone()

    if notification:
        return {
            "ID": notification[0],
            "user_id": notification[1],
            "group_id": notification[2],
            "content_type": notification[3],
            "content": notification[4],
            "caption": notification[5],
            "run_time": notification[6],
            "status": notification[7],
            "job_id": notification[8]
            }
    return {}

def get_notification_bytime(user_id, run_time):
    cursor.execute("""
        SELECT * FROM notifications
        WHERE user_id = ? AND run_time = ?
    """, (user_id, run_time,))
    notification = cursor.fetchone()

    if notification:
        return {
            "ID": notification[0],
            "user_id": notification[1],
            "group_id": notification[2],
            "content_type": notification[3],
            "content": notification[4],
            "caption": notification[5],
            "run_time": notification[6],
            "status": notification[7],
            "job_id": notification[8]
            }
    return {}

def get_notifications(user_id):
    cursor.execute("""
    SELECT * FROM notifications
    WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchall()

def remove_notification(user_id, Notif_id):
    cursor.execute("""
    DELETE FROM notifications
    WHERE user_id = ? AND id = ?
    """, (user_id, Notif_id,))
    conn.commit()

def update_status(user_id, notif_id, status):
    cursor.execute("""
    UPDATE notifications SET status = ?
    WHERE id = ? AND user_id = ?
    """, (status, notif_id, user_id))
    conn.commit()

def update_job_id(user_id, notif_id, job_id):
    cursor.execute("""
    UPDATE notifications SET job_id = ?
    WHERE id = ? AND user_id = ?
    """, (job_id, notif_id, user_id))
    conn.commit()