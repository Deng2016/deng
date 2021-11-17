import base64
import hashlib
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def to_encode(connect: str) -> str:
    return str(
        base64.b64encode(bytes(connect, encoding="utf8")),
        encoding="utf8",
    )


def to_decode(connect: str) -> str:
    return str(base64.b64decode(bytes(connect, encoding="utf8")), encoding="utf8")


class CommanderCrypto(object):
    """V5.5.5之后的加密算法"""

    secret = "awsomerobot" + str(datetime.datetime.now().year)

    @classmethod
    def encrypt(cls, data, xsrf_token="") -> str:
        """加密"""
        if xsrf_token:
            key = cls.sha256(xsrf_token)
        else:
            key = cls.secret
        if len(key) >= 32:
            key = key[:32]
        else:
            key = cls.__add_to_32(key)
        cipher1 = AES.new(key=key.encode("utf-8"), mode=AES.MODE_ECB)
        ct = cipher1.encrypt(pad(data.encode("utf-8"), 16))
        encrypt_data = base64.b64encode(ct)
        return encrypt_data.decode("utf-8")

    @classmethod
    def decrypt(cls, data, xsrf_token="") -> str:
        """解密"""
        if xsrf_token:
            key = cls.sha256(xsrf_token)
        else:
            key = cls.secret
        if len(key) >= 32:
            key = key[:32]
        else:
            key = cls.__add_to_32(key)
        ct = base64.b64decode(data)
        cipher2 = AES.new(key=key.encode("utf-8"), mode=AES.MODE_ECB)
        pt = unpad(cipher2.decrypt(ct), 16)
        return pt.decode("utf-8")

    @classmethod
    def __add_to_32(cls, text):
        while len(text) % 32 != 0:
            text += "\0"
        return text

    @classmethod
    def sha256(cls, data):
        """sha256加密"""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
