import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the hidden .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_threat_report(parsed_data, forensic_data, risk_data):
    """Feeds forensic evidence to Gemini to generate a SOC narrative."""
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are a Senior Cybersecurity SOC Analyst. Analyze this extracted email forensic data and provide a brief, highly professional threat narrative. 
        Explain exactly how this attack works based on the evidence, and tell the user what to do next. Keep it under 3 paragraphs. Use bullet points for readability. Do not hallucinate.

        --- EVIDENCE ---
        Risk Score: {risk_data.get('score')}/100 ({risk_data.get('classification')})
        From: {parsed_data.get('From')}
        Subject: {parsed_data.get('Subject')}
        Spoofed Sender Detected: {forensic_data.get('Spoofed_Sender')}
        Suspicious Links Found: {forensic_data.get('URLs')}
        
        Email Body Snippet:
        {parsed_data.get('Body')[:500]}
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"⚠️ **API Error:** {str(e)}"