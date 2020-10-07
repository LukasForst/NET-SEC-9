import hashlib
import string
import sys
import time

from main import test_remotely


def my_hash(password, salt):
    h = []
    for i in range(len(password)):
        m = hashlib.sha256()
        for j in range(100000):
            m.update(password[i].encode())
        m.update(salt)
        h = h + [m.hexdigest()[0:4]]
    return "".join(h)


def compare(password, pass_hash, salt):
    h = []
    for i in range(0, len(password)):
        m = hashlib.sha256()
        for j in range(100000):
            m.update(password[i].encode())
        m.update(salt)
        if (pass_hash[4 * i] != m.hexdigest()[0]) or (pass_hash[4 * i + 1] != m.hexdigest()[1]) or (
                pass_hash[4 * i + 2] != m.hexdigest()[2]) or (pass_hash[4 * i + 3] != m.hexdigest()[3]):
            return False
    if (len(password) != len(pass_hash) // 4):
        return False
    return True


def remote_compare(pwd: str) -> bool:
    status, _ = test_remotely(pwd)
    return status == 200


if __name__ == "__main__":
    s = "toto_je_salt".encode()
    p = "prdel"

    h = my_hash(p, s)
    alpha = string.ascii_letters

    found = "Pa"
    while True:
        record, candidate = -1, "-"
        for x in alpha:
            cur = f"{found}{x}"
            print(cur, end='\r')

            if remote_compare(f"{cur}"):
                print(f"Done -> {cur}")
                sys.exit(0)

            start = time.time()
            compare(f"{cur}$", h, s)
            elapsed = time.time() - start

            # print(f"{x} -> {elapsed}")
            if elapsed > record:
                record = elapsed
                candidate = x
        # print("-------")
        found = f"{found}{candidate}"
