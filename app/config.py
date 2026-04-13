import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", "https://api.hubapi.com")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

EMAIL_TEMPLATE_IDS = {
    "ops_lead": os.getenv("OPS_LEAD_EMAIL_ID"),
    "creative_director": os.getenv("CREATIVE_DIRECTOR_EMAIL_ID"),
    "freelancer": os.getenv("FREELANCER_EMAIL_ID"),
}


