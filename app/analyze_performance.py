from datetime import datetime, UTC
from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.db import get_conn

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_performance_summary(topic: str, metrics: list[dict]) -> str:
    prompt = f"""
You are a Content & Growth Analyst for NovaMind.

Below is newsletter performance data for one campaign topic.

Topic: {topic}

Metrics:
{metrics}

Please write a concise performance summary in English that includes:
1. Which persona performed best
2. One likely explanation
3. One recommendation for the next newsletter
4. One suggested next blog topic

Keep it between 120 and 180 words.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.5,
        max_output_tokens=400,
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




