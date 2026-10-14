"""Test suite for AL01 Ticket Rules and Follow-Up.

Demonstrates algorithmic correctness, boundary testing, policy comparison,
and validation rules for team review.
"""

import sys
from pathlib import Path

# Add the current directory so imports work smoothly
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    validate_ticket,
    select_open_tickets,
    select_follow_up,
    meets_follow_up_age,
)
from ticket_data import TICKETS


def test_validation_rules():
    """Verify field-level validation and error messages."""
    print("Testing: Validation rules...")

    # Valid ticket
    valid = {"id": "TX1", "status": "open", "category": "software", "age_days": 0, "priority": "low"}
    ticket, err = validate_ticket(valid)
    assert ticket is not None, "Valid ticket failed validation"
    assert err is None, "Valid ticket returned an error message"

    # Boolean age defect check (Python bool inherits from int)
    bool_age = {"id": "TX2", "status": "open", "category": "software", "age_days": True, "priority": "low"}
    ticket, err = validate_ticket(bool_age)
    assert ticket is None, "Boolean age must be rejected"
    assert "not boolean" in err, f"Expected boolean notice in error: {err}"

    # Negative age
    neg_age = {"id": "TX3", "status": "open", "category": "software", "age_days": -1, "priority": "low"}
    ticket, err = validate_ticket(neg_age)
    assert ticket is None, "Negative age must be rejected"

    # Missing field
    missing_cat = {"id": "TX4", "status": "open", "age_days": 2, "priority": "low"}
    ticket, err = validate_ticket(missing_cat)
    assert ticket is None, "Missing category must be rejected"

    # Whitespace-only id
    blank_id = {"id": "   ", "status": "open", "category": "access", "age_days": 1, "priority": "low"}
    ticket, err = validate_ticket(blank_id)
    assert ticket is None, "Whitespace ID must be rejected"

    # Invalid status
    bad_status = {"id": "TX5", "status": "pending", "category": "access", "age_days": 1, "priority": "low"}
    ticket, err = validate_ticket(bad_status)
    assert ticket is None, "Invalid status must be rejected"


def test_boundary_age_repair():
    """Test the Tuesday isolated boundary bug repair for 'at least 2 days old'.
    
    Starter bug: age_days > 2
    Repaired: age_days >= 2
    """
    print("Testing: Age boundary check (meets_follow_up_age)...")
    assert not meets_follow_up_age(0), "Age 0 should not qualify"
    assert not meets_follow_up_age(1), "Age 1 should not qualify (< 2)"
    assert meets_follow_up_age(2), "Age 2 must qualify (repaired boundary: >= 2)"
    assert meets_follow_up_age(3), "Age 3 must qualify (> 2)"


def test_select_open_tickets():
    """Verify open ticket selection preserves order, filters closed/invalid tickets."""
    print("Testing: select_open_tickets...")
    selected, issues = select_open_tickets(TICKETS)

    # 12 tickets in dataset: 3 invalid, 2 closed (T05, T08), 7 open
    assert len(selected) == 7, f"Expected 7 open tickets, got {len(selected)}"
    assert len(issues) == 3, f"Expected 3 issues, got {len(issues)}"

    selected_ids = [t["id"] for t in selected]
    expected_ids = ["T01", "T02", "T03", "T04", "T06", "T07", "T09"]
    assert selected_ids == expected_ids, f"Expected order {expected_ids}, got {selected_ids}"

    # Ensure none of the selected tickets are closed
    for t in selected:
        assert t["status"] == "open"


def test_policy_v1_vs_v2_comparison():
    """Demonstrate policy transition from Tuesday (v1) to Thursday (v2).
    
    Checklist requirements:
    - High priority qualifying under v2
    - Access category qualifying under v2
    - Changed result between v1 and v2
    - Preserved result between v1 and v2
    """
    print("Testing: Policy v1 vs v2 comparison...")
    v1_tickets, _ = select_follow_up(TICKETS, policy="v1")
    v2_tickets, _ = select_follow_up(TICKETS, policy="v2")

    v1_ids = [t["id"] for t in v1_tickets]
    v2_ids = [t["id"] for t in v2_tickets]

    # Under v1: open and age >= 2 -> T02, T03, T04, T07, T09 (5 tickets)
    assert v1_ids == ["T02", "T03", "T04", "T07", "T09"]

    # Under v2: open, age >= 2, and (high priority OR access category)
    # -> T02 (high), T04 (access), T09 (high) (3 tickets)
    assert v2_ids == ["T02", "T04", "T09"]

    # Evidence of a PRESERVED result:
    # T02: open, age 2, high priority -> in both v1 and v2
    assert "T02" in v1_ids and "T02" in v2_ids

    # Evidence of a CHANGED result:
    # T03: open, age 3, but normal priority + software category -> in v1, dropped in v2
    # T07: open, age 4, but low priority + network category -> in v1, dropped in v2
    assert "T03" in v1_ids and "T03" not in v2_ids
    assert "T07" in v1_ids and "T07" not in v2_ids


def test_empty_and_no_match_inputs():
    """Verify behavior on empty input lists and records that produce no matches."""
    print("Testing: Empty inputs and non-matching tickets...")
    empty_selected, empty_issues = select_open_tickets([])
    assert empty_selected == []
    assert empty_issues == []

    # Valid closed tickets only
    closed_batch = [
        {"id": "C01", "status": "closed", "category": "software", "age_days": 5, "priority": "high"},
        {"id": "C02", "status": "closed", "category": "access", "age_days": 10, "priority": "high"},
    ]
    open_sel, open_iss = select_open_tickets(closed_batch)
    assert open_sel == [], "Should have no open tickets"
    assert open_iss == [], "All records were valid"

    follow_sel, follow_iss = select_follow_up(closed_batch, policy="v2")
    assert follow_sel == [], "Closed tickets cannot qualify for follow-up"
    assert follow_iss == []


def run_all_tests():
    """Run full test suite and report summary."""
    print("=" * 60)
    print("RUNNING AL01 TEST SUITE")
    print("=" * 60)
    test_validation_rules()
    test_boundary_age_repair()
    test_select_open_tickets()
    test_policy_v1_vs_v2_comparison()
    test_empty_and_no_match_inputs()
    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! (5 test groups verified)")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
