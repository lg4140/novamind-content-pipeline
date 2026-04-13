import json
import re
from datetime import datetime, UTC
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def generate_content(topic: str) -> dict:
    prompt = f"""
You are a B2B SaaS content strategist for NovaMind, an early-stage AI startup
that helps small creative agencies automate workflows.

Return ONLY valid JSON with this structure:
{{
  "topic": "...",
  "blog_title": "...",
  "blog_outline": ["...", "...", "...", "..."],
  "blog_draft": "...",
  "newsletters": {{
    "ops_lead": {{
      "subject": "...",
      "preview_text": "...",
      "body": "...",
      "cta_text": "..."
    }},
    "creative_director": {{
      "subject": "...",
      "preview_text": "...",
      "body": "...",
      "cta_text": "..."
    }},
    "freelancer": {{
      "subject": "...",
      "preview_text": "...",
      "body": "...",
      "cta_text": "..."
    }}
  }}
}}

Rules:
1. Blog should be 400-600 words.
2. Tone: practical, smart, startup-friendly.
3. Persona differences:
   - ops_lead: efficiency, margins, process standardization
   - creative_director: protect creative time, reduce workflow chaos
   - freelancer: simple setup, fewer tools, fast wins
4. Each newsletter body should be short and clearly tailored to the persona.
5. No markdown fences. Output raw JSON only.

Topic: {topic}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.7,
        max_output_tokens=2500,
    )

    raw_text = response.output_text
    data = json.loads(raw_text)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    filename = f"data/generated_content/{timestamp}_{slugify(topic)}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    data["_saved_path"] = filename
    return data




