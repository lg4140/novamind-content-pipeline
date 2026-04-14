import uuid
import requests
from datetime import datetime, UTC
from app.config import HUBSPOT_ACCESS_TOKEN, HUBSPOT_BASE_URL, DRY_RUN

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def upsert_contacts(contacts: list[dict]) -> dict:
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/batch/upsert"

    payload = {"inputs": []}

    for c in contacts:
        payload["inputs"].append({
            "id": c["email"],
            "idProperty": "email",
            "properties": {

                "email": c["email"],
                "firstname": c["firstname"],
                "lastname": c["lastname"],
                "company": c["company"],
                "persona_segment": c["persona_segment"]
            }
        })

    if DRY_RUN:
        return {"status": "DRY_RUN", "payload": payload}

    response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

def get_contact_by_email(email: str) -> dict:
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{email}"
    params = {
        "idProperty": "email",
        "properties": "email,firstname,lastname,company,persona_segment"
    }

    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def create_note(note_body: str) -> dict:
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/notes"
    payload = {
        "properties": {
            "hs_timestamp": datetime.now(UTC).isoformat(),
            "hs_note_body": note_body
        }
    }

    if DRY_RUN:
        return {"status": "DRY_RUN", "payload": payload}

    response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

def send_newsletter(contact: dict, newsletter: dict, hubspot_email_id: str | None) -> dict:
    url = f"{HUBSPOT_BASE_URL}/marketing/v3/transactional/single-email/send"

    payload = {
        "emailId": int(hubspot_email_id) if hubspot_email_id else None,
        "message": {
            "to": contact["email"],
            "sendId": f"{contact['persona_segment']}-{uuid.uuid4().hex[:12]}"
        },
        "contactProperties": {
            "email": contact["email"],
            "firstname": contact["firstname"],
            "lastname": contact["lastname"],
            "company": contact["company"],
            "persona_segment": contact["persona_segment"]
        },
        "customProperties": {
            "newsletter_subject": newsletter["subject"],
            "newsletter_preview_text": newsletter["preview_text"],
            "newsletter_body": newsletter["body"],
            "newsletter_cta_text": newsletter["cta_text"]
        }
    }

    if DRY_RUN:
        return {
            "status": "DRY_RUN",
            "endpoint": url,
            "hubspot_email_id": payload["emailId"],
            "statusId": None,
            "payload": payload,
        }

    if payload["emailId"] is None:
        raise ValueError("Missing HubSpot emailId for live send.")

    response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()

    return {
        "status": result.get("status"),
        "endpoint": url,
        "hubspot_email_id": payload["emailId"],
        "statusId": result.get("statusId"),
        "payload": payload,
    }

def associate_note_to_contact(note_id: str, contact_id: str) -> dict:
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/notes/{note_id}/associations/contact/{contact_id}/note_to_contact"

    if DRY_RUN:
        return {
            "status": "DRY_RUN",
            "note_id": note_id,
            "contact_id": contact_id
        }

    response = requests.put(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return {"status": "associated"}







