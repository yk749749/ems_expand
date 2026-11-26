import hashlib


def md5(value):
    """把字符串转换为 32 位 MD5 十六进制字符串。"""
    return hashlib.md5(value.encode("utf-8")).hexdigest()
