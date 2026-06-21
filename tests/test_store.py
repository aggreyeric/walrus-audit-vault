"""Tests for the blob-id extraction helper (no network).

`get_blob_id` must parse every response shape the Walrus publisher can return.
"""

from walrus_audit_vault.store import get_blob_id


def test_get_blob_id_newly_created():
    resp = {
        "newlyCreated": {
            "blobObject": {"id": "0xobj", "blobId": "BLOB_NEW", "size": 52},
            "cost": 514395,
        }
    }
    assert get_blob_id(resp) == "BLOB_NEW"


def test_get_blob_id_already_certified():
    resp = {"alreadyCertified": {"blobId": "BLOB_CERT", "event": {"seq": 1}}}
    assert get_blob_id(resp) == "BLOB_CERT"


def test_get_blob_id_newly_encoded():
    resp = {"newlyEncoded": {"blobId": "BLOB_ENC"}}
    assert get_blob_id(resp) == "BLOB_ENC"


def test_get_blob_id_unknown_shape_returns_none():
    assert get_blob_id({}) is None
    assert get_blob_id({"someOtherShape": {}}) is None


def test_get_blob_id_newly_encoded_missing_id():
    # Defensive: a newlyEncoded without an explicit blobId should not crash.
    assert get_blob_id({"newlyEncoded": {}}) is None
