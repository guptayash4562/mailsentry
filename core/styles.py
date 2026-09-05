"""
MailSentry Enterprise Cyber SOC Design System
Styles and UI Components inspired by Google Chronicle, CrowdStrike Falcon, and Cloudflare Radar.
"""

def get_custom_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-dark: #0a0e17;
        --card-bg: rgba(17, 24, 39, 0.75);
        --card-border: rgba(30, 41, 59, 0.85);
        --accent-cyan: #00e5ff;
        --accent-glow: rgba(0, 229, 255, 0.25);
        --danger-red: #ef4444;
        --danger-glow: rgba(239, 68, 68, 0.25);
        --warning-amber: #f59e0b;
        --safe-emerald: #10b981;
        --text-primary: #f8fafc;
        --text-muted: #94a3b8;
    }

    /* Global Body Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }

    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Top Enterprise Header Bar */
    .soc-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid rgba(0, 229, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        padding: 12px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }

    .soc-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .soc-brand-icon {
        font-size: 28px;
        filter: drop-shadow(0 0 12px var(--accent-cyan));
    }

    .soc-brand-title {
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #00e5ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .soc-telemetry {
        display: flex;
        gap: 20px;
        font-size: 12px;
        font-family: 'JetBrains Mono', monospace;
    }

    .telemetry-item {
        display: flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 0, 0, 0.4);
        padding: 5px 12px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px currentColor;
        animation: pulseAnimation 2s infinite ease-in-out;
    }

    .pulse-dot.cyan { color: #00e5ff; background-color: #00e5ff; }
    .pulse-dot.green { color: #10b981; background-color: #10b981; }
    .pulse-dot.red { color: #ef4444; background-color: #ef4444; }
    .pulse-dot.amber { color: #f59e0b; background-color: #f59e0b; }

    @keyframes pulseAnimation {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Enterprise Glass Cards */
    .soc-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(16px);
        margin-bottom: 20px;
        transition: all 0.25s ease;
    }

    .soc-card:hover {
        border-color: rgba(0, 229, 255, 0.4);
        box-shadow: 0 12px 36px rgba(0, 229, 255, 0.08);
    }

    .soc-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        padding-bottom: 12px;
        margin-bottom: 16px;
    }

    .soc-card-title {
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Severity Badges */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .badge-critical {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #f87171;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
    }

    .badge-suspicious {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #fbbf24;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
    }

    .badge-benign {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.5);
        color: #34d399;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }

    .badge-info {
        background: rgba(0, 229, 255, 0.15);
        border: 1px solid rgba(0, 229, 255, 0.5);
        color: #38bdf8;
    }

    /* SOC Metric Counter Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .metric-box {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.4) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px;
        position: relative;
        overflow: hidden;
    }

    .metric-box::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    }

    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }

    .metric-sub {
        font-size: 11px;
        color: var(--text-muted);
        margin-top: 4px;
    }

    /* Timeline & Relay Nodes */
    .relay-node {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.15s ease;
    }

    .relay-node:hover {
        transform: translateX(4px);
        border-color: var(--accent-cyan);
    }

    /* Streamlit element overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 13px;
        color: var(--text-muted);
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%) !important;
        color: #00e5ff !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
    }

    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        letter-spacing: 0.03em;
        transition: all 0.2s ease;
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        border: none;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
    }

    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(0, 198, 255, 0.6);
        transform: translateY(-1px);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0e17;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00e5ff;
    }
    </style>
    """
