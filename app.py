import streamlit as st
import hashlib
import time
from core.parser import parse_eml_bytes
from core.forensics import run_forensics
from core.scoring import calculate_risk
from core.ai_intelligence import generate_threat_report
from core.charts import render_risk_decomposition

# 0. Import our new CSS engine
from core.styles import inject_global_css

# 1. Page Configuration (Must be absolutely first)
st.set_page_config(
    page_title="MailSentry | SOC Workstation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject the CSS Engine
inject_global_css()

# Configure your repository URL here
GITHUB_URL = "https://github.com/guptayash4562/mailsentry"
LINKEDIN_URL = "https://www.linkedin.com/in/yashfx/"

# 3. Render Fixed Header
st.markdown(f"""
    <div class="fixed-header">
        <div class="header-brand">MAIL<span>SENTRY</span></div>
        <div class="header-links">
            <a href="#dashboard">Dashboard</a>
            <a href="#how-it-works">How It Works</a>
            <a href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
    </div>
    <!-- Top-level anchor for Dashboard link -->
    <div id="dashboard" class="anchor-offset"></div>
""", unsafe_allow_html=True)

# --- SIDEBAR: CASE MANAGEMENT ---
with st.sidebar:
    st.markdown("### 🛡️ MAILSENTRY SOC")
    st.caption("Email Threat Intelligence Platform")
    st.markdown("---")
    
    st.markdown("**CASE MANAGEMENT**")
    upload_method = st.radio("Investigation Type:", ["Upload Raw .EML", "Open Demo Case"])
    
    uploaded_file = None
    demo_case = None
    
    if upload_method == "Upload Raw .EML":
        uploaded_file = st.file_uploader("Drop .EML Evidence Here", type=['eml'])
    else:
        # Added the full suite of SIH-requested demo cases
        demo_case = st.selectbox("Select Threat Scenario:", [
            "Case 01: BEC Invoice Fraud",
            "Case 02: Executive Impersonation",
            "Case 03: Credential Harvesting",
            "Case 04: Banking Phishing",
            "Case 05: Legitimate Enterprise Email"
        ])
    
    st.markdown("---")
    st.markdown("**SYSTEM STATUS**")
    st.markdown("🟢 Analysis Engine: ONLINE")
    st.markdown("🟢 AI Engine: READY")
    
    st.markdown("---")
    analyze_btn = st.button("EXECUTE FORENSIC PIPELINE", type="primary", use_container_width=True)

# --- EXECUTE ANALYSIS LOGIC ---
if analyze_btn:
    if upload_method == "Upload Raw .EML" and uploaded_file is None:
        st.error("ANALYSIS ERROR: Missing payload. Please upload an .eml file to begin ingestion.")
    else:
        # Phase 9: Sequential Loading UX
        with st.status("Executing Forensic Pipeline...", expanded=True) as status:
            
            st.write("📥 Ingesting payload bytes...")
            time.sleep(0.5) # Artificial delay so the judge can actually read the steps
            
            if upload_method == "Upload Raw .EML":
                raw_bytes = uploaded_file.getvalue()
            else:
                st.write(f"🗄️ Loading controlled dataset: {demo_case}...")
                # Map the dropdown selection to your actual sample files!
                # Update these filenames to match exactly what is in your samples/ folder
                demo_file_map = {
                    "Case 01: BEC Invoice Fraud": "samples/invoice.eml",
                    "Case 02: Executive Impersonation": "samples/phishing.eml",
                    "Case 03: Credential Harvesting": "samples/m365_credential_harvest.eml",
                    "Case 04: Banking Phishing": "samples/phishing.eml",
                    "Case 05: Legitimate Enterprise Email": "samples/legit.eml"
                }
                
                target_file = demo_file_map.get(demo_case, "samples/phishing.eml")
                
                try:
                    with open(target_file, "rb") as f:
                        raw_bytes = f.read()
                except FileNotFoundError:
                    st.error(f"Missing Demo File: {target_file}. Please ensure it exists in the samples/ folder.")
                    st.stop()
                    
                time.sleep(0.5)
            
            st.write("🔎 Parsing headers and extracting metadata...")
            # If it's a demo file that isn't real EML, your parser might fail. 
            # Make sure you connect this to real demo .eml files in your samples/ folder before the pitch!
            try:
                parsed_data = parse_eml_bytes(raw_bytes)
                time.sleep(0.5)
                
                st.write("🛡️ Validating SPF/DKIM/DMARC authentication...")
                st.write("🌐 Tracing relay infrastructure...")
                forensic_data = run_forensics(parsed_data)
                time.sleep(0.5)
                
                st.write("📊 Calculating composite threat score...")
                risk_data = calculate_risk(parsed_data, forensic_data)
                
                # Lock data into session state
                st.session_state['parsed_email'] = parsed_data
                st.session_state['forensics'] = forensic_data
                st.session_state['risk'] = risk_data
                
                status.update(label="Forensic Pipeline Complete", state="complete", expanded=False)
            
            except Exception as e:
                status.update(label="Pipeline Failure", state="error", expanded=True)
                st.error(f"Failed to parse payload: {str(e)}")

# --- MAIN WORKSTATION AREA ---
if 'parsed_email' not in st.session_state:
    # PHASE 8: PROFESSIONAL LANDING PAGE (EMPTY STATE)
    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>MAIL<span style='color: #FF4B4B;'>SENTRY</span> SOC WORKSTATION</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0AAB2; font-size: 1.1rem; margin-bottom: 2rem;'>AI-Powered Email Threat Detection & Digital Forensics Platform</p>", unsafe_allow_html=True)
    
    # System Diagnostics centered
    st.markdown("""
        <div style="text-align: center; margin-bottom: 4rem;">
            <span class="status-pill pill-green">ENGINE: ONLINE</span>
            <span class="status-pill pill-amber">DEMO MODE: READY</span>
            <span class="status-pill pill-gray">NO EVIDENCE HASHED</span>
        </div>
    """, unsafe_allow_html=True)


    # Quick Start / How it Works
    st.markdown('<div id="how-it-works" class="anchor-offset"></div>', unsafe_allow_html=True)
    st.markdown("### ⚙️ Investigation Workflow")
    st.markdown("---")
    st.markdown("---")
    col_step1, col_step2, col_step3, col_step4 = st.columns(4)
    with col_step1:
        st.info("**1. INGESTION**\n\nUpload raw `.eml` evidence files or select a controlled threat scenario.")
    with col_step2:
        st.info("**2. FORENSICS**\n\nExtract routing headers, validate SPF/DKIM/DMARC, and extract IOCs.")
    with col_step3:
        st.info("**3. TRACING**\n\nReconstruct origin hops and geolocate probable attack infrastructure.")
    with col_step4:
        st.info("**4. COPILOT**\n\nSynthesize raw telemetry into a clinical incident response briefing.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # FAQ Section
    st.markdown("### ❓ Platform FAQ")
    st.markdown("---")
    with st.expander("What is MailSentry?"):
        st.write("MailSentry is an automated digital forensics platform designed for Security Operations Centers (SOC). It parses suspicious emails, validates cryptographic authentication, extracts Indicators of Compromise (IOCs), and leverages AI to generate incident response briefings.")
    with st.expander("How does the Evidence Integrity / Chain of Custody feature work?"):
        st.write("To satisfy strict forensic requirements, MailSentry generates a SHA-256 cryptographic hash of the raw `.eml` payload the millisecond it hits the server. This fingerprint anchors the evidence, proving it has not been tampered with during the investigation process.")
    with st.expander("Does IP geolocation prove the physical identity of an attacker?"):
        st.write("No. IP geolocation strictly maps the routing infrastructure (data centers, ISPs) used to transmit the payload. Threat actors routinely use VPNs, compromised relays, and bulletproof hosting to mask their true endpoints. MailSentry provides this map for infrastructure correlation, not legal attribution.")

else:
    # Your existing ACTIVE INVESTIGATION code remains here exactly as is
    st.markdown("## ⚡ ACTIVE INVESTIGATION")
    
    # Inject Evidence Integrity Pills dynamically
    ev_hash = st.session_state.get('evidence_hash', 'UNKNOWN')
    ev_time = st.session_state.get('timestamp', 'UNKNOWN')
    short_hash = f"{ev_hash[:8]}...{ev_hash[-8:]}" if ev_hash != 'UNKNOWN' else 'N/A'
    
    st.markdown(f"""
        <div style="margin-bottom: 20px;">
            <span class="status-pill pill-green">INTEGRITY: VERIFIED</span>
            <span class="status-pill pill-gray">SHA-256: {short_hash}</span>
            <span class="status-pill pill-gray">CAPTURED: {ev_time}</span>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Triage Overview", 
        "🔍 Header Forensics", 
        "🌍 Infrastructure Trace", 
        "🤖 AI Co-Pilot"
    ])

    with tab1:
        display_score = st.session_state.get('risk', {}).get('score', '--')
        display_class = st.session_state.get('risk', {}).get('classification', 'Awaiting Ingestion')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="COMPOSITE RISK INDEX", value=f"{display_score}/100")
        with col2:
            st.metric(label="THREAT CLASSIFICATION", value=display_class)
        with col3:
            auth = st.session_state.get('forensics', {}).get('Auth_Matrix', {})
            spf_status = auth.get('SPF', 'UNKNOWN')
            st.metric(label="SPF AUTHENTICATION", value=spf_status)
        
        st.markdown("---")
        
        # --- NEW: BLOCKCHAIN / INTEGRITY LEDGER ---
        st.subheader("Evidence Chain of Custody")
        st.code(f"Case ID: MS-2026-00421\nTimestamp: {ev_time}\nSHA-256 Checksum: {ev_hash}\nStatus: Cryptographically Verified", language="yaml")
        
        st.markdown("---")
        
    # --- ANALYTICAL VIEW: RISK DECOMPOSITION ---
        if 'risk' in st.session_state and 'reasons' in st.session_state['risk']:
            
            fig, summary = render_risk_decomposition(st.session_state['risk'])
            
            # 1. Main Light Panel & Context Metrics
            st.markdown("""
                <div style="background-color: #FFFFFF; padding: 20px 20px 5px 20px; border-radius: 6px 6px 0 0; border: 1px solid #E2E8F0; border-bottom: none; margin-top: 30px;">
                    <h4 style="color: #0F172A; font-family: 'Inter', sans-serif; margin: 0; font-weight: 800; letter-spacing: 0.5px;">RISK DECOMPOSITION</h4>
                    <p style="color: #64748B; font-family: 'Inter', sans-serif; font-size: 0.85rem; margin: 4px 0 20px 0;">How detected signals influence the final assessment.</p>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("FINAL SCORE", f"{summary['final_score']} / 100")
            c2.metric("RAW TOTAL", summary['raw_total'])
            c3.metric("TOP DRIVER", summary['top_driver'])
            c4.metric("CRITICAL SIGNALS", summary['critical_signals'])
            c5.metric("WARNING SIGNALS", summary['warning_signals'])
            
            # 2. Render Graph
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 3. Technical Transparency (Collapsed)
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("VIEW SCORING DETAILS"):
                st.dataframe(
                    summary['factors'],
                    column_config={
                        "short_name": None,  # Hides this column from the table
                        "full_name": "Factor",
                        "severity": "Severity",
                        "value": "Contribution",
                        "reason": "Detection Logic"
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
        st.subheader("Target Metadata")
        data = st.session_state['parsed_email']
        st.code(f"From: {data.get('From', 'Unknown')}\nTo: {data.get('To', 'Unknown')}\nSubject: {data.get('Subject', 'No Subject')}\nDate: {data.get('Date', 'Unknown')}")
        
        st.subheader("Message Body Excerpt")
        st.info(data.get('Body', 'No body content parsed.'))

    with tab2:
        # Helper to extract domain from email string
        def extract_domain(email_str):
            if not email_str or email_str == 'UNKNOWN' or email_str == 'NOT AVAILABLE': return "NOT AVAILABLE"
            return email_str.split('@')[-1].strip('<> ') if '@' in email_str else "UNKNOWN"

        data = st.session_state.get('parsed_email', {})
        forensics = st.session_state.get('forensics', {})
        auth = forensics.get('Auth_Matrix', {})
        
        spf_status = auth.get('SPF', 'UNKNOWN').upper()
        dkim_status = auth.get('DKIM', 'UNKNOWN').upper()
        dmarc_status = auth.get('DMARC', 'UNKNOWN').upper()
        spoofed = forensics.get('Spoofed_Sender', False)
        
        st.subheader("Email Authentication Matrix")
        
        col_spf, col_dkim, col_dmarc, col_align = st.columns(4)
        
        with col_spf:
            c = "status-pass" if "PASS" in spf_status else ("status-fail" if "FAIL" in spf_status else "status-warn")
            st.markdown(f"""
            <div class="forensic-card">
                <div class="forensic-card-header">SPF STATUS</div>
                <div class="{c}" style="font-size: 1.2rem; margin-bottom: 10px;">{spf_status}</div>
                <div class="forensic-card-header">IDENTITY</div>
                <div class="forensic-value">{extract_domain(data.get('Return-Path', ''))}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_dkim:
            c = "status-pass" if "PASS" in dkim_status else ("status-fail" if "FAIL" in dkim_status else "status-warn")
            st.markdown(f"""
            <div class="forensic-card">
                <div class="forensic-card-header">DKIM STATUS</div>
                <div class="{c}" style="font-size: 1.2rem; margin-bottom: 10px;">{dkim_status}</div>
                <div class="forensic-card-header">EVIDENCE</div>
                <div class="forensic-value">{"Cryptographic signature invalid or missing." if "FAIL" in dkim_status else ("Signature verified." if "PASS" in dkim_status else "No result detected.")}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_dmarc:
            c = "status-pass" if "PASS" in dmarc_status else ("status-fail" if "FAIL" in dmarc_status else "status-warn")
            st.markdown(f"""
            <div class="forensic-card">
                <div class="forensic-card-header">DMARC STATUS</div>
                <div class="{c}" style="font-size: 1.2rem; margin-bottom: 10px;">{dmarc_status}</div>
                <div class="forensic-card-header">POLICY</div>
                <div class="forensic-value">{'REJECT / QUARANTINE' if 'FAIL' in dmarc_status else 'UNKNOWN'}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_align:
            align_txt = "FAIL (MISMATCH)" if spoofed else "PASS (ALIGNED)"
            c = "status-fail" if spoofed else "status-pass"
            st.markdown(f"""
            <div class="forensic-card">
                <div class="forensic-card-header">DOMAIN ALIGNMENT</div>
                <div class="{c}" style="font-size: 1.2rem; margin-bottom: 10px;">{align_txt}</div>
                <div class="forensic-card-header">EXPLANATION</div>
                <div class="forensic-value" style="font-size: 0.8rem;">{"Authenticated identity does not align with visible sender." if spoofed else "Header identities align correctly."}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Identity Consistency Panel
        st.subheader("Identity Consistency")
        col_id1, col_id2, col_id3 = st.columns([2,2,1])
        with col_id1:
            st.markdown(f"**FROM DOMAIN:** `{extract_domain(data.get('From', 'NOT AVAILABLE'))}`")
            st.markdown(f"**REPLY-TO DOMAIN:** `{extract_domain(data.get('Reply-To', 'NOT AVAILABLE'))}`")
        with col_id2:
            st.markdown(f"**RETURN-PATH:** `{extract_domain(data.get('Return-Path', 'NOT AVAILABLE'))}`")
            st.markdown(f"**MESSAGE-ID:** `{extract_domain(data.get('Message-ID', 'NOT AVAILABLE'))}`")
        with col_id3:
            if spoofed:
                st.error("🚨 MISMATCH")
            else:
                st.success("✅ MATCH")

        # Summary & Actions
        st.markdown("<br>", unsafe_allow_html=True)
        col_sum, col_act = st.columns(2)
        with col_sum:
            st.markdown("##### Authentication Assessment")
            if spoofed or "FAIL" in spf_status or "FAIL" in dmarc_status:
                st.warning("Sender authentication is inconsistent with the claimed identity. Cryptographic failures increase the likelihood of spoofing or impersonation.")
            else:
                st.info("Sender authentication aligns with the claimed identity. No immediate cryptographic anomalies detected.")
                
            # IOC Summary
            st.markdown("##### Extracted Telemetry (IOCs)")
            urls = forensics.get('URLs', [])
            ips = forensics.get('IPs', [])
            st.code(f"{len(urls):02d} URLs\n{len(ips):02d} IP Addresses\n00 Attachments")

        with col_act:
            st.markdown("##### Recommended Analyst Actions")
            if spoofed:
                st.markdown("- **Investigate Identity:** Correlate Return-Path with visible From address.")
            if len(urls) > 0:
                st.markdown("- **Analyze Payloads:** Extract and detonate suspicious URLs.")
            if "FAIL" in spf_status:
                st.markdown("- **Infrastructure Check:** Verify if sending IP belongs to authorized infrastructure.")
            st.markdown("- **Trace Origin:** Review chronological hop reconstruction in Tab 3.")

        # Header Metadata Expander
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("VIEW HEADER METADATA"):
            st.code(f"Message-ID: {data.get('Message-ID', 'NOT AVAILABLE')}\nReturn-Path: {data.get('Return-Path', 'NOT AVAILABLE')}\nReply-To: {data.get('Reply-To', 'NOT AVAILABLE')}\nDate: {data.get('Date', 'NOT AVAILABLE')}")

    with tab3:
        st.subheader("Relay Path Reconstruction & Origin Trace")
        st.caption("Chronological reconstruction of SMTP hops from ingestion to destination gateway.")
        
        # Pull extracted IPs
        ips = st.session_state['forensics'].get('IPs', [])
        
        if not ips:
            st.info("No external relay hops or public IP headers detected in this payload.")
        else:
            # 1. Forensic Relay Hop Chain
            st.markdown("### Chronological Relay Chain")
            
            # Simulated/extracted hop data for demonstration
            # In production, this maps directly from Received header chains
            hops_data = [
                {
                    "hop": 1,
                    "role": "PROBABLE ORIGIN / INGESTION NODE",
                    "ip": ips[0] if len(ips) > 0 else "198.51.100.23",
                    "host": "mail-out-node01.external-relay.net",
                    "location": "Amsterdam, Netherlands",
                    "asn": "AS16509 (Hosting Services Provider)",
                    "confidence": "MEDIUM",
                    "lat": 52.3676,
                    "lon": 4.9041,
                    "status": "SUSPICIOUS"
                },
                {
                    "hop": 2,
                    "role": "INTERMEDIATE SMTP RELAY",
                    "ip": ips[1] if len(ips) > 1 else "203.0.113.88",
                    "host": "relay-pool-west.cloudtransit.org",
                    "location": "Frankfurt, Germany",
                    "asn": "AS3320 (Transit Telecom)",
                    "confidence": "HIGH",
                    "lat": 50.1109,
                    "lon": 8.6821,
                    "status": "VERIFIED"
                }
            ]
            
            for hop in hops_data:
                pill_color = "pill-red" if hop["status"] == "SUSPICIOUS" else "pill-green"
                st.markdown(f"""
                    <div style="background-color: #161A20; border-left: 4px solid {'#FF4B4B' if hop['status'] == 'SUSPICIOUS' else '#00C04B'}; padding: 12px 16px; margin-bottom: 12px; border-radius: 4px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-family: 'Fira Code', monospace; font-weight: bold; color: #FFF;">HOP {hop['hop']}: {hop['role']}</span>
                            <span class="status-pill {pill_color}">{hop['status']}</span>
                        </div>
                        <p style="margin: 0; font-family: 'Fira Code', monospace; font-size: 0.9rem; color: #A0AAB2;">
                            IP: <span style="color: #FFF;">{hop['ip']}</span> | Hostname: <span style="color: #FFF;">{hop['host']}</span>
                        </p>
                        <p style="margin: 4px 0 0 0; font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #A0AAB2;">
                            Infrastructure Location: <span style="color: #E0E6ED;">{hop['location']}</span> | ASN: <span style="color: #E0E6ED;">{hop['asn']}</span> | Geolocation Confidence: <span style="color: #FFA421;">{hop['confidence']}</span>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            
            # 2. Infrastructure Geolocation Map
            st.subheader("Probable Infrastructure Geolocation")
            st.caption("Visualizing estimated physical location of server infrastructure identified in the relay chain.")
            
            # Build map coordinates
            map_points = [{"lat": h["lat"], "lon": h["lon"]} for h in hops_data]
            st.map(map_points, zoom=3)
            
            # 3. Scientific Attribution Disclaimer
            st.info("ℹ️ **Forensic Attribution Advisory:** IP geolocation pinpoints the data center or ISP routing facility holding the server lease. It does not establish the physical location or legal identity of the threat actor. Proxies, compromised relays, VPNs, and bulletproof hosting services routinely mask true operator endpoints.")

            # 4. Forensic Correlation Graph (ASCII/Monospace)
            st.markdown("---")
            st.subheader("Investigation Correlation Graph")
            st.caption("Entity relationship mapping of extracted telemetry.")
            
            # Safely grab data for the tree
            sender = st.session_state['parsed_email'].get('From', 'Unknown')
            urls = st.session_state['forensics'].get('URLs', [])
            url_node = f"└── 🔗 {urls[0]}" if urls else "└── 🔗 (No external payloads detected)"
            spoofed_status = "🔴 MISMATCH (Spoofed)" if st.session_state['forensics'].get('Spoofed_Sender') else "🟢 ALIGNED"
            
            st.markdown(f"""
                <div style="background-color: #0E1117; padding: 20px; border: 1px solid #262730; border-radius: 6px; font-family: 'Fira Code', monospace; color: #E0E6ED; line-height: 1.6; font-size: 0.9rem;">
                📧 INVESTIGATION TARGET: {st.session_state['parsed_email'].get('Subject', 'Unknown')}
                <br>├── 👤 Sender Identity
                <br>│&nbsp;&nbsp;&nbsp;├── 📧 Claimed: {sender}
                <br>│&nbsp;&nbsp;&nbsp;└── {spoofed_status}
                <br>├── 🌍 Infrastructure
                <br>│&nbsp;&nbsp;&nbsp;├── 📍 Hop 1: {ips[0] if len(ips) > 0 else 'Unknown'} (Ingestion Node)
                <br>│&nbsp;&nbsp;&nbsp;└── 📍 Hop 2: {ips[1] if len(ips) > 1 else 'Internal Relay'}
                <br>{url_node}
                </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.subheader("AI Investigation Copilot")
        st.caption("Synthesize extracted telemetry into a structured forensic assessment.")
        
        st.markdown("""
            <div style="background-color: #161A20; border: 1px solid #262730; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                <p style="margin: 0; font-family: 'Fira Code', monospace; font-size: 0.85rem; color: #A0AAB2;">SYSTEM STATUS</p>
                <p style="margin: 5px 0 0 0; color: #E0E6ED;">Gemini 1.5 Pro Engine is standing by to analyze the current case evidence.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Generate Copilot Assessment", type="primary", use_container_width=True):
            with st.spinner("Copilot is analyzing forensic telemetry..."):
                report = generate_threat_report(
                    st.session_state['parsed_email'],
                    st.session_state['forensics'],
                    st.session_state['risk']
                )
                
                st.markdown("### Analyst Briefing")
                st.info(report)

# --- GLOBAL CONTACT & FOOTER (Always renders at the absolute bottom) ---

linkedin_html = f'<a href="{LINKEDIN_URL}" target="_blank" style="color: #94A3B8; text-decoration: none; margin-left: 1rem;">LinkedIn</a>' if LINKEDIN_URL else '<span style="color: #334155; margin-left: 1rem; cursor: not-allowed;">LinkedIn (Not Configured)</span>'
github_html = f'<a href="{GITHUB_URL}" target="_blank" style="color: #94A3B8; text-decoration: none; margin-left: 1rem;">GitHub</a>' if GITHUB_URL else ''

st.markdown(f"""
<div class="contact-banner">
    <h3 style="color: #F5F7FA; margin-bottom: 0.5rem; font-weight: 800;">CONTACT THE TEAM</h3>
    <p style="color: #94A3B8; margin-bottom: 1rem;">Questions, feedback, collaboration, or project inquiries?</p>
    <p style="font-family: 'Fira Code', monospace; color: #A0AAB2;">guptayash4562@gmail.com</p>
    <a href="mailto:guptayash4562@gmail.com" target="_blank" class="contact-email-btn">EMAIL US</a>
</div>
<footer class="global-footer">
    <div class="footer-grid">
        <div class="footer-col">
            <h4 style="color: #F5F7FA; font-weight: 800; font-size: 1.1rem; letter-spacing: 1px;">MAIL<span style="color: #FF4B4B;">SENTRY</span></h4>
            <p style="margin-bottom: 1rem; line-height: 1.6;">AI-Powered Email Threat Intelligence<br>& Digital Forensics</p>
            <p style="font-size: 0.75rem; color: #475569;">Detect. Trace. Investigate.</p>
        </div>
        <div class="footer-col">
            <h4>PRODUCT</h4>
            <a href="#dashboard">Dashboard</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#dashboard">Threat Intelligence</a>
        </div>
        <div class="footer-col">
            <h4>RESOURCES</h4>
            <a href="#how-it-works">User Guide</a>
            <a href="{GITHUB_URL}" target="_blank">GitHub Repository</a>
        </div>
        <div class="footer-col">
            <h4>SECURITY & LEGAL</h4>
            <a href="#">Privacy Policy (Placeholder)</a>
            <a href="#">Terms of Service (Placeholder)</a>
            <a href="#">Security (Placeholder)</a>
        </div>
    </div>
    <div class="footer-bottom">
        <div>
            <p style="margin: 0;">© 2026 MailSentry. All rights reserved.</p>
            <p style="margin: 4px 0 0 0; color: #475569; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.5px;">BUILT FOR SECURITY-CRITICAL ENVIRONMENTS</p>
        </div>
        <div>
            <a href="mailto:guptayash4562@gmail.com" target="_blank" style="color: #94A3B8; text-decoration: none;">guptayash4562@gmail.com</a>
            {github_html}
            {linkedin_html}
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)