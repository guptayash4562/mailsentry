"""
MailSentry SOC Authentication Interface
Cyberpunk-styled, dark mode Firebase Login, Registration, and Password Reset UI.
"""

import streamlit as st
from components.branding import get_logo_svg
from core.auth import (
    sign_in_with_password,
    sign_up_with_password,
    send_password_reset_email,
    login_user,
    demo_analyst_login
)
from core.config import FIREBASE_PROJECT_ID


def render_auth_portal():
    """Renders the central SOC Authentication and Identity Gateway."""
    
    # Outer layout container
    col_left, col_center, col_right = st.columns([1, 2.4, 1])

    with col_center:
        # Header Brand Lockup
        logo_svg = get_logo_svg(variant="color", size=48)
        header_html = f"""<div style="text-align: center; margin-top: 1rem; margin-bottom: 1.5rem;"><div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 0.8rem;">{logo_svg}<div style="font-family: 'Inter', sans-serif; font-weight: 900; font-size: 2rem; letter-spacing: 2px;"><span style="color: #F5F7FA;">MAIL</span><span style="color: #FF4B4B;">SENTRY</span></div></div><div style="font-family: 'Fira Code', monospace; color: #00D9FF; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase;">🛡️ SOC IDENTITY & ACCESS GATEWAY</div><p style="color: #64748B; font-family: 'Inter', sans-serif; font-size: 0.9rem; margin-top: 6px;">Zero-Trust Forensic Authentication • Powered by Firebase Identity Platform</p></div>"""
        st.markdown(header_html, unsafe_allow_html=True)

        # Status & Diagnostic Pills
        pills_html = f"""<div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 1.5rem;"><span class="status-pill pill-green">FIREBASE NODE: {FIREBASE_PROJECT_ID}</span><span class="status-pill pill-gray">TLS 1.3 ENCRYPTED</span><span class="status-pill pill-amber">TIER-3 RBAC</span></div>"""
        st.markdown(pills_html, unsafe_allow_html=True)

        # Main Authentication Card
        st.markdown('<div class="auth-card-wrapper">', unsafe_allow_html=True)
        
        tab_login, tab_register, tab_reset, tab_demo = st.tabs([
            "🔐 Analyst Login",
            "📝 Register Profile",
            "🔑 Reset Key",
            "⚡ Quick Demo Access"
        ])

        # --- TAB 1: LOGIN ---
        with tab_login:
            st.markdown("##### 🔐 Authenticate Analyst Credentials")
            st.caption("Provide registered SOC credentials to decrypt and access investigative tools.")
            
            with st.form(key="login_form", clear_on_submit=False):
                login_email = st.text_input(
                    "Analyst Email / User ID",
                    placeholder="analyst@mailsentry.soc",
                    help="Enter your Firebase registered email address"
                )
                login_password = st.text_input(
                    "Access Key / Password",
                    type="password",
                    placeholder="••••••••••••",
                    help="Your secure account password"
                )
                
                remember_me = st.checkbox("Keep SOC Session Active (Persistent Auth)", value=True)
                
                submit_login = st.form_submit_button(
                    "AUTHENTICATE ANALYST",
                    type="primary",
                    use_container_width=True
                )
                
                if submit_login:
                    if not login_email or not login_password:
                        st.error("⚠️ Please specify both your Analyst Email and Password.")
                    else:
                        with st.spinner("Verifying credentials with Firebase Identity Platform..."):
                            result = sign_in_with_password(login_email, login_password)
                            
                            if result.get("success"):
                                user = result.get("user")
                                login_user(user)
                                st.success(f"✅ Access Granted. Welcome, **{user.get('displayName')}**.")
                                st.rerun()
                            else:
                                st.error(result.get("error"))

        # --- TAB 2: REGISTER ---
        with tab_register:
            st.markdown("##### 📝 Register SOC Analyst Profile")
            st.caption("Provision a new investigator profile within the Firebase Identity Cluster.")
            
            with st.form(key="register_form", clear_on_submit=False):
                reg_name = st.text_input(
                    "Analyst Callsign / Full Name",
                    placeholder="e.g. Agent Alex Vance",
                    help="Display name for investigation audit logs"
                )
                reg_email = st.text_input(
                    "Official Email Address",
                    placeholder="analyst@agency.soc",
                    help="Official email for account identity"
                )
                reg_pass1 = st.text_input(
                    "Master Access Key (Password)",
                    type="password",
                    placeholder="Minimum 6 characters",
                    help="Strong password meeting forensic access standards"
                )
                reg_pass2 = st.text_input(
                    "Confirm Access Key",
                    type="password",
                    placeholder="Repeat password",
                    help="Must match master access key"
                )
                
                submit_register = st.form_submit_button(
                    "PROVISION ANALYST CREDENTIALS",
                    type="primary",
                    use_container_width=True
                )
                
                if submit_register:
                    if not reg_email or not reg_pass1:
                        st.error("⚠️ Email and Password are required for registration.")
                    elif len(reg_pass1) < 6:
                        st.error("⚠️ Security Policy: Password must be at least 6 characters long.")
                    elif reg_pass1 != reg_pass2:
                        st.error("⚠️ Password mismatch. Please verify confirmation entry.")
                    else:
                        with st.spinner("Provisioning new identity on Firebase cluster..."):
                            result = sign_up_with_password(reg_email, reg_pass1, reg_name)
                            
                            if result.get("success"):
                                user = result.get("user")
                                login_user(user)
                                st.success(f"🎉 Identity Provisioned Successfully! Welcome, **{user.get('displayName')}**.")
                                st.rerun()
                            else:
                                st.error(result.get("error"))

        # --- TAB 3: PASSWORD RESET ---
        with tab_reset:
            st.markdown("##### 🔑 Reset Access Credentials")
            st.caption("Dispatch an automated cryptographic password recovery link via Firebase.")
            
            with st.form(key="reset_form", clear_on_submit=False):
                reset_email = st.text_input(
                    "Registered Analyst Email",
                    placeholder="analyst@mailsentry.soc",
                    help="The email associated with your SOC analyst account"
                )
                
                submit_reset = st.form_submit_button(
                    "DISPATCH RECOVERY LINK",
                    type="secondary",
                    use_container_width=True
                )
                
                if submit_reset:
                    if not reset_email:
                        st.error("⚠️ Please specify the target analyst email address.")
                    else:
                        with st.spinner("Dispatching reset payload..."):
                            result = send_password_reset_email(reset_email)
                            if result.get("success"):
                                st.success(result.get("message"))
                            else:
                                st.error(result.get("error"))

        # --- TAB 4: DEMO / QUICK ACCESS ---
        with tab_demo:
            st.markdown("##### ⚡ Quick Access / Demonstration Mode")
            st.caption("Instant bypass for technical judges, live pitches, or offline forensic demonstrations.")
            
            demo_role = st.selectbox(
                "Select Clearance & Profile:",
                [
                    "Tier-3 Lead Incident Responder (Agent Zero)",
                    "Digital Forensics & Malware Specialist (Agent Vance)",
                    "SOC Threat Intelligence Supervisor (Director Ross)"
                ]
            )
            
            callsign_map = {
                "Tier-3 Lead Incident Responder (Agent Zero)": ("Agent Zero", "agent.zero@mailsentry.soc"),
                "Digital Forensics & Malware Specialist (Agent Vance)": ("Analyst Vance", "vance.malware@mailsentry.soc"),
                "SOC Threat Intelligence Supervisor (Director Ross)": ("Director Ross", "director.ross@mailsentry.soc")
            }
            
            name, email = callsign_map.get(demo_role, ("SOC Specialist", "analyst@mailsentry.soc"))
            
            if st.button("ENTER SOC WORKSTATION (DEMO CLEARANCE)", type="primary", use_container_width=True):
                user = demo_analyst_login(callsign=name, email=email)
                st.success(f"✅ Demo Clearance Granted. Welcome, **{user.get('displayName')}**.")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Footer info inside center column
        footer_html = """<div style="text-align: center; margin-top: 2rem; color: #475569; font-size: 0.8rem; font-family: 'Inter', sans-serif;">🔒 All authentication requests are secured via TLS and audited for tamper-evident chain of custody.<br>© 2026 MailSentry SOC Workstation • Identity Cluster v2.4</div>"""
        st.markdown(footer_html, unsafe_allow_html=True)