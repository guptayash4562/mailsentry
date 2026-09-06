# components/branding.py

def get_logo_svg(variant="color", size=32):
    """
    Returns the pure SVG string for the MailSentry 'S-Signal' logo.
    variant: 'color', 'white', or 'dark'
    """
    if variant == "white":
        stroke, node_start, node_end = "#FFFFFF", "#FFFFFF", "#FFFFFF"
    elif variant == "dark":
        stroke, node_start, node_end = "#A7B2C2", "#A7B2C2", "#A7B2C2"
    else:
        # Official Brand Palette
        stroke, node_start, node_end = "#2563EB", "#00D9FF", "#F5F7FA"

    return f"""
    <svg viewBox="0 0 100 100" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
        <!-- Continuous Origin Trace (S-Signal) -->
        <path d="M 75 25 L 30 25 L 30 50 L 70 50 L 70 75 L 25 75" 
              fill="none" stroke="{stroke}" stroke-width="10" 
              stroke-linejoin="round" stroke-linecap="round"/>
        <!-- Origin Node (Top Right) -->
        <circle cx="75" cy="25" r="10" fill="{node_start}"/>
        <!-- Target Node (Bottom Left) -->
        <circle cx="25" cy="75" r="10" fill="{node_end}"/>
    </svg>
    """

def get_header_lockup():
    """Horizontal logo + wordmark for the fixed sticky navigation."""
    logo = get_logo_svg(variant="color", size=28)
    return f"""
    <div style="display: flex; align-items: center; gap: 12px; cursor: pointer;">
        {logo}
        <div style="font-family: 'Inter', sans-serif; font-weight: 800; font-size: 1.2rem; letter-spacing: 1px;">
            <span style="color: #F5F7FA;">MAIL</span><span style="color: #00D9FF;">SENTRY</span>
        </div>
    </div>
    """