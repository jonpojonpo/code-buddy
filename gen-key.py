import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)

new_api_key = generate_api_key()
print("Your new API key:", new_api_key)
