from flask import Flask, jsonify
from web3 import Web3
import json

# Use the standard Sepolia RPC endpoint
RPC = "https://sepolia.infura.io/v3/d9c75086e13349a09b5166b5615111ed"
CONTRACT_ADDR = "0x0f097F712375c287009Bd584BeD5770421963Cad"

# Ensure the ABI matches your KeyRegistry.sol contract
ABI = json.loads('[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"get","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider(RPC))

# Verify connection before starting
if not w3.is_connected():
    print("Error: Could not connect to Sepolia. Check your RPC URL.")

contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDR), abi=ABI)

# FIX: Use dynamic route <addr> to handle any peer wallet
@app.get("/peerkey/<addr>")
def peerkey(addr):
    try:
        # Checksum the address to prevent Web3 errors
        checksum_addr = w3.to_checksum_address(addr)
        
        # Fetch verified RSA key from Sepolia
        k = contract.functions.get(checksum_addr).call()
        
        if not k:
            return jsonify({"error": "No key found on-chain for this wallet"}), 404
            
        return jsonify({"key": k})
    except Exception as e:
        print(f"Blockchain Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"Monitoring Sepolia Contract: {CONTRACT_ADDR}")
    app.run(port=8000)