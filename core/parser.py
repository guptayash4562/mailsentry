import email
from email import policy
import email.utils
import hashlib
import re

SUSPICIOUS_EXTENSIONS = {
    '.exe', '.scr', '.vbs', '.js', '.bat', '.cmd', '.ps1',
    '.iso', '.img', '.hta', '.jar', '.wsf', '.cpl', '.dll'
}

def parse_eml_bytes(file_bytes):
    """
    Enterprise-grade parser extracting structural headers, authentication tags,
    relay hops, attachments with cryptographic hashes, and body contents.
    """
    msg = email.message_from_bytes(file_bytes, policy=policy.default)
    
    # Parse From field into display name and email address
    raw_from = msg.get("From", "Unknown")
    from_display_name, from_email = email.utils.parseaddr(raw_from)
    
    # Parse To field
    raw_to = msg.get("To", "Unknown")
    to_display_name, to_email = email.utils.parseaddr(raw_to)
    
    # Parse Reply-To field
    raw_reply_to = msg.get("Reply-To", "")
    reply_to_display, reply_to_email = email.utils.parseaddr(raw_reply_to) if raw_reply_to else ("", "")

    # Extract all Received headers in chronological order (top is most recent, bottom is originating)
    received_headers = msg.get_all("Received", [])
    
    # Extract attachments & text bodies
    plain_body = ""
    html_body = ""
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition") or "")
            filename = part.get_filename()
            
            if filename or "attachment" in content_disposition:
                payload = part.get_payload(decode=True) or b""
                sha256_hash = hashlib.sha256(payload).hexdigest() if payload else ""
                ext = ("." + filename.split(".")[-1].lower()) if filename and "." in filename else ""
                
                attachments.append({
                    "filename": filename or "unnamed_attachment",
                    "content_type": content_type,
                    "size_bytes": len(payload),
                    "sha256": sha256_hash,
                    "is_risky": ext in SUSPICIOUS_EXTENSIONS,
                    "extension": ext
                })
            elif content_type == "text/plain" and not plain_body:
                try:
                    payload = part.get_payload(decode=True)
                    plain_body = payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
                except Exception:
                    plain_body = str(part.get_payload())
            elif content_type == "text/html" and not html_body:
                try:
                    payload = part.get_payload(decode=True)
                    html_body = payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
                except Exception:
                    html_body = str(part.get_payload())
    else:
        content_type = msg.get_content_type()
        try:
            payload = msg.get_payload(decode=True)
            text = payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore') if payload else str(msg.get_payload())
        except Exception:
            text = str(msg.get_payload())
            
        if content_type == "text/html":
            html_body = text
        else:
            plain_body = text

    # Fallback body extraction if plain text is empty
    if not plain_body and html_body:
        # Strip simple HTML tags for text representation
        clean_text = re.sub(r'<style.*?</style>', '', html_body, flags=re.DOTALL)
        clean_text = re.sub(r'<script.*?</script>', '', clean_text, flags=re.DOTALL)
        clean_text = re.sub(r'<[^<]+?>', ' ', clean_text)
        plain_body = ' '.join(clean_text.split())

    return {
        "Subject": msg.get("Subject", "No Subject"),
        "From": raw_from,
        "From_Display": from_display_name,
        "From_Email": from_email,
        "To": raw_to,
        "To_Display": to_display_name,
        "To_Email": to_email,
        "Reply_To": raw_reply_to,
        "Reply_To_Email": reply_to_email,
        "Date": msg.get("Date", "Unknown"),
        "Message-ID": msg.get("Message-ID", "None"),
        "Return-Path": msg.get("Return-Path", "None"),
        "Received_SPF": msg.get("Received-SPF", "None"),
        "Authentication_Results": msg.get("Authentication-Results", "None"),
        "DKIM_Signature": msg.get("DKIM-Signature", "None"),
        "X_Mailer": msg.get("X-Mailer", msg.get("User-Agent", "Not Disclosed")),
        "X_Originating_IP": msg.get("X-Originating-IP", "None"),
        "Received_Hops": received_headers,
        "Headers": dict(msg.items()),
        "Body": plain_body.strip(),
        "HTML_Body": html_body,
        "Attachments": attachments
    }