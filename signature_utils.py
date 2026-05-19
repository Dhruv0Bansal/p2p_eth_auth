from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys():
    key = RSA.generate(2048)
    return key, key.publickey()

def sign_message(private_key, message: bytes):  # here msg is the data we have to protect
    h = SHA256.new(message)                     # convert the msg into the  hash
    return pkcs1_15.new(private_key).sign(h)    # sign the hash with private key

def verify_signature(public_key, message: bytes, signature: bytes):
    h = SHA256.new(message)
    pkcs1_15.new(public_key).verify(h, signature)
