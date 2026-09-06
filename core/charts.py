import plotly.graph_objects as go
import re

def parse_risk_factors(reasons):
    parsed = []
    
    for r in reasons:
        factor_name = "Risk Signal"
        contribution = 0
        severity = "WARNING"
        reason_text = ""
        
        if isinstance(r, dict):
            raw_text = r.get('text', '')
            severity = r.get('level', 'WARNING').upper()
            reason_text = raw_text
            
            match = re.search(r'\(([+-]\d+)\)', raw_text)
            if match:
                contribution = int(match.group(1))
                factor_name = re.sub(r'\s*\([+-]\d+\)\s*', '', raw_text).strip()
            else:
                factor_name = raw_text
                
        elif isinstance(r, str):
            reason_text = r
            match = re.search(r'\(([+-]\d+)\)', r)
            if match:
                contribution = int(match.group(1))
                factor_name = re.sub(r'\([+-]\d+\)', '', r).replace('CRITICAL:', '').replace('WARNING:', '').strip()
            else:
                factor_name = r
                
            if "CRITICAL" in r.upper(): severity = "CRITICAL"
            elif "SAFE" in r.upper() or "-" in str(contribution): severity = "MITIGATION"
            
        # Create ultra-short labels for the x-axis
        short_name = factor_name.split('-')[0].strip()
        if len(short_name) > 18:
            short_name = short_name[:15] + "..."
            
        parsed.append({
            "short_name": short_name,
            "full_name": factor_name,
            "value": contribution,
            "severity": severity,
            "reason": reason_text
        })
        
    return parsed

def render_risk_decomposition(risk_data):
    final_score = int(risk_data.get('score', 0))
    reasons = risk_data.get('reasons', [])
    factors = parse_risk_factors(reasons)
    
    x_labels = []
    y_values = []
    bases = []
    colors = []
    hover_texts = []
    text_vals = []
    
    current_base = 0
    
    # 1. Plot Individual Signals
    for f in factors:
        x_labels.append(f['short_name'])
        val = f['value']
        y_values.append(val)
        bases.append(current_base)
        text_vals.append(f"+{val}" if val > 0 else str(val))
        
        if f['severity'] == "CRITICAL": colors.append("#F43F5E")       # Red
        elif f['severity'] == "MITIGATION": colors.append("#22C55E")   # Green
        else: colors.append("#F59E0B")                                 # Amber
            
        hover_texts.append(f"<b>{f['full_name']}</b><br>Severity: {f['severity']}<br>Contribution: {'+' if val>0 else ''}{val}<br><i>{f['reason']}</i>")
        current_base += val

    raw_total = current_base
    
    # 2. Raw Signal Total Anchor
    x_labels.append("Raw Total")
    y_values.append(raw_total)
    bases.append(0)
    colors.append("#2563EB") # Blue 
    text_vals.append(str(raw_total))
    hover_texts.append(f"<b>Raw Signal Total</b><br>Cumulative sum before normalization: {raw_total}")

    # 3. Engine Normalization / Transformation
    normalization = final_score - raw_total
    if normalization != 0:
        x_labels.append("Normalization")
        y_values.append(normalization)
        bases.append(raw_total)
        colors.append("#94A3B8") # Neutral Gray
        text_vals.append(str(normalization))
        hover_texts.append(f"<b>Score Normalization</b><br>Mathematical constraint applied: {normalization}")

    # 4. Final Score Anchor
    x_labels.append("Final Score")
    y_values.append(final_score)
    bases.append(0)
    colors.append("#2563EB") # Blue
    text_vals.append(str(final_score))
    hover_texts.append(f"<b>Final Risk Score</b><br>Engine Output: {final_score}")

    # 5. Render as a Custom Bar Chart (Bypasses Plotly Waterfall Limitations)
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=y_values,
        base=bases,
        marker_color=colors,
        text=text_vals,
        textposition="outside",
        hoverinfo="text",
        hovertext=hover_texts,
        width=0.7
    ))

    # Analytical Light Theme
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#0F172A", size=11),
        margin=dict(l=20, r=20, t=30, b=40),
        xaxis=dict(showgrid=False, tickangle=0),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", zeroline=True, zerolinecolor="#94A3B8", title="Points"),
        height=380,
        showlegend=False
    )
    
    # Build Summary Metrics
    critical_signals = len([f for f in factors if f['severity'] == "CRITICAL"])
    warning_signals = len([f for f in factors if f['severity'] == "WARNING"])
    
    top_driver = "None"
    if len(factors) > 0:
        worst_factor = max(factors, key=lambda x: x['value'])
        if worst_factor['value'] > 0:
            top_driver = worst_factor['short_name']
            
    summary = {
        "final_score": final_score,
        "raw_total": raw_total,
        "top_driver": top_driver,
        "critical_signals": critical_signals,
        "warning_signals": warning_signals,
        "factors": factors
    }
    
    return fig, summary