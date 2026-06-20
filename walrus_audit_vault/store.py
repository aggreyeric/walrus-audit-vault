"""
Walrus client — store and retrieve blobs on Walrus decentralized storage.

Testnet endpoints verified working (Jun 2026).
"""

from __future__ import annotations

import httpx

# Verified-live testnet publisher/aggregator endpoints (Jun 2026)
PUBLISHER_URL = "https://publisher.walrus-testnet.walrus.space/v1/blobs"
AGGREGATOR_URL = "https://aggregator.walrus-testnet.walrus.space/v1/blobs"


def store_blob(data: bytes, deletable: bool = True, timeout: float = 30.0) -> dict:
    """Store a blob on Walrus. Returns the full response dict.

    Args:
        data: Raw bytes to store.
        deletable: If True, blob can be deleted later (testnet convenience).
        timeout: HTTP timeout in seconds.

    Returns:
        Dict with blob_id, size, storage metadata. Example::

            {
              "newlyCreated": {
                "blobObject": {"id": "0x...", "blobId": "...", "size": 52, ...},
                "cost": 514395
              }
            }
    """
    resp = httpx.put(
        PUBLISHER_URL,
        content=data,
        headers={"Content-Type": "application/octet-stream"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def store_blob_json(obj: dict, timeout: float = 30.0) -> dict:
    """Convenience: serialize a dict to JSON bytes and store."""
    import json
    return store_blob(json.dumps(obj, sort_keys=True).encode("utf-8"), timeout=timeout)


def retrieve_blob(blob_id: str, timeout: float = 30.0) -> bytes:
    """Retrieve a blob's raw bytes from Walrus by blob ID.

    Args:
        blob_id: The Walrus blob ID (base64-encoded string).
        timeout: HTTP timeout.

    Returns:
        Raw bytes of the stored blob.
    """
    resp = httpx.get(f"{AGGREGATOR_URL}/{blob_id}", timeout=timeout)
    resp.raise_for_status()
    return resp.content


def retrieve_blob_json(blob_id: str, timeout: float = 30.0) -> dict:
    """Retrieve a blob and parse it as JSON."""
    import json
    return json.loads(retrieve_blob(blob_id, timeout=timeout).decode("utf-8"))


def get_blob_id(response: dict) -> str | None:
    """Extract the blob ID from a store_blob response."""
    # Handle both "newlyCreated" and "alreadyCertified" response shapes
    if "newlyCreated" in response:
        return response["newlyCreated"]["blobObject"]["blobId"]
    if "alreadyCertified" in response:
        return response["alreadyCertified"]["blobId"]
    if "newlyEncoded" in response:
        return response["newlyEncoded"].get("blobId")
    return None
