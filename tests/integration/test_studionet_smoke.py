import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


def emit(address, deployed, intelligent, observed):
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))


@pytest.mark.integration
def test_studionet_transition_review(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "setlist_bridge.py")
    deployed = ok(factory.deploy_contract_tx(args=["A three-act evening moving from quiet reflection to a warm communal close.", "A valid adjacency must continue the declared energy arc or provide a deliberate breathing space."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    tracks = [("A", "A sparse opening built around patient space, a soft pulse, and an unresolved final phrase."), ("B", "A middle piece that keeps the pulse, adds warm harmony, and resolves the opening phrase."), ("C", "A bright communal closer with a stronger beat and a clear sense of arrival for the audience.")]
    for args in tracks:
        ok(contract.submit_track(args=list(args)).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.lock_tracks(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(contract.review_transition(args=["A", "B"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    transition = contract.get_transition(args=["A", "B"]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert transition["transition"] in ("FLOW", "BREATH", "CLASH")
    emit(address, deployed, intelligent, transition["transition"])

