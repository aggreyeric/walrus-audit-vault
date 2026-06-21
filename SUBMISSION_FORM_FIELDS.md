# Sui Overflow 2026 — Submission Form

> Walrus Track

---

## Project Name

**Walrus Audit Vault — Verifiable Decentralized Audit Logs**

---

## One-Liner

> Every agent action hashed, stored on Walrus, indexed on Sui — tamper-evident by design.

---

## Description

### What it does

Walrus Audit Vault is a decentralized, tamper-evident audit log system for autonomous AI agents. Every time an agent acts — a payment, a policy decision, a tool call — the full context (who requested it, which policies were evaluated, the resulting decision and reasoning, the on-chain transaction receipt, and a timestamp) is bundled into a structured record, SHA-256 hashed, cryptographically signed, and stored immutably as a blob on Walrus. The returned blob ID, together with the content hash, is anchored to a Sui on-chain registry object so that any third party can later fetch the blob, recompute its hash, and prove the audit log has not been tampered with — without ever needing to store the full log on-chain.

### Why Walrus + Sui

Audit trails are large and append-only; they are the exact opposite of what an L1 should store. Sui's on-chain storage is optimized for small, frequently-accessed objects and is expensive for bulk data. Walrus fills the gap: it provides cheap, verifiable, decentralized blob storage with content-addressed retrieval. Sui then plays the role it is good at — a cheap, fast, programmable verification anchor that maps a content hash to a Walrus blob ID. This split gives us the best of both worlds: full audit fidelity off-chain on Walrus, and a cryptographically verifiable, queryable index on Sui.

### How the architecture works

The pipeline flows in five stages. First, an agent action (for example a PayBridge SUI transfer) emits an audit event. Second, a Python client builds an `AuditRecord` with pydantic-typed fields and computes a SHA-256 `content_hash` over the canonical JSON, then signs it. Third, the record is PUT to the Walrus publisher endpoint, returning a decentralized, replicated `blob_id`. Fourth, the `blob_id` and `content_hash` are written to a Sui `Registry` Move object so the pair becomes an on-chain verification anchor. Fifth, any verifier — a regulator, another agent, or an end user — retrieves the blob from a Walrus aggregator, recomputes the SHA-256, and compares it to the hash stored on Sui. A match proves the log is intact; a mismatch proves tampering. The whole flow is exercised end-to-end from a single `python cli.py` command.

---

## Tech Stack

- **Python** — agent integration, record builder, CLI
- **Walrus** — decentralized blob storage for the audit records
- **Sui** — on-chain content-hash → blob-id verification anchor
- **pydantic** — typed, validated audit record data model
- **httpx** — HTTP client for the Walrus publisher/aggregator API

---

## Known Gaps / Limitations

- **Move contract not yet implemented.** The on-chain Sui registry (`registry.move`) that maps `content_hash → blob_id` is specified in the README and architecture but has not been written or deployed. For the hackathon demo, the Walrus storage + verification round-trip is fully functional; the Sui anchoring step is simulated/ mocked. Writing and deploying the Move module is the next milestone.

---

## GitHub Repository

https://github.com/aggreyeric/walrus-audit-vault

---

## Demo

Run the CLI to store and then verify an audit entry:

```bash
# 1. Store an audit entry on Walrus
python cli.py store \
  --actor "0xpaybridge_agent" \
  --action "transfer_sui" \
  --decision "ALLOWED" \
  --amount 5000000000

# → prints the content hash and the returned Walrus blob_id

# 2. Verify the same entry end-to-end
python cli.py verify --blob-id <blob_id_from_step_1>

# → fetches the blob from a Walrus aggregator,
#   recomputes the SHA-256, and reports ✅ Verified / ❌ Tampered
```

The store/verify round-trip demonstrates the full tamper-evidence guarantee: the content hash computed before storage matches the hash recomputed after retrieval, proving the log was not altered.
