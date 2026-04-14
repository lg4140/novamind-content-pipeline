from collections import Counter
import random
from datetime import datetime, UTC
from app.db import get_conn

def simulate_metrics(topic: str, send_results: list[dict]) -> list[dict]:
    recipient_counts = Counter(r["persona_segment"] for r in send_results)

    records = []
    for persona, recipient_count in recipient_counts.items():
        if persona == "ops_lead":
            open_rate = round(random.uniform(0.38, 0.48), 3)
            click_rate = round(random.uniform(0.08, 0.14), 3)
            unsubscribe_rate = round(random.uniform(0.005, 0.015), 3)
        elif persona == "creative_director":
            open_rate = round(random.uniform(0.34, 0.44), 3)
            click_rate = round(random.uniform(0.06, 0.11), 3)
            unsubscribe_rate = round(random.uniform(0.008, 0.020), 3)
        else:
            open_rate = round(random.uniform(0.42, 0.52), 3)
            click_rate = round(random.uniform(0.10, 0.18), 3)
            unsubscribe_rate = round(random.uniform(0.004, 0.012), 3)

        open_count = round(recipient_count * open_rate)
        click_count = round(recipient_count * click_rate)
        unsubscribe_count = round(recipient_count * unsubscribe_rate)

        records.append({
            "topic": topic,
            "persona_segment": persona,
            "recipient_count": recipient_count,
            "open_count": open_count,
            "click_count": click_count,
            "unsubscribe_count": unsubscribe_count,
            "open_rate": open_rate,
            "click_rate": click_rate,
            "unsubscribe_rate": unsubscribe_rate,
        })

    conn = get_conn()
    cur = conn.cursor()

    for r in records:
        cur.execute("""
        INSERT INTO metrics (
            topic, persona_segment, recipient_count, open_count, click_count,
            unsubscribe_count, open_rate, click_rate, unsubscribe_rate, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["topic"],
            r["persona_segment"],
            r["recipient_count"],
            r["open_count"],
            r["click_count"],
            r["unsubscribe_count"],
            r["open_rate"],
            r["click_rate"],
            r["unsubscribe_rate"],
            datetime.now(UTC).isoformat()
        ))

    conn.commit()
    conn.close()

    return records





