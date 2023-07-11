from passlib.hash import sha256_crypt

def hashed(password):
    hashed_password = sha256_crypt.hash(password)
    return hashed_password

def dehashed(password, hashed):
    try:
        a = sha256_crypt.verify(password, hashed)
        return a
    except Exception:
        return False

