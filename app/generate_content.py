import json
import os
import re
from datetime import datetime, UTC
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def word_count(text: str) -> int:
    return len(text.split())

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

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        os.makedirs("data/logs", exist_ok=True)
        with open("data/logs/last_bad_generation.txt", "w", encoding="utf-8") as f:
            f.write(raw_text)
        raise ValueError(
            "Model output was not valid JSON. "
            "Saved raw output to data/logs/last_bad_generation.txt"
        )

    required_top_level_keys = {"topic", "blog_title", "blog_outline", "blog_draft", "newsletters"}
    missing_top_level = required_top_level_keys - set(data.keys())
    if missing_top_level:
        raise ValueError(f"Missing required top-level keys: {sorted(missing_top_level)}")

    required_personas = {"ops_lead", "creative_director", "freelancer"}
    newsletters = data.get("newsletters", {})
    missing_personas = required_personas - set(newsletters.keys())
    if missing_personas:
        raise ValueError(f"Missing newsletter personas: {sorted(missing_personas)}")

    for persona in required_personas:
        required_newsletter_keys = {"subject", "preview_text", "body", "cta_text"}
        missing_newsletter_keys = required_newsletter_keys - set(newsletters[persona].keys())
        if missing_newsletter_keys:
            raise ValueError(
                f"Missing newsletter keys for {persona}: {sorted(missing_newsletter_keys)}"
            )

    blog_words = word_count(data["blog_draft"])
    if not (400 <= blog_words <= 600):
        data["_warning"] = f"Blog draft word count out of target range: {blog_words}"

    os.makedirs("data/generated_content", exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    filename = f"data/generated_content/{timestamp}_{slugify(topic)}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    data["_saved_path"] = filename
    return data





