import socket, threading, time, json, requests, tkinter as tk
from tkinter import ttk, filedialog
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES3

from crypto_context import CryptoContext
from signature_utils import generate_keys, sign_message, verify_signature
from metrics import measure
from metrics_logger import log_metric

# --- CONFIGURATION ---
AUTH_URL = "http://127.0.0.1:8000"
CHUNK_SIZE = 8192

def fetch_blockchain_key(wallet):
    """
    Queries Auth Server and uses a robust reconstruction method to fix PEM 
    boundary and formatting errors common with blockchain storage.
    """
    try:
        r = requests.get(f"{AUTH_URL}/peerkey/{wallet}", timeout=5)
        r.raise_for_status()
        raw_key = r.json().get("key", "").strip()
        
        if not raw_key: 
            print(f"Error: No key found for {wallet} on Sepolia.")
            return None

        # --- ROBUST PEM RECONSTRUCTION ---
        # 1. Remove existing headers, footers, and ALL whitespace/newlines
        clean_body = raw_key.replace("-----BEGIN PUBLIC KEY-----", "")
        clean_body = clean_body.replace("-----END PUBLIC KEY-----", "")
        # Strip all invisible characters to get pure base64 content
        clean_body = "".join(clean_body.split()) 
        
        # 2. Reconstruct with standard headers and clean newline structure
        # PyCryptodome is strict about the \n before the END boundary.
        formatted_key = f"-----BEGIN PUBLIC KEY-----\n{clean_body}\n-----END PUBLIC KEY-----"
        
        return RSA.import_key(formatted_key.encode())
    except Exception as e:
        print(f"Key Import Error for {wallet}: {e}")
        return None

# --- NETWORK CORE ---
def recvall(sock, size):
    data = b""
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part: return None
        data += part
    return data

def send_packet(conn, header, binary=b""):
    try:
        h_bytes = json.dumps(header).encode()
        conn.sendall(len(h_bytes).to_bytes(4, "big"))
        conn.sendall(h_bytes)
        if binary: conn.sendall(binary)
    except: pass

def recv_packet(conn):
    len_bytes = recvall(conn, 4)
    if not len_bytes: return None
    h_len = int.from_bytes(len_bytes, "big")
    h_data = recvall(conn, h_len)
    return json.loads(h_data.decode())

# --- BLOCKCHAIN HANDSHAKE ---
def run_handshake(is_init, my_port, p_port, wallet):
    global conn, crypto, SESSION_ALGO, NODE_ID
    NODE_ID = "A" if is_init else "B"
    SESSION_ALGO = "AES"

    try:
        if is_init:
            log_ui(f"Connecting to Peer on port {p_port}...")
            time.sleep(2) 
            conn = socket.socket()
            conn.connect(("127.0.0.1", p_port))
            
            shared_key = get_random_bytes(16)
            priv_sig, _ = generate_keys()
            msg = SESSION_ALGO.encode() + b"||" + shared_key
            sig = sign_message(priv_sig, msg)
            
            # Send Handshake: [ALGO+KEY] || [SIG] || [WALLET_ADDR]
            conn.sendall(msg + b"||" + sig + b"||" + wallet.encode())
            log_ui("Handshake sent. Waiting for peer verification...")
        else:
            log_ui(f"Listening on port {my_port}...")
            s = socket.socket()
            s.bind(("127.0.0.1", my_port))
            s.listen(1)
            conn, _ = s.accept()
            
            # Receive Handshake Data
            data = conn.recv(4096)
            parts = data.split(b"||")
            if len(parts) < 4:
                raise Exception("Invalid handshake format received")
            
            algo_b, s_key, sig, p_wallet_b = parts[0], parts[1], parts[2], parts[3]
            
            # VERIFY VIA BLOCKCHAIN: Fetch key from Sepolia
            peer_pub = fetch_blockchain_key(p_wallet_b.decode())
            if not peer_pub:
                log_ui("❌ Security Failure: Peer key format invalid or not found on Sepolia.")
                conn.close()
                return

            verify_signature(peer_pub, algo_b + b"||" + s_key, sig)
            shared_key = s_key
            log_ui(f"✅ Verified {p_wallet_b.decode()} via Blockchain.")

        crypto = CryptoContext(SESSION_ALGO, shared_key)
        status_label.config(text="SECURE CONNECTION ESTABLISHED", fg="#10b981")
        threading.Thread(target=receive_loop, daemon=True).start()
    except Exception as e:
        log_ui(f"❌ Handshake Error: {e}")
        status_label.config(text="CONNECTION FAILED", fg="#ef4444")

# --- RECEIVE LOOP ---
def receive_loop():
    while True:
        try:
            h = recv_packet(conn)
            if not h: break
            if h["type"] == "TEXT":
                enc = recvall(conn, h["size"])
                msg, _ = measure(crypto.decrypt, SESSION_ALGO, "decrypt", enc, NODE_ID)
                log_ui(f"[Peer]: {msg.decode()}")
        except: break

# --- UI ACTIONS ---
def log_ui(msg):
    chat.config(state='normal')
    chat.insert(tk.END, msg + "\n")
    chat.config(state='disabled')
    chat.see(tk.END)

def send_text():
    t = entry.get()
    if not t or not crypto: return
    enc, _ = measure(crypto.encrypt, SESSION_ALGO, "encrypt", t.encode(), NODE_ID)
    send_packet(conn, {"type": "TEXT", "size": len(enc)}, enc)
    log_ui(f"[You]: {t}")
    entry.delete(0, tk.END)

# --- GUI INIT ---
root = tk.Tk()
root.title("P2P Blockchain Chat")
root.geometry("600x500")

status_label = tk.Label(root, text="Handshake Pending...", font=("Arial", 10, "bold"))
status_label.pack(pady=5)

chat = tk.Text(root, state='disabled', height=20, width=65, bg="#ffffff", font=("Consolas", 10))
chat.pack(padx=10, pady=5)

bottom = tk.Frame(root)
bottom.pack(fill="x", padx=10, pady=10)

entry = tk.Entry(bottom, width=50)
entry.pack(side="left", padx=5)
tk.Button(bottom, text="Send", command=send_text, bg="#2563eb", fg="white").pack(side="left")

# --- STARTUP ---
m_port = int(input("Your Port: "))
p_port = int(input("Peer Port: "))
init = input("Are you Initiator? (y/n): ").lower() == 'y'
wal = input("Your Wallet: ").strip()

threading.Thread(target=run_handshake, args=(init, m_port, p_port, wal), daemon=True).start()
root.mainloop()