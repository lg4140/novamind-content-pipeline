import argparse
from datetime import datetime, UTC
import os
import pandas as pd

from app.config import OPENAI_API_KEY
from app.db import init_db, get_conn
from app.generate_content import generate_content
from app.metrics import simulate_metrics
from app.analyze_performance import generate_performance_summary

def save_content_run(topic: str, blog_title: str, content_json_path: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO content_runs (topic, blog_title, content_json_path, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        topic,
        blog_title,
        content_json_path,
        datetime.now(UTC).isoformat()
    ))
    conn.commit()
    conn.close()

def run_pipeline(topic: str):
    init_db()

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY No settings have been made. Please fill in first .env")

    contacts_df = pd.read_csv("data/contacts.csv")
    print(f"Loaded {len(contacts_df)} contacts.")
    print("\nPersona counts:")
    print(contacts_df["persona_segment"].value_counts())

    print("\n[1/4] Generating content...")
    content = generate_content(topic)
    blog_title = content["blog_title"]
    save_content_run(topic, blog_title, content["_saved_path"])

    print("\nBlog title:")
    print(blog_title)

    print("\nSaved content file:")
    print(content["_saved_path"])

    print("\nNewsletter subjects:")
    print("ops_lead:", content["newsletters"]["ops_lead"]["subject"])
    print("creative_director:", content["newsletters"]["creative_director"]["subject"])
    print("freelancer:", content["newsletters"]["freelancer"]["subject"])

    print("\n[2/4] Simulating metrics...")
    metrics = simulate_metrics(topic)
    print(metrics)

    print("\n[3/4] Generating AI performance summary...")
    summary = generate_performance_summary(topic, metrics)

    with open("data/logs/latest_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("\n[4/4] Done.")
    print("\n=== PERFORMANCE SUMMARY ===")
    print(summary)

    print("\nSaved summary file:")
    print("data/logs/latest_summary.txt")

    print("\nGenerated content files:")
    for f in sorted(os.listdir("data/generated_content")):
        print("-", f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True, help="Topic for the content pipeline")
    args = parser.parse_args()

    run_pipeline(args.topic)




    


