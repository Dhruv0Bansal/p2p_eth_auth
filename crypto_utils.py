from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad    # make the data length valid for the encryption 
#Block ciphers require fixed-size blocks
# So we add padding before encryption and remove it after decryption.
# AES
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.iv + cipher.encrypt(pad(data, 16))  # IV is random value for the security

def aes_decrypt(payload, key):
    iv, ct = payload[:16], payload[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), 16)

# DES
def des_encrypt(data, key):
    cipher = DES.new(key, DES.MODE_CBC)
    return cipher.iv + cipher.encrypt(pad(data, 8))

def des_decrypt(payload, key):
    iv, ct = payload[:8], payload[8:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), 8)

# 3DES
def des3_encrypt(data, key):
    cipher = DES3.new(key, DES3.MODE_CBC)
    return cipher.iv + cipher.encrypt(pad(data, 8))

def des3_decrypt(payload, key):
    iv, ct = payload[:8], payload[8:]
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), 8)

# RSA
def rsa_encrypt(data, pub):
    return PKCS1_OAEP.new(pub).encrypt(data)

def rsa_decrypt(ct, priv):
    return PKCS1_OAEP.new(priv).decrypt(ct)
