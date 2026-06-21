"""Tests for the audit record data model + hashing (no network)."""

import hashlib
import json
import time

from walrus_audit_vault.audit import AuditRecord, make_record


def _sample_record(**overrides):
    base = dict(
        actor="PayBridge-Agent-0x6dca",
        action="transfer_sui",
        decision="ALLOWED",
        timestamp=1_700_000_000,
        actor_address="0x6dca",
        target="0xrecipient",
        amount=5_000_000_000,
        policies_evaluated=["SpendLimit", "Whitelist"],
        blocking_policy=None,
        sui_tx_id="abc123digest",
        metadata={"reason": "ok"},
    )
    base.update(overrides)
    return AuditRecord(**base)


# ── make_record ──────────────────────────────────────────────

def test_make_record_sets_defaults():
    before = int(time.time())
    rec = make_record("agent", "act", "ALLOWED")
    after = int(time.time())
    assert rec.timestamp == int(rec.timestamp)
    assert before <= rec.timestamp <= after
    assert rec.policies_evaluated == []
    assert rec.metadata == {}
    assert rec.amount == 0
    assert rec.blocking_policy is None
    assert rec.sui_tx_id is None


def test_make_record_passes_fields():
    rec = make_record(
        "a", "b", "BLOCKED",
        target="0xt",
        amount=42,
        policies=["P1", "P2"],
        blocking_policy="P1",
        sui_tx_id="tx1",
        metadata={"k": "v"},
        timestamp=99,
    )
    assert rec.target == "0xt"
    assert rec.amount == 42
    assert rec.policies_evaluated == ["P1", "P2"]
    assert rec.blocking_policy == "P1"
    assert rec.sui_tx_id == "tx1"
    assert rec.metadata == {"k": "v"}
    assert rec.timestamp == 99


def test_make_record_accepts_empty_collections():
    rec = make_record("a", "b", "ALLOWED", policies=None, metadata=None)
    assert rec.policies_evaluated == []
    assert rec.metadata == {}


# ── canonical serialization ──────────────────────────────────

def test_to_bytes_is_canonical():
    """Serialized form must use sorted keys and no whitespace."""
    rec = _sample_record()
    raw = rec.to_bytes()
    decoded = json.loads(raw)
    assert list(decoded.keys()) == sorted(decoded.keys())
    # No insignificant whitespace: no spaces after separators
    assert b", " not in raw
    assert b": " not in raw


def test_to_bytes_is_utf8():
    rec = _sample_record()
    assert rec.to_bytes() == rec.to_bytes().decode("utf-8").encode("utf-8")


# ── content_hash ─────────────────────────────────────────────

def test_content_hash_is_deterministic():
    rec = _sample_record()
    assert rec.content_hash() == rec.content_hash()


def test_content_hash_matches_manual_sha256():
    rec = _sample_record()
    expected = hashlib.sha256(rec.to_bytes()).hexdigest()
    assert rec.content_hash() == expected
    assert len(rec.content_hash()) == 64


def test_identical_records_share_hash():
    a = _sample_record()
    b = _sample_record()
    assert a.content_hash() == b.content_hash()


def test_different_records_differ_in_hash():
    base = _sample_record()
    mutations = [
        _sample_record(actor="other"),
        _sample_record(decision="BLOCKED"),
        _sample_record(amount=6_000_000_000),
        _sample_record(policies_evaluated=["OnlyOne"]),
        _sample_record(metadata={"reason": "changed"}),
        _sample_record(sui_tx_id="differenttx"),
    ]
    for m in mutations:
        assert m.content_hash() != base.content_hash(), \
            "Mutation did not change the hash"


def test_key_order_irrelevant_for_hash():
    """Canonical serialization means the hash is stable regardless of how the
    record's dict keys were originally ordered."""
    rec = _sample_record()

    # A record built from a deliberately reversed key order must hash the same.
    fields = {
        "sui_tx_id": "abc123digest",
        "metadata": {"reason": "ok"},
        "policies_evaluated": ["SpendLimit", "Whitelist"],
        "blocking_policy": None,
        "amount": 5_000_000_000,
        "target": "0xrecipient",
        "actor_address": "0x6dca",
        "timestamp": 1_700_000_000,
        "decision": "ALLOWED",
        "action": "transfer_sui",
        "actor": "PayBridge-Agent-0x6dca",
    }
    reordered = AuditRecord(**fields)

    # to_bytes sorts keys, so both serialize identically and hash identically.
    assert rec.to_bytes() == reordered.to_bytes()
    assert rec.content_hash() == reordered.content_hash()


def test_timestamp_affects_hash():
    a = _sample_record(timestamp=1)
    b = _sample_record(timestamp=2)
    assert a.content_hash() != b.content_hash()


# ── to_json ──────────────────────────────────────────────────

def test_to_json_roundtrips():
    rec = _sample_record()
    parsed = json.loads(rec.to_json())
    assert parsed["actor"] == rec.actor
    assert parsed["action"] == rec.action
    assert parsed["decision"] == rec.decision
    assert parsed["amount"] == rec.amount
