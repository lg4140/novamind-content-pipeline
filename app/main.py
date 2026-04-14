import argparse
from datetime import datetime, UTC
import os
import pandas as pd

from app.hubspot_client import upsert_contacts, create_note, send_newsletter
from app.config import OPENAI_API_KEY, EMAIL_TEMPLATE_IDS
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

def log_campaign_send(
    topic: str,
    blog_title: str,
    persona_segment: str,
    contact_email: str,
    newsletter_subject: str,
    hubspot_email_id: str | None,
    hubspot_send_status_id: str | None,
    send_status: str,
):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO campaign_logs (
        topic, blog_title, persona_segment, contact_email,
        newsletter_subject, hubspot_email_id, hubspot_send_status_id,
        send_status, send_date
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        topic,
        blog_title,
        persona_segment,
        contact_email,
        newsletter_subject,
        hubspot_email_id,
        hubspot_send_status_id,
        send_status,
        datetime.now(UTC).isoformat()
    ))
    conn.commit()
    conn.close()

def run_pipeline(topic: str):
    init_db()

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY No settings have been made. Please fill in first .env")

    os.makedirs("data/logs", exist_ok=True)
    os.makedirs("data/generated_content", exist_ok=True)

    contacts_df = pd.read_csv("data/contacts.csv")
    contacts = contacts_df.to_dict(orient="records")

    print(f"Loaded {len(contacts_df)} contacts.")
    print("\nPersona counts:")
    print(contacts_df["persona_segment"].value_counts())

    print("\n[0/6] Syncing contacts to HubSpot...")
    sync_result = upsert_contacts(contacts)
    print(sync_result)

    print("\n[1/6] Generating content...")
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

    print("\n[2/6] Preparing persona-based newsletter sends...")
    send_results = []
    
    for contact in contacts:
        persona = contact["persona_segment"]
        newsletter = content["newsletters"][persona]
        hubspot_email_id = EMAIL_TEMPLATE_IDS.get(persona)

        send_result = send_newsletter(contact, newsletter, hubspot_email_id)
        print(send_result)
        
        send_results.append({
            "persona_segment": persona,
            "contact_email": contact["email"],
            "hubspot_email_id": send_result.get("hubspot_email_id"),
            "statusId": send_result.get("statusId"),
            "send_status": send_result["status"],
        }) 
        log_campaign_send(
            topic=topic,
            blog_title=blog_title,
            persona_segment=persona,
            contact_email=contact["email"],
            newsletter_subject=newsletter["subject"],
            hubspot_email_id=str(send_result.get("hubspot_email_id")) if send_result.get("hubspot_email_id") is not None else None,
            hubspot_send_status_id=send_result.get("statusId"),
            send_status=send_result["status"],
         )

    print("\n[3/6] Simulating metrics...")
    metrics = simulate_metrics(topic, send_results)
    print(metrics)

    print("\n[4/6] Generating AI performance summary...")
    summary = generate_performance_summary(topic, metrics)

    with open("data/logs/latest_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    note_text = (
        f"Campaign run completed | "
        f"topic={topic} | "
        f"blog_title={blog_title} | "
        f"content_file={content['_saved_path']} | "
        f"summary_file=data/logs/latest_summary.txt"
    )

    print("\n[5/6] Logging campaign note to HubSpot...")
    note_result = create_note(note_text)
    print(note_result)

    print("\n[6/6] Done.")
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











    


