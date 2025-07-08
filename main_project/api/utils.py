import secrets

def generate_api_keys():
    public_key = secrets.token_hex(16)
    private_key = secrets.token_hex(32)
    return public_key, private_key