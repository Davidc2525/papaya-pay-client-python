import hmac
import hashlib
import time
import json
from typing import Optional

from .types import WebhookEvent, Transaction
from .errors import InvalidSignatureFormat, ToleranceExceeded, SignatureMismatch

DEFAULT_TOLERANCE_SECONDS = 300

def construct_event(
    raw_payload: bytes, 
    signature_header: str, 
    secret: str, 
    tolerance: Optional[int] = None
) -> WebhookEvent:
    if tolerance is None:
        tolerance = DEFAULT_TOLERANCE_SECONDS
        
    parts = signature_header.split(',')
    t_str = None
    v1_str = None
    
    for part in parts:
        kv = part.split('=', 1)
        if len(kv) == 2:
            if kv[0] == 't':
                t_str = kv[1]
            elif kv[0] == 'v1':
                v1_str = kv[1]
                
    if not t_str or not v1_str:
        raise InvalidSignatureFormat("Missing timestamp or signature in header")
        
    try:
        timestamp = int(t_str)
    except ValueError:
        raise InvalidSignatureFormat("Timestamp is not a valid integer")
        
    now = int(time.time())
    
    if abs(now - timestamp) > tolerance:
        raise ToleranceExceeded("Webhook timestamp is too old or too far in the future")
        
    # Calcular el HMAC
    mac = hmac.new(secret.encode('utf-8'), digestmod=hashlib.sha256)
    mac.update(t_str.encode('utf-8'))
    mac.update(b'.')
    mac.update(raw_payload)
    
    expected_sig = mac.hexdigest()
    
    # Comparación segura en tiempo constante
    if not hmac.compare_digest(expected_sig, v1_str):
        raise SignatureMismatch("Signatures do not match")
        
    try:
        data = json.loads(raw_payload.decode('utf-8'))
        return WebhookEvent(
            app_id=data.get('app_id', ''),
            checkout_id=data.get('checkout_id', ''),
            status=data.get('status', ''),
            transaction=Transaction(**data.get('transaction', {}))
        )
    except json.JSONDecodeError:
        raise InvalidSignatureFormat("Invalid JSON payload")
