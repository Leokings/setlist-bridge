from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "setlist_bridge.py"
SDK = "v0.2.16"
PROMPT = "Judge one proposed live-set transition"


def built(vm, deploy, owner):
    vm.sender = owner
    contract = deploy(str(CONTRACT), "A three-act evening moving from quiet reflection to communal celebration.", "Adjacent tracks must either continue the energy arc or create an intentional breathing space.", sdk_version=SDK)
    contract.submit_track("A", "A sparse opening built around soft pulse, patient space, and an unresolved final phrase.")
    contract.submit_track("B", "A mid-set piece that picks up the pulse, adds warm harmony, and resolves the opening phrase.")
    contract.submit_track("C", "A bright communal closer with a stronger beat and a clear sense of arrival for the audience.")
    contract.lock_tracks()
    return contract


def test_reviewed_edges_build_complete_set(direct_vm, direct_deploy, direct_alice):
    contract = built(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "FLOW", "note": "The energy arc continues."}))
    contract.review_transition("A", "B")
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    contract.review_transition("B", "C")
    contract.begin_order("A")
    contract.append_track("B")
    contract.append_track("C")
    contract.finalize_set()
    assert contract.get_set()["phase"] == "FINAL"


def test_track_ids_cannot_alias_a_directed_edge(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    contract = direct_deploy(str(CONTRACT), "A carefully paced community show with three distinct sections.", "Every adjacency must support the declared arc without pretending to inspect audio.", sdk_version=SDK)
    with direct_vm.expect_revert("invalid_track_id"):
        contract.submit_track("A>B", "A track name containing the edge separator could collide with another directed transition.")
    with direct_vm.expect_revert("invalid_track_id"):
        contract.submit_track("A\nB", "A track name containing a newline must not be usable as a transition key.")


def test_unreviewed_or_clashing_transition_cannot_be_appended(direct_vm, direct_deploy, direct_alice):
    contract = built(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "CLASH", "note": "The arc breaks here."}))
    contract.review_transition("A", "B")
    contract.begin_order("A")
    with direct_vm.expect_revert("approved_transition_required"):
        contract.append_track("B")
    with direct_vm.expect_revert("approved_transition_required"):
        contract.append_track("C")
    with direct_vm.expect_revert("every_track_must_be_placed"):
        contract.finalize_set()


def test_curator_gate(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    contract = direct_deploy(str(CONTRACT), "A carefully paced community show with three distinct sections.", "Every adjacency must support the declared arc without pretending to inspect audio.", sdk_version=SDK)
    contract.submit_track("A", "A declared opening track with a calm texture and a long final tone for transition planning.")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_curator"):
        contract.lock_tracks()


def test_model_enum_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = built(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "PERFECT", "note": "Unsupported label."}))
    with direct_vm.expect_revert("invalid_transition_value"):
        contract.review_transition("A", "B")

