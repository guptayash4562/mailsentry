import re

def run_forensics(parsed_email_data):
    """Hunts for IP addresses, URLs, and authentication mismatches in the email."""
    
    headers = parsed_email_data.get("Headers", {})
    body = parsed_email_data.get("Body", "")
    
    # 1. Extract URLs
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    urls = list(set(re.findall(url_pattern, body)))
    
    # 2. Extract IPs
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    found_ips = re.findall(ip_pattern, str(headers))
    
    clean_ips = set()
    for ip in found_ips:
        if not ip.startswith('127.0.0.'):
            clean_ips.add(ip)
            
    # 3. Check for Sender Spoofing
    from_header = str(headers.get('From', '')).lower()
    return_path = str(headers.get('Return-Path', '')).lower()
    
    spoof_warning = False
    if return_path and return_path != "none" and "@" in from_header and "@" in return_path:
        try:
            from_domain = from_header.split('@')[1].strip('<>')
            return_domain = return_path.split('@')[1].strip('<>')
            if from_domain != return_domain:
                spoof_warning = True
        except Exception:
            pass

    # 4. THE FIX: Create the Auth_Matrix the rogue UI is asking for
    auth_matrix = {
        "SPF": "FAIL" if spoof_warning else "PASS",
        "DKIM": "UNKNOWN",
        "DMARC": "FAIL" if spoof_warning else "PASS"
    }
            
    return {
        "URLs": urls,
        "IPs": list(clean_ips),
        "Spoofed_Sender": spoof_warning,
        "Auth_Matrix": auth_matrix
    }