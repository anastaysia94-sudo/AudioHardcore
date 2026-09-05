from __future__ import annotations
import base64, hashlib, hmac, json, secrets, time

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + '=' * (-len(value) % 4))

def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f'scrypt${_b64(salt)}${_b64(digest)}'

def verify_password(password: str, encoded: str) -> bool:
    try:
        algo, salt, expected = encoded.split('$', 2)
        if algo != 'scrypt': return False
        digest = hashlib.scrypt(password.encode(), salt=_unb64(salt), n=2**14, r=8, p=1)
        return hmac.compare_digest(_b64(digest), expected)
    except Exception:
        return False

def issue_token(user_id: str, secret: str, ttl_seconds: int = 86400) -> str:
    header = _b64(json.dumps({'alg':'HS256','typ':'AH1'}, separators=(',',':')).encode())
    payload = _b64(json.dumps({'sub':user_id,'exp':int(time.time())+ttl_seconds}, separators=(',',':')).encode())
    body=f'{header}.{payload}'.encode(); sig=hmac.new(secret.encode(),body,hashlib.sha256).digest()
    return f'{header}.{payload}.{_b64(sig)}'

def verify_token(token: str, secret: str) -> str | None:
    try:
        header,payload,sig=token.split('.')
        expected=hmac.new(secret.encode(),f'{header}.{payload}'.encode(),hashlib.sha256).digest()
        if not hmac.compare_digest(_unb64(sig),expected): return None
        data=json.loads(_unb64(payload))
        if int(data.get('exp',0)) < int(time.time()): return None
        return str(data['sub'])
    except Exception:
        return None
