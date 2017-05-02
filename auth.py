from passlib.hash import pbkdf2_sha256

def salt_pw(password):
    return pbkdf2_sha256.encrypt(password, rounds=5000, salt_size=16)

def check_pw(password, pw_hash):
    return pbkdf2_sha256.verify(password, pw_hash)
