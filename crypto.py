import hashlib
import random


def hash(password, salt):
    h = []
    for i in range(len(password)):
        m = hashlib.sha256()
        for j in range(100000):
            m.update(password[i].encode())
        m.update(salt)
        h = h + [m.hexdigest()[0:4]]
    return "".join(h)


def compare(password, hash, salt):
    h = []
    for i in range(0, len(password)):
        m = hashlib.sha256()
        for j in range(100000):
            m.update(password[i].encode())
        m.update(salt)
        if (hash[4 * i] != m.hexdigest()[0]) or (hash[4 * i + 1] != m.hexdigest()[1]) or (
                hash[4 * i + 2] != m.hexdigest()[2]) or (hash[4 * i + 3] != m.hexdigest()[3]):
            return False
    if len(password) != len(hash) // 4:
        return False
    return True


def generate_salt() -> bytes:
    return bytes([random.randrange(0, 256) for _ in range(0, 16)])


def test():
    pwd = 'Password'
    salt = generate_salt()
    hsh = hash(pwd, salt)
    print(hsh)
    print(salt)
    print(compare(pwd, hsh, salt))


def test_data():
    hsh = '08af244f2b442b441a964d3bdf764bd0'
    salt = b'\xeb\xb66\x03\x9a]n\xc5\x9c\x9c\xcc\xbc\xb9\x17\x13\xf1'
    print(compare('Password', hsh, salt))


if __name__ == '__main__':
    test_data()
