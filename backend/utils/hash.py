import hashlib


def hash_password(password: str) -> str:
    encode_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encode_password).hexdigest()
    return hashed_password
