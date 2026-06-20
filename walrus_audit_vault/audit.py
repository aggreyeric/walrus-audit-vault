"""
Audit record model — tamper-evident log entries for agent actions.

Each record captures the full context of an autonomous agent's decision:
who, what, why, and the cryptographic hash that proves it wasn't altered.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class AuditRecord:
    """A single auditable action performed by an autonomous agent."""

    actor: str                      # Agent or user identifier (e.g. "PayBridge-0x6dca")
    action: str                     # What was attempted (e.g. "transfer_sui")
    decision: str                   # "ALLOWED" | "BLOCKED" | "REVERTED"
    timestamp: int                  # Unix epoch seconds
    # ── Context ──
    actor_address: str = ""         # On-chain address of the actor
    target: str = ""                # Target address / object
    amount: int = 0                 # Amount in mist (if applicable)
    policies_evaluated: list = field(default_factory=list)   # e.g. ["SpendLimit", "Whitelist"]
    blocking_policy: Optional[str] = None    # Which policy blocked it (if blocked)
    sui_tx_id: Optional[str] = None          # Sui transaction digest (if executed)
    metadata: dict = field(default_factory=dict)  # Free-form extra context

    def to_bytes(self) -> bytes:
        """Canonical serialization for hashing — sorted keys, no whitespace."""
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode("utf-8")

    def content_hash(self) -> str:
        """SHA-256 hash of the canonical record. Used as the verification anchor."""
        return hashlib.sha256(self.to_bytes()).hexdigest()

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


def make_record(
    actor: str,
    action: str,
    decision: str,
    *,
    actor_address: str = "",
    target: str = "",
    amount: int = 0,
    policies: list | None = None,
    blocking_policy: str | None = None,
    sui_tx_id: str | None = None,
    metadata: dict | None = None,
    timestamp: int | None = None,
) -> AuditRecord:
    """Build an AuditRecord with sensible defaults."""
    return AuditRecord(
        actor=actor,
        action=action,
        decision=decision,
        timestamp=timestamp or int(time.time()),
        actor_address=actor_address,
        target=target,
        amount=amount,
        policies_evaluated=policies or [],
        blocking_policy=blocking_policy,
        sui_tx_id=sui_tx_id,
        metadata=metadata or {},
    )
