import random
from datetime import datetime,UTC
from app.db import get_conn

def simulate_metrics(topic: str) -> list[dict]:
    records = [
        {
            "topic": topic,
            "persona_segment": "ops_lead",
            "open_rate": round(random.uniform(0.38, 0.48), 3),
            "click_rate": round(random.uniform(0.08, 0.14), 3),
            "unsubscribe_rate": round(random.uniform(0.005, 0.015), 3),
        },
        {
            "topic": topic,
            "persona_segment": "creative_director",
            "open_rate": round(random.uniform(0.34, 0.44), 3),
            "click_rate": round(random.uniform(0.06, 0.11), 3),
            "unsubscribe_rate": round(random.uniform(0.008, 0.020), 3),
        },
        {
            "topic": topic,
            "persona_segment": "freelancer",
            "open_rate": round(random.uniform(0.42, 0.52), 3),
            "click_rate": round(random.uniform(0.10, 0.18), 3),
            "unsubscribe_rate": round(random.uniform(0.004, 0.012), 3),
        },
    ]

    conn = get_conn()
    cur = conn.cursor()

    for r in records:
        cur.execute("""
        INSERT INTO metrics (topic, persona_segment, open_rate, click_rate, unsubscribe_rate, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            r["topic"],
            r["persona_segment"],
            r["open_rate"],
            r["click_rate"],
            r["unsubscribe_rate"],
            datetime.now(UTC).isoformat()
        ))

    conn.commit()
    conn.close()

    return records




