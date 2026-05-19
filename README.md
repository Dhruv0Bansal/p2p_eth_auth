# p2p_eth_auth

> Decentralized peer-to-peer communication with Ethereum-based identity verification, AES-256 encrypted file transfer, and MetaMask wallet login — no central auth server required.

---

## How it works

Traditional P2P apps rely on a central server to verify user identity. This project replaces that with Ethereum smart contracts — your wallet *is* your identity.

The key design decision: **only session keys are stored on-chain, not messages.** This reduces on-chain transactions by ~95%, cutting testnet faucet usage from hundreds of calls down to a single key-exchange per session.

```
User A (MetaMask)                          User B (MetaMask)
      │                                          │
      │── signs identity ──► Ethereum ◄── signs identity ──│
      │                       (key exchange only)           │
      │                                          │
      └──────── AES-256 encrypted P2P channel ──────────────┘
                     (off-chain, direct)
```

---

## Features

- **Blockchain identity** — wallet address acts as unique identity; no username/password
- **MetaMask login** — one-click authentication via browser wallet
- **On-chain key exchange** — session public keys written to a Solidity smart contract
- **AES-256 encryption** — all communication encrypted end-to-end
- **Digital signatures** — messages and files signed to prevent tampering
- **Secure file transfer** — encrypted binary transfer between peers
- **No central server** — auth is fully decentralized

---

## Tech stack

| Layer | Technology |
|---|---|
| Blockchain | Ethereum (Sepolia testnet) |
| Smart contracts | Solidity |
| Web3 integration | Web3.js |
| Wallet | MetaMask |
| Encryption | AES-256, digital signatures |
| IDE / deployment | Remix IDE |

---

## Getting started

### Prerequisites

- [Node.js](https://nodejs.org/) v18+
- [MetaMask](https://metamask.io/) browser extension
- Sepolia testnet ETH (from a [faucet](https://sepoliafaucet.com/))

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/p2p_eth_auth.git
cd p2p_eth_auth
npm install
```

### Run

```bash
npm start
```

Open `http://localhost:3000` in your browser, connect MetaMask, and you're in.

---

## Smart contract

The contract handles one thing: storing and retrieving session public keys per wallet address.

```solidity
// Simplified interface
function registerKey(address user, string memory publicKey) public
function getKey(address user) public view returns (string memory)
```

Only one transaction per session — that's the entire on-chain footprint.

---

## Security model

| What | How |
|---|---|
| Identity | Ethereum wallet address (cryptographically unique) |
| Session key exchange | On-chain via smart contract |
| Message encryption | AES-256 with per-session keys |
| Integrity | Digital signatures on all payloads |
| Auth server | None — removed entirely |

---

