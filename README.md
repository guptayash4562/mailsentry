# 🛡️ MailSentry: Enterprise SOC AI Co-Pilot

MailSentry is an automated, AI-driven email forensic and threat intelligence platform. Built for security operations centers (SOC), it ingests raw suspicious emails, extracts malicious infrastructure, calculates a weighted risk score, and leverages Google Gemini to generate live, executive-level threat narratives.

## ⚡ Core Capabilities
* **Automated Parsing:** Extracts metadata, headers, and payloads from raw `.eml` files.
* **Infrastructure Trace:** Isolates spoofed sender domains and extracts hidden IP addresses and URLs.
* **Risk Scoring Engine:** Calculates a 0-100 severity index based on hard forensic evidence (SPF failures, link density, domain mismatches).
* **AI Threat Intelligence:** Feeds structured telemetry to Gemini to instantly write human-readable incident response reports.

## 🛠️ Tech Stack
* **Frontend:** Streamlit 
* **Backend:** Python (Modular Architecture)
* **AI Integration:** Google GenAI SDK (`gemini-flash-latest`)
* **Environment:** `python-dotenv` for secure API key management

## 🚀 Quick Start Guide

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/mailsentry.git](https://github.com/yourusername/mailsentry.git)
cd mailsentry