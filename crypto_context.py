from Crypto.PublicKey import RSA
from crypto_utils import *

class CryptoContext:
    def __init__(self, algo, shared_key=None):
        self.algo = algo
        self.key = shared_key

        if algo == "RSA":
            self.priv = RSA.generate(2048)
            self.pub = self.priv.publickey()

    def encrypt(self, data):
        if self.algo == "AES":
            return aes_encrypt(data, self.key)
        if self.algo == "DES":
            return des_encrypt(data, self.key)
        if self.algo == "3DES":
            return des3_encrypt(data, self.key)
        if self.algo == "RSA":
            return rsa_encrypt(data, self.pub)

    def decrypt(self, payload):
        if self.algo == "AES":
            return aes_decrypt(payload, self.key)
        if self.algo == "DES":
            return des_decrypt(payload, self.key)
        if self.algo == "3DES":
            return des3_decrypt(payload, self.key)
        if self.algo == "RSA":
            return rsa_decrypt(payload, self.priv)
