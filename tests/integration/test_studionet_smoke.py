import base64
import hashlib
import json
from pathlib import Path
import time
from urllib import error, request

import pytest
from gltest import get_contract_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address
from genlayer_py.exceptions import GenLayerError
from genlayer_py.provider.provider import GenLayerProvider


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


def _rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    last_error = None
    for attempt in range(8):
        try:
            call = request.Request("https://studio.genlayer.com/api", data=body, headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Codex-GenLayer-Audit/1.0",
            })
            with request.urlopen(call, timeout=30) as response:
                payload = json.load(response)
            assert "error" not in payload, payload
            return payload["result"]
        except (error.HTTPError, error.URLError, TimeoutError, AssertionError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < 7:
                time.sleep(6)
    raise AssertionError(f"StudioNet RPC verification failed: {last_error}")


def deployed_source_hash(address, source):
    deployed = base64.b64decode(_rpc("gen_getContractCode", [address]), validate=True)
    # GitHub stores this Python source with LF; a Windows checkout may use CRLF.
    local = source.read_bytes().replace(b"\r\n", b"\n")
    assert deployed == local, "deployed source differs from this repository"
    return hashlib.sha256(local).hexdigest()


@pytest.fixture(autouse=True)
def retry_transient_read_rpc(monkeypatch):
    original = GenLayerProvider.make_request

    def resilient(self, method, params):
        for attempt in range(5):
            try:
                return original(self, method, params)
            except GenLayerError as exc:
                if not str(method).startswith("eth_get") or "invalid JSON" not in str(exc) or attempt == 4:
                    raise
                time.sleep(3)

    monkeypatch.setattr(GenLayerProvider, "make_request", resilient)


@pytest.mark.integration
def test_studionet_transition_review():
    curator, outsider = create_accounts(2)
    source = Path(__file__).resolve().parents[2] / "contracts" / "setlist_bridge.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=["A three-act evening moving from quiet reflection to a warm communal close.", "A valid adjacency must continue the declared energy arc or provide a deliberate breathing space."], account=curator, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    print("STUDIONET_DEPLOY=" + json.dumps({"address": address, "tx": deployed["hash"]}), flush=True)
    contract = factory.build_contract(address, account=curator)
    outsider_contract = factory.build_contract(address, account=outsider)
    tracks = [("A", "A sparse opening built around patient space, a soft pulse, and an unresolved final phrase."), ("B", "A middle piece that keeps the pulse, adds warm harmony, and resolves the opening phrase."), ("C", "A bright communal closer with a stronger beat and a clear sense of arrival for the audience.")]
    setup = []
    setup.append(ok(outsider_contract.submit_track(args=["X", "A public untrusted track brief that the curator should be able to remove before lock."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    print("STUDIONET_SETUP_TX=" + setup[-1]["hash"], flush=True)
    for args in tracks:
        setup.append(ok(contract.submit_track(args=list(args)).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
        print("STUDIONET_SETUP_TX=" + setup[-1]["hash"], flush=True)
    setup.append(ok(contract.remove_track(args=["X"]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    print("STUDIONET_REMOVE_TX=" + setup[-1]["hash"], flush=True)
    setup.append(ok(contract.lock_tracks(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    print("STUDIONET_SETUP_TX=" + setup[-1]["hash"], flush=True)
    intelligent = []
    labels = []
    for left, right in [("A", "B"), ("B", "C")]:
        intelligent.append(ok(contract.review_transition(args=[left, right]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
        print("STUDIONET_INTELLIGENT_TX=" + intelligent[-1]["hash"], flush=True)
        transition = contract.get_transition(args=[left, right]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
        labels.append(transition["transition"])
        assert transition["transition"] in ("FLOW", "BREATH"), transition
    completion = [
        ok(contract.begin_order(args=["A"]).transact(wait_transaction_status=TransactionStatus.FINALIZED)),
        ok(contract.append_track(args=["B"]).transact(wait_transaction_status=TransactionStatus.FINALIZED)),
        ok(contract.append_track(args=["C"]).transact(wait_transaction_status=TransactionStatus.FINALIZED)),
        ok(contract.finalize_set(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED)),
    ]
    final_state = contract.get_set(args=[]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert final_state == {"phase": "FINAL", "track_count": 3, "review_count": 2, "ordered_tracks": ["A", "B", "C"]}
    print("STUDIONET_FLOW=" + json.dumps({
        "address": address,
        "deploy_tx": deployed["hash"],
        "setup_txs": [item["hash"] for item in setup],
        "intelligent_txs": [item["hash"] for item in intelligent],
        "completion_txs": [item["hash"] for item in completion],
        "transition_labels": labels,
        "final_state": final_state,
    }, sort_keys=True))
    source_hash = deployed_source_hash(address, source)
    assert _rpc("gen_getContractSchema", [address]) == json.loads((source.parents[1] / "abi.json").read_text(encoding="utf-8"))
    print("STUDIONET_RECORD=" + json.dumps({
        "address": address,
        "deploy_tx": deployed["hash"],
        "setup_txs": [item["hash"] for item in setup],
        "intelligent_txs": [item["hash"] for item in intelligent],
        "completion_txs": [item["hash"] for item in completion],
        "transition_labels": labels,
        "final_state": final_state,
        "source_sha256": source_hash,
    }, sort_keys=True))

