import hmac
import hashlib

def generate_signature(private_key):
    return hmac.new(
        key=private_key.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

