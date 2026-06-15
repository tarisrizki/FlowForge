import hmac
import hashlib
from app.core.config import settings

def verify_hmac_signature(payload: bytes, signature_header: str) -> bool:
    """
    Verifies the HMAC SHA256 signature of a webhook payload.
    Expected signature_header format: 'sha256=...' or just the hex string.
    """
    if not signature_header:
        return False
        
    # Support GitHub style "sha256=HEX"
    if signature_header.startswith("sha256="):
        signature_header = signature_header.split("=")[1]
        
    secret = settings.WEBHOOK_SECRET.encode('utf-8')
    computed_hmac = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(computed_hmac, signature_header)
