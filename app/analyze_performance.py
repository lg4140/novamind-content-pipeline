from datetime import datetime, UTC
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.db import get_conn

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_performance_summary(topic: str, metrics: list[dict]) -> str:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        persona_segment,
        AVG(recipient_count),
        AVG(open_count),
        AVG(click_count),
        AVG(unsubscribe_count),
        AVG(open_rate),
        AVG(click_rate),
        AVG(unsubscribe_rate)
    FROM metrics
    WHERE topic = ?
      AND id NOT IN (
          SELECT MAX(id)
          FROM metrics
          WHERE topic = ?
          GROUP BY persona_segment
      )
    GROUP BY persona_segment
    """, (topic, topic))

    historical_rows = cur.fetchall()
    conn.close()

    historical_summary = {
        row[0]: {
            "avg_recipient_count": round(row[1], 2) if row[1] is not None else None,
            "avg_open_count": round(row[2], 2) if row[2] is not None else None,
            "avg_click_count": round(row[3], 2) if row[3] is not None else None,
            "avg_unsubscribe_count": round(row[4], 2) if row[4] is not None else None,
            "avg_open_rate": round(row[5], 3) if row[5] is not None else None,
            "avg_click_rate": round(row[6], 3) if row[6] is not None else None,
            "avg_unsubscribe_rate": round(row[7], 3) if row[7] is not None else None,
        }
        for row in historical_rows
    }

    prompt = f"""
You are a Content & Growth Analyst for NovaMind.

Below is newsletter performance data for one campaign topic.

Topic: {topic}

Current campaign metrics:
{metrics}

Historical averages for this topic from previous runs:
{historical_summary if historical_summary else "No historical baseline available yet."}

Please write a concise performance summary in English that includes:
1. Which persona performed best in the current campaign
2. One likely explanation
3. One recommendation for the next newsletter
4. One suggested next blog topic
5. One brief comparison vs. historical averages if available

Keep it between 140 and 220 words.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.5,
        max_output_tokens=500,
    )

    summary = response.output_text.strip()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO summaries (topic, summary_text, created_at)
    VALUES (?, ?, ?)
    """, (
        topic,
        summary,
        datetime.now(UTC).isoformat()
    ))
    conn.commit()
    conn.close()

    return summary




