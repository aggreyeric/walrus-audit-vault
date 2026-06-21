# Submission Form Fields — Walrus Audit Vault

## Hackathon
Sui Overflow 2026 (Devpost) — $500K prize pool

## Project Name
Walrus Audit Vault — Tamper-Evident Decentralized Audit Logs

## Tagline
Every agent action gets an immutable, verifiable audit trail — stored on Walrus, anchored on Sui.

## Description (3-4 paragraphs)
Walrus Audit Vault is a verifiable logging system that creates tamper-evident audit trails for AI agent actions. When an agent takes a step — reading a file, making an API call, executing a trade — Walrus Audit Vault records the action as a cryptographic hash, stores the full log on Walrus (decentralized storage), and anchors a commitment hash on Sui for on-chain verification.

The architecture separates storage (Walrus) from verification (Sui): logs live on Walrus for cheap, scalable storage, while Sui holds only the lightweight hash commitments that prove the logs haven't been tampered with. This means anyone can verify the integrity of an agent's full action history by comparing the Walrus-stored log against the Sui-anchored hash.

The Python SDK provides a simple API for agents to use: `vault.record(action)` writes a log entry, `vault.verify(entry_id)` confirms integrity, and `vault.audit(agent_id)` retrieves the full history. The system is designed for any multi-agent system where accountability matters — DeFi trading agents, legal compliance agents, or enterprise workflow agents.

## Tech Stack
- Python 3.11+ with httpx and pydantic
- Walrus decentralized storage (Sui ecosystem)
- Sui blockchain for hash commitment anchoring
- pytest for testing

## Known Gaps
- Move smart contract for on-chain verification is not yet implemented
- Currently uses Python-only verification (no on-chain proof)

## GitHub URL
https://github.com/aggreyeric/walrus-audit-vault

## Built For
- Sui Overflow 2026 — Agentic Web track
- Verifiable agent accountability
