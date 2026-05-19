from web3 import Web3
from Crypto.PublicKey import RSA
import json

# --- Connection ---
RPC_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_KEY"
CONTRACT_ADDR = "0xf5Db938f2A17775a10f295E968Cfa0e3893E7fDE"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- ABI (Simplified for registration) ---
ABI = json.loads('[{"inputs":[{"internalType":"string","name":"key","type":"string"}],"name":"register","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

def register_wallet(private_key):
    # 1. Setup Account
    account = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDR), abi=ABI)
    
    # 2. Generate RSA Key locally
    rsa_key = RSA.generate(2048)
    pub_key_pem = rsa_key.publickey().export_key().decode()
    
    # 3. Build & Sign Transaction
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.register(pub_key_pem).build_transaction({
        'chainId': 11155111,
        'gas': 250000,
        'maxFeePerGas': w3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"Registering {account.address}... Transaction: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # IMPORTANT: Save your private RSA key locally to 'my_private_rsa.pem'
    with open(f"{account.address}_private.pem", "wb") as f:
        f.write(rsa_key.export_key())
    print(f"✅ Registered! Private RSA key saved as {account.address}_private.pem")

# --- EXECUTION ---
# Run this twice, once for each wallet's private key
# register_wallet("PRIVATE_KEY_A")
# register_wallet("PRIVATE_KEY_B")