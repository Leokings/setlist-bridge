from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Judge one proposed live-set transition"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"transition": "FLOW", "note": "The arc continues."})}})
    return {"validators": [item.to_dict() for item in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validators_review_directed_transition():
    owner = create_accounts(1)[0]
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "setlist_bridge.py")
    deployed = factory.deploy_contract_tx(args=["A three-act evening moving from quiet reflection to communal celebration.", "Adjacent tracks continue the declared arc or create an intentional breathing space."], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    contract = factory.build_contract(extract_contract_address(deployed), account=owner)
    for args in [("A", "A sparse opening with patient space and an unresolved final phrase for the next track."), ("B", "A warm middle track that picks up the pulse and resolves the opening musical idea in its description."), ("C", "A bright communal closer with a stronger declared pulse and clear sense of arrival.")]:
        ok(contract.submit_track(args=list(args)).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.lock_tracks(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.review_transition(args=["A", "B"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.get_set(args=[]).call()["review_count"] == 1

