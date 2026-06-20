# 🦭 Walrus Audit Vault — Verifiable Decentralized Audit Logs

**Built for [Sui Overflow 2026 — Walrus Track](https://overflow.sui.io)**

A decentralized, tamper-evident audit log system. Every transaction, policy decision, and agent action is hashed, signed, and stored immutably on **Walrus** (decentralized blob storage), with a content-addressed index anchored on **Sui**.

> Why Walrus? Audit logs grow large. Sui's on-chain storage is expensive and meant for small objects. Walrus gives us **cheap, verifiable, decentralized large-blob storage** — perfect for immutable audit trails, agent transcripts, and policy decision logs.

## 🎯 What It Does

When an AI agent (like PayBridge) makes a payment, the full context gets logged:
1. **Who** requested it, **what** policies were evaluated
2. The **decision** (allow/block) and **reasoning**
3. **Transaction receipt** from Sui
4. All bundled into a JSON document, **SHA-256 hashed**, and **stored on Walrus**

The blob ID is returned and anchored to a Sui on-chain registry object, so anyone can **verify** the audit log was not tampered with — without storing the full log on-chain.

## 🏗️ Architecture

```
Agent action (e.g. PayBridge payment)
        │
        ▼
┌─ Build audit record ──────────────────┐
│  { actor, action, policies, decision, │
│    sui_tx_id, timestamp, signature }  │
└───────────────────────────────────────┘
        │
        ▼
┌─ SHA-256 hash + sign ─────────────────┐
│  content_hash = sha256(record)        │
│  signature = sign(content_hash)       │
└───────────────────────────────────────┘
        │
        ▼
┌─ Store on Walrus ─────────────────────┐
│  blob_id = PUT publisher/blob          │
│  → decentralized, replicated storage   │
└───────────────────────────────────────┘
        │
        ▼
┌─ Anchor on Sui ───────────────────────┐
│  SuiRegistry { blob_id, content_hash }│
│  → on-chain verification anchor        │
└───────────────────────────────────────┘
        │
        ▼
   ✅ Anyone can verify:
   fetch(blob_id) → sha256 → compare to on-chain hash
```

## 🚀 Quick Start

```bash
# Python 3.11+
pip install httpx pydantic

# Set your Sui address (for anchoring)
export SUI_ADDRESS=0x6dca...your...address

# Store an audit log
python -m walrus_audit_vault.cli store \
  --actor "0xpaybridge_agent" \
  --action "transfer_sui" \
  --decision "ALLOWED" \
  --amount 5000000000

# Verify an audit log
python -m walrus_audit_vault.cli verify --blob-id <blob_id>

# List recent logs
python -m walrus_audit_vault.cli list
```

## 📦 Modules

### `walrus_audit_vault/store.py`
Core Walrus client — store and retrieve blobs via the publisher/aggregator API.

### `walrus_audit_vault/audit.py`
Audit record data model + SHA-256 hashing + signature.

### `walrus_audit_vault/registry.move`
Sui Move contract — on-chain registry mapping `content_hash → blob_id` for verification.

### `walrus_audit_vault/cli.py`
Command-line interface for storing, verifying, and listing audit logs.

## 🦭 Why Walrus + Sui

| Layer | Tech | Role |
|-------|------|------|
| **Audit data** | Walrus | Large, cheap, decentralized blob storage |
| **Verification anchor** | Sui | On-chain content hash registry |
| **Agent** | Python | Generates + signs audit records |

Walrus handles the **bulk storage**; Sui handles the **verification anchor**. Together they create a tamper-evident audit trail that's cheaper than full on-chain logs but cryptographically verifiable.

## Use Cases
- 🤖 **AI agent action logs** — prove what an autonomous agent did and why
- 💸 **Payment audit trails** — full policy-decision context, not just tx receipts
- 📋 **Compliance records** — immutable logs for regulated DeFi
- 🔍 **Agent transparency** — verifiable "chain of thought" for autonomous systems

## License
MIT
