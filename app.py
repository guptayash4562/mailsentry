import streamlit as st
from core.parser import parse_eml_bytes
from core.forensics import run_forensics
from core.scoring import calculate_risk
from core.ai_intelligence import generate_threat_report
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MailSentry | Enterprise SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that dark SOC vibe without breaking the backend
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .stButton>button { width: 100%; border-radius: 4px; background-color: #0068c9; color: white; }
    .stMetric { background-color: #1e2329; padding: 15px; border-radius: 8px; border-left: 4px solid #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: INGESTION VECTOR ---
with st.sidebar:
    st.title("🛡️ MAILSENTRY")
    st.caption("Enterprise SOC v2.4 | SIH Prototype")
    st.markdown("---")
    
    st.header("Ingestion Vector")
    upload_method = st.radio("Select Incident Scenario:", ["Upload Raw .EML", "Pre-Loaded Demo"])
    
    uploaded_file = None
    if upload_method == "Upload Raw .EML":
        uploaded_file = st.file_uploader("Upload Suspicious Email", type=['eml'])
    else:
        demo_case = st.selectbox("Select Threat Feed:", ["Case 01: Executive Brand Impersonation"])
    
    st.markdown("---")
    st.markdown("**Intelligence Parameters**")
    st.text_input("Gemini API Key", type="password", placeholder="Loaded from .env", disabled=True)
    
    st.markdown("---")
    analyze_btn = st.button("EXECUTE FORENSIC PIPELINE")

# --- EXECUTE ANALYSIS LOGIC ---
if analyze_btn:
    if upload_method == "Upload Raw .EML" and uploaded_file is not None:
        with st.spinner("Initializing Threat Forensics..."):
            raw_bytes = uploaded_file.getvalue()
            parsed_data = parse_eml_bytes(raw_bytes)
            forensic_data = run_forensics(parsed_data)
            risk_data = calculate_risk(parsed_data, forensic_data)
            
            st.session_state['parsed_email'] = parsed_data
            st.session_state['forensics'] = forensic_data
            st.session_state['risk'] = risk_data
    elif upload_method == "Upload Raw .EML" and uploaded_file is None:
        st.error("Missing payload: Please upload an .eml file to begin ingestion.")

# --- MAIN DASHBOARD AREA ---
st.markdown("## ⚡ MAILSENTRY INTELLIGENCE PLATFORM")
st.caption("Unified Email Forensics & Automated Threat Containment")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Triage Overview", 
    "🔍 Header Forensics", 
    "🌍 Infrastructure Trace", 
    "🤖 AI Co-Pilot"
])

# --- TAB 1: TRIAGE OVERVIEW ---
with tab1:
    display_score = st.session_state.get('risk', {}).get('score', '--')
    display_class = st.session_state.get('risk', {}).get('classification', 'Awaiting Ingestion')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="COMPOSITE RISK INDEX", value=f"{display_score}/100")
    with col2:
        st.metric(label="THREAT CLASSIFICATION", value=display_class)
    with col3:
        # Safely pull Auth Matrix data if it exists, otherwise default to UNKNOWN
        auth = st.session_state.get('forensics', {}).get('Auth_Matrix', {})
        spf_status = auth.get('SPF', 'UNKNOWN')
        st.metric(label="SPF AUTHENTICATION", value=spf_status)
    
    st.markdown("---")
    
    if 'parsed_email' in st.session_state:
        st.subheader("Risk Scoring Breakdown")
        for reason in st.session_state['risk']['reasons']:
            st.warning(reason)
            
        st.subheader("Target Metadata")
        data = st.session_state['parsed_email']
        st.code(f"From: {data.get('From', 'Unknown')}\nTo: {data.get('To', 'Unknown')}\nSubject: {data.get('Subject', 'No Subject')}\nDate: {data.get('Date', 'Unknown')}")
        
        st.subheader("Message Body Excerpt")
        st.info(data.get('Body', 'No body content parsed.'))
    else:
        st.info("System Idle. Upload a payload in the sidebar and execute pipeline.")

# --- TAB 2 & 3 ---
with tab2:
    st.subheader("Technical Header Analysis")
    if 'forensics' in st.session_state:
        forensics = st.session_state['forensics']
        if forensics.get('Spoofed_Sender'):
            st.error("🚨 CRITICAL: The visible 'From' domain does not align with the authenticated 'Return-Path' domain.")
        else:
            st.success("✅ Sender domains appear to align.")
            
        st.markdown("### Extracted Suspicious URLs")
        urls = forensics.get('URLs', [])
        if urls:
            for url in urls:
                st.code(url)
        else:
            st.write("No external links detected.")

with tab3:
    st.subheader("Email Relay Path & IP Extraction")
    if 'forensics' in st.session_state:
        st.markdown("### Extracted IP Addresses")
        ips = forensics.get('IPs', [])
        if ips:
            for ip in ips:
                st.code(ip)
        else:
            st.write("No external infrastructure IPs detected.")

with tab4:
    st.subheader("🤖 AI Threat Narrative (Gemini)")
    
    if 'parsed_email' in st.session_state:
        st.write("Leverage Google Gemini to synthesize forensic evidence into a human-readable SOC report.")
        
        # The Trigger Button
        if st.button("Generate AI Threat Report", type="primary"):
            with st.spinner("Gemini is analyzing the forensic evidence..."):
                report = generate_threat_report(
                    st.session_state['parsed_email'],
                    st.session_state['forensics'],
                    st.session_state['risk']
                )
                st.markdown("---")
                st.write(report)
    else:
        st.info("System Idle. Upload a payload in the sidebar and execute the pipeline first.")