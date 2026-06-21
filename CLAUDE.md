# CLAUDE.md — Walrus Audit Vault

## Project Overview
Tamper-evident decentralized audit logs for AI agent actions. Stores on Walrus (decentralized blob storage), indexed on Sui.

## Tech Stack
- **Language:** Python 3.11+
- **Dependencies:** httpx, pydantic
- **Storage:** Walrus (decentralized), Sui (index)
- **Tests:** pytest

## Commands
```bash
# Install
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Architecture
- `walrus_audit_vault/` — Core package (audit.py, cli.py, store.py)
- `tests/` — pytest test files
- `pyproject.toml` — Package manifest

## Known Gaps
- Move/Sui smart contract for on-chain indexing is **NOT yet implemented**
- No test suite yet (0 tests)

## Hackathon Target
- Sui Overflow 2026 — Walrus Track — $500K prize pool
