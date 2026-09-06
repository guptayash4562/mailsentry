import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
    /* Forensic Panel Styling */
    .forensic-card {
        background-color: #0E1117;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .forensic-card-header {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .forensic-value {
        font-family: 'Fira Code', monospace;
        color: #E0E6ED;
        font-size: 0.9rem;
        word-break: break-all;
    }
    .status-pass { color: #22C55E; font-weight: bold; }
    .status-fail { color: #F43F5E; font-weight: bold; }
    .status-warn { color: #F59E0B; font-weight: bold; }
    
    /* Contact & Global Footer */
    .contact-banner {
        background-color: #0E1117;
        border-top: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
        padding: 4rem 2rem;
        text-align: center;
        margin-top: 4rem;
    }
    .contact-email-btn {
        display: inline-block;
        background-color: #2563EB;
        color: #FFFFFF !important;
        padding: 0.75rem 2rem;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 1.5rem;
        transition: background-color 0.2s;
    }
    .contact-email-btn:hover { background-color: #1D4ED8; }
    
    .global-footer {
        background-color: #070B14;
        padding: 4rem 2rem 2rem 2rem;
        color: #64748B;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }
    .footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .footer-col h4 {
        color: #F5F7FA;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    .footer-col a {
        display: block;
        color: #94A3B8;
        text-decoration: none;
        margin-bottom: 0.75rem;
        transition: color 0.2s;
    }
    .footer-col a:hover { color: #F5F7FA; }
    .footer-bottom {
        max-width: 1200px;
        margin: 3rem auto 0 auto;
        padding-top: 2rem;
        border-top: 1px solid #1E293B;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    /* 1. Make Streamlit's native header invisible and let clicks pass through to your links */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 999999 !important;
        pointer-events: none !important; 
    }

    /* 2. Re-enable clicks ONLY for the native sidebar toggle and deploy menu */
    header[data-testid="stHeader"] * {
        pointer-events: auto !important;
    }

    /* 3. Push the main app content down so the fixed header doesn't cover the title */
    .block-container {
        padding-top: 80px !important;
    }

    /* 4. Enable smooth scrolling across the Streamlit container */
    html, body, [data-testid="stAppViewContainer"] {
        scroll-behavior: smooth;
    }

    /* 5. Prevent fixed header from overlapping anchor targets */
    .anchor-offset {
        scroll-margin-top: 90px;
    }

    /* 6. The Custom Fixed Header */
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #070B14;
        border-bottom: 1px solid #1E293B;
        z-index: 999998; /* Just below the native header so toggle button stays on top */
        display: flex;
        justify-content: space-between;
        align-items: center;
        /* 4rem left dodges the sidebar toggle, 8rem right dodges deploy menu */
        padding: 0 8rem 0 4rem; 
    }

    .header-brand {
        font-family: 'Inter', sans-serif, monospace;
        font-weight: 800;
        font-size: 1.2rem;
        color: #F5F7FA;
        letter-spacing: 1px;
    }

    .header-brand span {
        color: #FF4B4B;
    }

    .header-links {
        display: flex;
        gap: 2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .header-links a {
        color: #A0AAB2;
        text-decoration: none;
        transition: color 0.2s;
    }

    .header-links a:hover {
        color: #F5F7FA;
    }
    </style>
    """, unsafe_allow_html=True)