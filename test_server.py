from crypto import generate_salt, compare

salt = generate_salt()
real_pwd = 'Password'
pwd_hash = hash(real_pwd)


def test_local_compare(pwd: str) -> bool:
    try:
        return compare(pwd, pwd_hash, salt)
    except Exception:
        return False
