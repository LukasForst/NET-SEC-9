Your task is to find out the password for your account at a web server using a weak authentication method. The server uses many iterations of a hash function and salt to strengthen the authentication, but it seems not enough care was taken during its implementation. :(

Your username is `auXXXXXX` and the host is `https://ec2-18-218-24-114.us-east-2.compute.amazonaws.com:8080/`. Use the `POST` method!
A testing account has been setup with username `au597939` and password `Password` for you to verify.
Each password has a finite number of letters and numbers, salts have 16 random bytes. The password hashing function is:

```python
def hash(password, salt):
    h = []
    for i in range(len(password)):
        m = hashlib.sha256()
        for j in range(100000):
                m.update(password[i])
        m.update(salt)
        h = h + [m.hexdigest()[0:4]]
    return "".join(h)
```
And the password comparison function is:
```python
def compare(password, hash, salt):
    h = []
    for i in range(0,len(password)):
        m = hashlib.sha256()
        for j in range(100000):
                m.update(password[i])
        m.update(salt)
        if (hash[4*i] != m.hexdigest()[0]) or (hash[4*i+1] != m.hexdigest()[1]) or (hash[4*i+2] != m.hexdigest()[2]) or (hash[4*i+3] != m.hexdigest()[3]):
                return False
    if (len(password) != len(hash)//4):
        return False
    return True
```

Hint: If the latency to the server is perhaps too high from your local network, how can you get a little closer? :)

----
```bash
curl --insecure -X POST 'https://ec2-18-218-24-114.us-east-2.compute.amazonaws.com:8080/' --data 'username=au597939&password=Password'
```