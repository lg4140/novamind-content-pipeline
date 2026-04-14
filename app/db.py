import sqlite3

DB_PATH = "data/app.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        blog_title TEXT,
        content_json_path TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS campaign_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        blog_title TEXT,
        persona_segment TEXT,
        contact_email TEXT,
        newsletter_subject TEXT,
        hubspot_email_id TEXT,
        hubspot_send_status_id TEXT,
        send_status TEXT,
        send_date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        persona_segment TEXT,
        recipient_count INTEGER,
        open_count INTEGER,
        click_count INTEGER,
        unsubscribe_count INTEGER,
        open_rate REAL,
        click_rate REAL,
        unsubscribe_rate REAL,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        summary_text TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()




