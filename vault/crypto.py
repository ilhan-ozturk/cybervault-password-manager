import base64, hashlib, hmac, os
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


def _fernet_key():
    configured=os.getenv('VAULT_ENCRYPTION_KEY','').strip()
    if configured:
        return configured.encode()
    # Development fallback: deterministic per Django secret. Production should set VAULT_ENCRYPTION_KEY.
    digest=hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_text(value):
    if not value: return ''
    return Fernet(_fernet_key()).encrypt(value.encode()).decode()

def decrypt_text(value):
    if not value: return ''
    try: return Fernet(_fernet_key()).decrypt(value.encode()).decode()
    except InvalidToken: return '[Unable to decrypt: encryption key changed]'

def password_fingerprint(value):
    key=os.getenv('VAULT_FINGERPRINT_KEY', settings.SECRET_KEY).encode()
    return hmac.new(key, value.encode(), hashlib.sha256).hexdigest()
