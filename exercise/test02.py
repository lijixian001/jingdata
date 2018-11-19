import hashlib

md5 = hashlib.md5(b'123456')
password_md5 = md5.hexdigest()
print(password_md5)