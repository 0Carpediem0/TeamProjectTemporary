import hashlib


def hash_password(password: str) -> str:
    '''
    Функция для вычисления SHA-256 хэша пароля.
    '''
    
    encode_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encode_password).hexdigest()
    return hashed_password
