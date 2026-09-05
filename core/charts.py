# pyrefly: ignore [missing-import]
import plotly.graph_objects as go

def create_threat_gauge(score, classification):
    """Generates an enterprise-grade dark mode threat speedometer gauge."""
    if score >= 75:
        bar_color = "#ef4444"
    elif score >= 50:
        bar_color = "#f59e0b"
    elif score >= 25:
        bar_color = "#eab308"
    else:
        bar_color = "#10b981"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{classification}</b>", 'font': {'size': 14, 'color': '#94a3b8', 'family': 'Outfit'}},
        number={'suffix': "/100", 'font': {'size': 44, 'color': '#ffffff', 'family': 'Outfit'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155", 'tickfont': {'color': '#64748b'}},
            'bar': {'color': bar_color, 'thickness': 0.25},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [25, 50], 'color': 'rgba(234, 179, 8, 0.15)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(239, 68, 68, 0.25)'}
            ],
            'threshold': {
                'line': {'color': bar_color, 'width': 4},
                'thickness': 0.8,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=220,
        font={'family': 'Inter'}
    )
    return fig


def create_vector_radar(vectors):
    """Generates a multi-dimensional attack vector polar radar chart."""
    categories = list(vectors.keys())
    values = list(vectors.values())
    
    # Close polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(0, 229, 255, 0.2)',
        line=dict(color='#00e5ff', width=2),
        marker=dict(size=6, color='#00e5ff'),
        name='Threat Exposure'
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(15, 23, 42, 0.5)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color='#64748b'),
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color='#94a3b8', family='Outfit'),
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.1)'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=240,
        showlegend=False
    )
    return fig


def create_hop_geo_map(hop_geos):
    """Generates an interactive global transit map for email relay hops."""
    fig = go.Figure()

    if not hop_geos:
        # Default empty world view
        fig.update_layout(
            geo=dict(
                bgcolor='rgba(10, 14, 23, 1)',
                showland=True, landcolor='rgba(15, 23, 42, 1)',
                showocean=True, oceancolor='rgba(8, 11, 19, 1)',
                showcountries=True, countrycolor='rgba(255, 255, 255, 0.1)',
                coastlinecolor='rgba(0, 229, 255, 0.2)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            height=360,
            margin=dict(l=0, r=0, t=10, b=10)
        )
        return fig

    lats = [g['lat'] for g in hop_geos]
    lons = [g['lon'] for g in hop_geos]
    labels = [f"Hop {i+1}: {g['ip']}<br>{g['city']}, {g['country']}<br>{g['asn']}" for i, g in enumerate(hop_geos)]
    colors = []
    
    for g in hop_geos:
        t = g.get('threat', '')
        if 'Hostile' in t or 'Tor' in t:
            colors.append('#ef4444')
        elif 'Suspicious' in t or 'Anonymized' in t:
            colors.append('#f59e0b')
        else:
            colors.append('#00e5ff')

    # Draw flight paths between hops
    if len(hop_geos) > 1:
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            mode='lines',
            line=dict(width=2, color='rgba(0, 229, 255, 0.6)', dash='dash'),
            hoverinfo='none'
        ))

    # Draw nodes
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='markers+text',
        marker=dict(
            size=14,
            color=colors,
            line=dict(width=2, color='#ffffff'),
            opacity=0.9
        ),
        text=[f"Hop {i+1}" for i in range(len(hop_geos))],
        textposition="top right",
        textfont=dict(family="JetBrains Mono", size=10, color="#ffffff"),
        hoverinfo='text',
        hovertext=labels
    ))

    fig.update_layout(
        geo=dict(
            bgcolor='rgba(10, 14, 23, 1)',
            showland=True, landcolor='rgba(15, 23, 42, 1)',
            showocean=True, oceancolor='rgba(8, 11, 19, 1)',
            showcountries=True, countrycolor='rgba(255, 255, 255, 0.15)',
            coastlinecolor='rgba(0, 229, 255, 0.25)',
            showsubunits=True,
            projection_type='equirectangular'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=360,
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False
    )
    return fig
