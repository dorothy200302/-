import hashlib

def encrypt_password(password: str) -> str:
    """
    使用MD5加密密码
    """
    return hashlib.md5(password.encode()).hexdigest() 