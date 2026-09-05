def calculate_risk(parsed_data, forensic_data):
    """
    Multi-dimensional SOC risk evaluation engine.
    Calculates overall score, vector scores (0-100 for radar analysis), and itemized reasons.
    """
    reasons = []
    
    # 1. Vector: Domain & Authentication (Max 35 points towards overall)
    domain_score = 0
    auth = forensic_data.get("Auth_Matrix", {})
    if auth.get("SPF") == "FAIL":
        domain_score += 40
        reasons.append({"level": "CRITICAL", "icon": "🚨", "text": "SPF Authentication Failed - Unauthorized transmitting server (+40)"})
    elif auth.get("SPF") == "SOFTFAIL":
        domain_score += 20
        reasons.append({"level": "WARNING", "icon": "⚠️", "text": "SPF Softfail detected (+20)"})

    if auth.get("DKIM") == "FAIL":
        domain_score += 35
        reasons.append({"level": "CRITICAL", "icon": "🚨", "text": "DKIM Cryptographic Signature Invalid - Message tampered (+35)"})

    if auth.get("DMARC") == "FAIL":
        domain_score += 40
        reasons.append({"level": "CRITICAL", "icon": "🚨", "text": "DMARC Policy Rejection - Domain alignment failed (+40)"})

    if forensic_data.get("Spoofed_Sender"):
        domain_score += 45
        for detail in forensic_data.get("Spoof_Details", []):
            reasons.append({"level": "CRITICAL", "icon": "🚨", "text": f"{detail} (+45)"})
            
    domain_vector = min(100, domain_score)

    # 2. Vector: URL Threats (Max 30 points towards overall)
    url_score = 0
    analyzed_urls = forensic_data.get("Analyzed_URLs", [])
    for u in analyzed_urls:
        if u.get("risk") == "CRITICAL":
            url_score += 50
            reasons.append({"level": "CRITICAL", "icon": "🔗", "text": f"Critical URL detected: {u['url']} ({'; '.join(u['flags'])})"})
        elif u.get("risk") == "HIGH":
            url_score += 30
            reasons.append({"level": "WARNING", "icon": "🔗", "text": f"High-risk URL: {u['url']} ({'; '.join(u['flags'])})"})
        elif u.get("risk") == "SUSPICIOUS":
            url_score += 15
            reasons.append({"level": "WARNING", "icon": "🔗", "text": f"Suspicious URL keywords: {u['url']}"})
    url_vector = min(100, url_score)

    # 3. Vector: Social Engineering & Urgency (Max 25 points towards overall)
    social_score = 0
    body = parsed_data.get("Body", "").lower()
    urgent_keywords = [
        ("account suspended", 30), ("verify your account", 30), ("password expires", 25),
        ("unauthorized login", 25), ("immediate action", 20), ("wire transfer", 35),
        ("payment overdue", 25), ("tax penalty", 30), ("gift card", 30), ("confidential request", 20)
    ]
    detected_phrases = []
    for phrase, weight in urgent_keywords:
        if phrase in body:
            social_score += weight
            detected_phrases.append(phrase)
            
    if detected_phrases:
        reasons.append({"level": "WARNING", "icon": "⚠️", "text": f"Coercive Social Engineering detected: '{', '.join(detected_phrases[:3])}' (+{min(40, social_score)})"})
    social_vector = min(100, social_score)

    # 4. Vector: Payload & Attachment Risk (Max 25 points towards overall)
    payload_score = 0
    attachments = forensic_data.get("Attachments", [])
    for att in attachments:
        if att.get("is_risky"):
            payload_score += 60
            reasons.append({"level": "CRITICAL", "icon": "☣️", "text": f"High-Risk Weaponized Extension: {att['filename']} ({att['extension']})"})
        else:
            payload_score += 10
            reasons.append({"level": "INFO", "icon": "📎", "text": f"Attachment present: {att['filename']} ({att['size_bytes']} bytes)"})
    payload_vector = min(100, payload_score)

    # 5. Vector: Infrastructure & Relay Anomaly (Max 20 points towards overall)
    infra_score = 0
    for hop in forensic_data.get("Relay_Hops", []):
        geo = hop.get("geo", {})
        if geo.get("threat") in ["Hostile Infrastructure", "Anonymized Proxy"]:
            infra_score += 45
            reasons.append({"level": "CRITICAL", "icon": "🌐", "text": f"Transit through flagged infrastructure: {geo['ip']} ({geo['threat']}, {geo['country']})"})
    infra_vector = min(100, infra_score)

    # Weighted Overall Threat Score Calculation (0 - 100)
    composite_score = int(
        (domain_vector * 0.35) +
        (url_vector * 0.25) +
        (social_vector * 0.15) +
        (payload_vector * 0.15) +
        (infra_vector * 0.10)
    )
    composite_score = max(0, min(100, composite_score))

    # Classification Tier
    if composite_score >= 75:
        classification = "CRITICAL THREAT"
        badge_class = "badge-critical"
    elif composite_score >= 50:
        classification = "HIGH RISK / SUSPICIOUS"
        badge_class = "badge-suspicious"
    elif composite_score >= 25:
        classification = "ELEVATED RISK"
        badge_class = "badge-suspicious"
    else:
        classification = "LOW RISK / BENIGN"
        badge_class = "badge-benign"

    if not reasons:
        reasons.append({"level": "SAFE", "icon": "✅", "text": "All cryptographic signatures and sender domains verified authentic."})

    return {
        "score": composite_score,
        "classification": classification,
        "badge_class": badge_class,
        "reasons": reasons,
        "vectors": {
            "Domain Spoofing": domain_vector,
            "Malicious URLs": url_vector,
            "Social Engineering": social_vector,
            "Payload Risk": payload_vector,
            "Infra Anomalies": infra_vector
        }
    }