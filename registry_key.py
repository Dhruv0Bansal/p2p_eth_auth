from web3 import Web3
from Crypto.PublicKey import RSA
import json

# Replace with your data
RPC = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
CONTRACT_ADDR = "YOUR_DEPLOYED_CONTRACT_ADDRESS"
PRIV_KEY = "YOUR_WALLET_PRIVATE_KEY"

w3 = Web3(Web3.HTTPProvider(RPC))
ABI = json.loads('[{"inputs":[{"internalType":"string","name":"key","type":"string"}],"name":"register","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

def register():
    account = w3.eth.account.from_key(PRIV_KEY)
    contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDR), abi=ABI)
    
    # Generate RSA Identity
    rsa_key = RSA.generate(2048)
    pub_pem = rsa_key.publickey().export_key().decode()
    
    # Register on Sepolia
    tx = contract.functions.register(pub_pem).build_transaction({
        'chainId': 11155111,
        'gas': 250000,
        'maxFeePerGas': w3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        'nonce': w3.eth.get_transaction_count(account.address),
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIV_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Registered {account.address}. TX: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)

register()