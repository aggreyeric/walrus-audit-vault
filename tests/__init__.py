"""Pure (no-network) tests for the audit record model.

These cover the cryptographic core that makes the vault tamper-evident:
canonical serialization, deterministic SHA-256 hashing, and builder defaults.
No network access required.
"""
