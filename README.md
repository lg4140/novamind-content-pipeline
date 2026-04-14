# AI-Powered Marketing Content Pipeline for NovaMind

## Project Overview
This project implements a lightweight AI-powered marketing pipeline for NovaMind, a fictional early-stage AI startup serving small creative agencies. The system generates persona-specific blog and newsletter content, syncs segmented contacts to HubSpot, simulates campaign performance, and produces AI-generated optimization insights.

## Objective
Build an automated marketing workflow that can:
- generate a blog draft and persona-specific newsletters from a single topic
- segment contacts by persona
- sync contacts to a CRM
- log campaign activity to CRM
- simulate engagement metrics
- generate AI-powered recommendations for future content

## Personas
This project targets three audience segments:

1. **Ops Lead**
   - Focus: efficiency, margins, workflow standardization

2. **Creative Director**
   - Focus: protecting creative time, reducing process chaos

3. **Freelancer / Small Studio Owner**
   - Focus: simple setup, fast wins, fewer tools

These personas were selected because they represent key stakeholder types within small creative agencies and require different messaging angles.

## Architecture
Pipeline flow:

Topic Input  
→ AI Content Generation  
→ JSON Content Storage  
→ Contact Segmentation via CSV  
→ HubSpot Contact Sync (dry-run supported)  
→ Persona-Based Newsletter Distribution (dry-run)  
→ Campaign Logging to SQLite  
→ Metrics Simulation with Send Context  
→ AI Performance Summary with Historical Comparison

## Tools Used
- Python
- OpenAI API
- HubSpot API
- SQLite
- Pandas
- Requests
- python-dotenv

## Project Structure
```text
novamind-content-pipeline/
├── app/
│   ├── config.py
│   ├── db.py
│   ├── generate_content.py
│   ├── metrics.py
│   ├── analyze_performance.py
│   ├── hubspot_client.py
│   └── main.py
├── data/
│   ├── contacts.csv
│   ├── generated_content/
│   ├── logs/
│   └── app.db
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

### 1. AI Content Generation
Given a topic such as `"AI in creative automation"`, the system generates:
- a blog title
- a blog outline
- a short-form blog draft
- three persona-specific newsletter versions

Generated content is stored as JSON in `data/generated_content/`.

### 2. CRM Contact Sync
Mock contact data is stored in `data/contacts.csv`, including a `persona_segment` field.

The system syncs contacts to HubSpot using:
- email as the unique identifier
- a persona-based segmentation field
- dry-run mode for safe testing

### 3. Persona-Based Newsletter Distribution
After content generation, the pipeline maps each contact to the correct persona-specific newsletter version based on the `persona_segment` field.

For each contact, the system prepares a realistic send payload that includes:
- contact email
- persona segment
- email template ID
- newsletter subject
- preview text
- body copy
- CTA text
- send status

This distribution step is currently implemented in dry-run mode, which allows safe testing while still demonstrating realistic send logic and payload structure.

### 4. Campaign Logging
Each newsletter send event is logged to SQLite for traceability and historical analysis.

Every campaign log record stores:
- topic
- blog title
- persona segment
- contact email
- newsletter subject
- template ID
- send status
- send date

This makes the pipeline more analysis-ready and better aligned with real marketing operations workflows.

### 5. Performance Simulation and Analysis
The system simulates:
- open rate
- click rate
- unsubscribe rate

Then it uses AI to generate a short performance summary with:
- best-performing persona
- likely explanation
- next newsletter recommendation
- suggested next blog topic

## Assumptions
- Contact data is mocked for demonstration purposes.
- HubSpot integration runs in `DRY_RUN=true` mode by default.
- Performance metrics are simulated rather than pulled from a live email platform.
- `persona_segment` is treated as a custom CRM field in HubSpot.
- Email sending is designed conceptually but is not required to run live for this demo.

## How to Run

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Add environment variables
Create a .env file in the project root with:
```env
OPENAI_API_KEY=your_openai_api_key
HUBSPOT_ACCESS_TOKEN=your_hubspot_private_app_token
HUBSPOT_BASE_URL=https://api.hubapi.com
DRY_RUN=true
OPS_LEAD_EMAIL_ID=
CREATIVE_DIRECTOR_EMAIL_ID=
FREELANCER_EMAIL_ID=
```

### 4. Run the pipeline
```bash
python3 -m app.main --topic "AI in creative automation"
```
## Example Output

The pipeline prints:

- persona counts
- HubSpot sync payload
- generated blog title
- newsletter subject lines
- simulated campaign metrics
- AI performance summary
- saved file locations

### Example output may look like:

- blog title: How AI Is Transforming Workflow Automation for Small Creative Agencies
- best-performing persona: freelancer
- suggested next blog topic: Maximizing Productivity with AI-Powered Creative Tools

## Current Status
### Implemented
- local end-to-end pipeline
- AI content generation
- persona-specific newsletter generation
- persona-based newsletter send payload generation in dry-run mode
- JSON content storage
- SQLite logging
- campaign send logging to SQLite
- HubSpot contact sync in dry-run mode
- HubSpot campaign note logging in dry-run mode
- simulated campaign performance metrics
- AI-generated performance summary
- metrics simulation now includes send context such as recipient count, open count, click count, and unsubscribe count
- AI performance summaries compare the current run against historical averages when available

## Future Improvements
- enable live HubSpot contact sync by switching off dry-run mode
- connect persona-based email templates for actual newsletter distribution
- replace dry-run newsletter payload generation with live send execution
- associate HubSpot campaign notes with individual CRM contacts
- add a dashboard using Streamlit
- support A/B testing for subject lines
- generate next topic recommendations based on historical campaign performance
- add approval or review steps before publishing generated content

## Why Dry-Run Mode
Dry-run mode makes the demo safer, more reproducible, and easier to evaluate. It allows the project to demonstrate realistic HubSpot payloads, persona-based newsletter distribution logic, and campaign logging behavior without depending on portal permissions, email template availability, or live sending configuration.

This approach keeps the workflow implementation concrete while avoiding avoidable delivery failures during evaluation.




