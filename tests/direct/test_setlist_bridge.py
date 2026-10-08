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


def test_only_curator_can_choose_and_finish_order(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = built(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "FLOW", "note": "This pair fits."}))
    direct_vm.sender = direct_bob
    contract.review_transition("A", "B")
    with direct_vm.expect_revert("only_curator"):
        contract.begin_order("A")
    direct_vm.sender = direct_alice
    contract.begin_order("A")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_curator"):
        contract.append_track("B")
    with direct_vm.expect_revert("only_curator"):
        contract.finalize_set()
    direct_vm.sender = direct_alice
    contract.append_track("B")
    with direct_vm.expect_revert("every_track_must_be_placed"):
        contract.finalize_set()


def test_duplicate_and_post_lock_writes_fail_closed(direct_vm, direct_deploy, direct_alice):
    contract = built(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert("track_window_closed"):
        contract.submit_track("D", "A late arrival should not change the locked transition-review input set.")
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "FLOW", "note": "This pair fits."}))
    contract.review_transition("A", "B")
    with direct_vm.expect_revert("transition_already_reviewed"):
        contract.review_transition("A", "B")
    contract.begin_order("A")
    with direct_vm.expect_revert("transition_review_closed"):
        contract.review_transition("B", "C")
    contract.append_track("B")
    with direct_vm.expect_revert("track_already_placed"):
        contract.append_track("B")


def test_validator_rejects_different_transition_label(direct_vm, direct_deploy, direct_alice):
    contract = built(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "FLOW", "note": "The leader's explanation."}))
    contract.review_transition("A", "B")
    leader = direct_vm._captured_validators[-1][0]
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "CLASH", "note": "The verifier disagrees."}))
    assert direct_vm.run_validator(leader_result=leader) is False


def test_transition_note_is_explicitly_non_consensus(direct_vm, direct_deploy, direct_alice):
    contract = built(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "FLOW", "note": "Leader explanation."}))
    contract.review_transition("A", "B")
    leader = direct_vm._captured_validators[-1][0]
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"transition": "FLOW", "note": "Different verifier explanation."}))
    assert direct_vm.run_validator(leader_result=leader) is True
    assert contract.get_transition("A", "B")["note_scope"] == "leader_only_not_consensus_checked"


def test_curator_can_clear_spam_and_restore_submission_capacity(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    contract = direct_deploy(str(CONTRACT), "A carefully paced community show with three distinct sections.", "Every adjacency must support the declared arc without pretending to inspect audio.", sdk_version=SDK)
    direct_vm.sender = direct_bob
    for index in range(8):
        contract.submit_track(f"SPAM{index}", "An untrusted public brief that uses a slot before curator review and should remain removable.")
    with direct_vm.expect_revert("track_limit"):
        contract.submit_track("SPAM8", "Another public brief should not be accepted while the bounded list is full.")
    with direct_vm.expect_revert("only_curator"):
        contract.remove_track("SPAM3")
    direct_vm.sender = direct_alice
    contract.remove_track("SPAM3")
    assert len(contract.track_ids) == 7
    assert "SPAM3" not in list(contract.track_ids)
    direct_vm.sender = direct_bob
    contract.submit_track("SPAM3", "A resubmission with the same ID must be possible after its earlier record is removed.")
    direct_vm.sender = direct_alice
    contract.remove_track("SPAM3")
    direct_vm.sender = direct_bob
    contract.submit_track("A", "A legitimate opening brief that may take the slot the curator cleared from spam.")
    direct_vm.sender = direct_alice
    contract.remove_track("SPAM0")
    contract.remove_track("SPAM7")
    contract.lock_tracks()
    with direct_vm.expect_revert("track_window_closed"):
        contract.remove_track("A")

