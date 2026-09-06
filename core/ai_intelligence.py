import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load local environment variables if they exist
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_threat_report(parsed_data, forensic_data, risk_data):
    """Feeds forensic evidence to Gemini to generate a structured SOC narrative."""
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are an elite Tier-3 SOC Analyst. Review the following email forensic data and provide a highly technical threat briefing. 
        
        Format your response exactly like this using Markdown. Add double line breaks between sections so the text is extremely easy to read. Do not use conversational filler.

        **VERDICT:**
        (One clear sentence summarizing the threat and objective)

        **KEY EVIDENCE:**
        (Use bullet points to list the most critical IOCs, header anomalies, or suspicious language. Leave a blank line between each bullet point.)

        **RECOMMENDED ACTION:**
        (Numbered list of immediate containment steps for the incident response team. Leave a blank line between each step.)
        
        --- TELEMETRY ---
        RISK SCORE: {risk_data.get('score', 'UNKNOWN')}/100 ({risk_data.get('classification', 'UNKNOWN')})
        SPF STATUS: {forensic_data.get('Auth_Matrix', {}).get('SPF', 'UNKNOWN')}
        SPOOFING DETECTED: {forensic_data.get('Spoofed_Sender', 'UNKNOWN')}
        FROM: {parsed_data.get('From', 'UNKNOWN')}
        SUBJECT: {parsed_data.get('Subject', 'UNKNOWN')}
        URLS DETECTED: {forensic_data.get('URLs', 'NONE')}
        
        BODY SNIPPET:
        {parsed_data.get('Body', '')[:500]}
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"⚠️ **API Error:** {str(e)}"