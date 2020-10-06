from crypto import generate_salt, compare

salt = generate_salt()
real_pwd = 'Password'
pwd_hash = hash(real_pwd)


def verify_password(pwd: str) -> bool:
    return compare(pwd, pwd_hash, salt)
