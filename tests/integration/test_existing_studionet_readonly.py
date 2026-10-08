"""Independently recheck the published StudioNet evidence without new writes."""

import json
from pathlib import Path

import pytest
from genlayer_py import create_account
from genlayer_py.chains import studionet
from genlayer_py.client import create_client
from genlayer_py.types import TransactionHashVariant
from gltest.assertions import tx_execution_succeeded

from tests.integration.test_studionet_smoke import _rpc, deployed_source_hash


@pytest.mark.integration
def test_current_deployment_is_final_and_source_matched():
    root = Path(__file__).resolve().parents[2]
    evidence = json.loads((root / "deployments" / "studionet.json").read_text(encoding="utf-8"))
    client = create_client(chain=studionet, account=create_account())
    hashes = [evidence["deploy_tx"], *evidence["setup_txs"], *evidence["intelligent_txs"], *evidence["completion_txs"]]
    for transaction_hash in hashes:
        receipt = client.get_transaction(transaction_hash)
        assert receipt["status_name"] == "FINALIZED", receipt
        assert tx_execution_succeeded(receipt), receipt
    source = root / "contracts" / "setlist_bridge.py"
    assert deployed_source_hash(evidence["contract_address"], source) == evidence["source_sha256_lf"]
    assert _rpc("gen_getContractSchema", [evidence["contract_address"]]) == json.loads((root / "abi.json").read_text(encoding="utf-8"))
    final_state = client.read_contract(
        evidence["contract_address"],
        "get_set",
        args=[],
        transaction_hash_variant=TransactionHashVariant.LATEST_FINAL,
    )
    assert final_state == evidence["final_state"]
