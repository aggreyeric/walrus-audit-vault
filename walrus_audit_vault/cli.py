"""
CLI for Walrus Audit Vault — store, verify, and list audit logs.

Usage:
  python -m walrus_audit_vault.cli store --actor PayBridge --action transfer --decision ALLOWED
  python -m walrus_audit_vault.cli verify --blob-id <blob_id>
  python -m walrus_audit_vault.cli demo
"""

from __future__ import annotations

import argparse
import json
import sys

from .audit import make_record
from .store import store_blob_json, retrieve_blob_json, get_blob_id


def cmd_store(args):
    """Store an audit record on Walrus."""
    record = make_record(
        actor=args.actor,
        action=args.action,
        decision=args.decision,
        target=args.target or "",
        amount=args.amount or 0,
        policies=(args.policies.split(",") if args.policies else []),
        blocking_policy=args.blocking_policy,
        sui_tx_id=args.tx_id,
        metadata=json.loads(args.metadata) if args.metadata else {},
    )

    content_hash = record.content_hash()
    print(f"  Content hash: {content_hash}")
    print(f"  Storing on Walrus testnet...")

    resp = store_blob_json(record.__dict__ if hasattr(record, "__dict__") else record.to_bytes.__self__.__dict__)
    blob_id = get_blob_id(resp)

    if not blob_id:
        print("  ❌ Failed to store blob")
        print(json.dumps(resp, indent=2))
        sys.exit(1)

    print(f"  ✅ Stored!")
    print(f"  Blob ID:     {blob_id}")
    print(f"  Size:        {resp.get('newlyCreated', {}).get('blobObject', {}).get('size', '?')} bytes")
    print(f"  Storage ID:  {resp.get('newlyCreated', {}).get('blobObject', {}).get('id', '?')}")
    print()
    print("  Verify with:")
    print(f"    python -m walrus_audit_vault.cli verify --blob-id {blob_id}")


def cmd_verify(args):
    """Verify an audit record by retrieving it from Walrus."""
    print(f"  Fetching blob {args.blob_id} from Walrus...")
    try:
        record = retrieve_blob_json(args.blob_id)
    except Exception as e:
        print(f"  ❌ Failed to retrieve: {e}")
        sys.exit(1)

    print(f"  ✅ Retrieved audit record:")
    print(json.dumps(record, indent=2))


def cmd_demo(args):
    """Run a live demo: store a sample PayBridge audit log and verify it."""
    print("=" * 60)
    print("  WALRUS AUDIT VAULT — LIVE DEMO")
    print("=" * 60)
    print()
    print("  Scenario: PayBridge agent attempts a 50 SUI transfer")
    print("  that gets BLOCKED by SpendLimitPolicy.")
    print()

    record = make_record(
        actor="PayBridge-Agent-0x6dca",
        action="transfer_sui",
        decision="BLOCKED",
        actor_address="0x6dcac660db0c07f345f00fe0fec59c9e3ec2768dbec98032a76da42b26b000d0",
        target="0xrecipient1234",
        amount=50_000_000_000,  # 50 SUI in mist
        policies=["SpendLimitPolicy", "WhitelistPolicy", "RateLimitPolicy", "TimeWindowPolicy"],
        blocking_policy="SpendLimitPolicy",
        metadata={"reason": "50 SBAR exceeds max_per_tx of 10 SUI"},
    )

    print(f"  Record: {record.actor} → {record.target}")
    print(f"  Decision: {record.decision} (blocked by {record.blocking_policy})")
    print()

    content_hash = record.content_hash()
    print(f"  Content hash: {content_hash}")

    print(f"  Storing on Walrus testnet...")
    from .store import store_blob
    try:
        data = store_blob(record.to_bytes())
    except Exception as e:
        print(f"  ❌ Storage failed: {e}")
        return
    blob_id = get_blob_id(data)

    if blob_id:
        print(f"  ✅ Stored on Walrus!")
        print(f"  Blob ID: {blob_id}")
        print()
        print("  Now verifying by retrieving the blob...")
        retrieved = retrieve_blob_json(blob_id)
        print(f"  ✅ Retrieved & verified intact: {retrieved['actor']} → {retrieved['decision']}")
        print()
        print("  ✔ Audit trail is tamper-evident and decentralized.")
    else:
        print(f"  ❌ Storage failed: {json.dumps(data)[:200]}")

    print()
    print("=" * 60)
    print("  DEMO COMPLETE — full round-trip on Walrus testnet")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Walrus Audit Vault CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # store
    p_store = sub.add_parser("store", help="Store an audit record")
    p_store.add_argument("--actor", required=True)
    p_store.add_argument("--action", required=True)
    p_store.add_argument("--decision", required=True, choices=["ALLOWED", "BLOCKED", "REVERTED"])
    p_store.add_argument("--target", default="")
    p_store.add_argument("--amount", type=int, default=0)
    p_store.add_argument("--policies", default="")
    p_store.add_argument("--blocking-policy", dest="blocking_policy", default=None)
    p_store.add_argument("--tx-id", dest="tx_id", default=None)
    p_store.add_argument("--metadata", default=None)
    p_store.set_defaults(func=cmd_store)

    # verify
    p_verify = sub.add_parser("verify", help="Verify an audit record by blob ID")
    p_verify.add_argument("--blob-id", dest="blob_id", required=True)
    p_verify.set_defaults(func=cmd_verify)

    # demo
    p_demo = sub.add_parser("demo", help="Run a live demo on Walrus testnet")
    p_demo.set_defaults(func=cmd_demo)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
