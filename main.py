"""Ticket validation, selection rules, and console presentation.

Assignment: AL01 - Ticket Rules and Follow-Up
Overview for Team:
- Validation checks raw records against field specifications without modifying inputs.
- select_open_tickets filters valid tickets where status == 'open'.
- select_follow_up applies the follow-up policy (Tuesday v1 vs Thursday v2).
- Boundary fix note: age threshold is '>= 2', repairing the initial bug '> 2'.
- Presentation separates display formatting cleanly from algorithmic filtering.
"""

from ticket_data import TICKETS
import console_style as style

# Specification constants for allowed categorical values
VALID_STATUSES = {"open", "closed"}
VALID_CATEGORIES = {"software", "network", "access"}
VALID_PRIORITIES = {"low", "normal", "high"}


def validate_ticket(ticket):
    """Validate a single ticket record against schema rules.
    
    Returns:
        (ticket, None) if record is valid.
        (None, error_message) describing all failing fields if invalid.
    """
    if not isinstance(ticket, dict):
        return None, "Record is not a valid dictionary."

    problems = []
    ticket_id = ticket.get("id")
    id_label = f"Ticket '{ticket_id}'" if ticket_id else "Ticket with missing ID"

    # Rule 1: id must be non-empty text, not whitespace-only
    if "id" not in ticket or not isinstance(ticket["id"], str) or not ticket["id"].strip():
        problems.append("id must be non-empty text")

    # Rule 2: status must be either 'open' or 'closed'
    if "status" not in ticket or ticket["status"] not in VALID_STATUSES:
        problems.append(f"status must be one of {sorted(VALID_STATUSES)}")

    # Rule 3: category must be 'software', 'network', or 'access'
    if "category" not in ticket or ticket["category"] not in VALID_CATEGORIES:
        problems.append(f"category must be one of {sorted(VALID_CATEGORIES)}")

    # Rule 4: age_days must be an integer >= 0, explicitly excluding Python bools
    # (In Python, bool subclasses int, so isinstance(True, int) is True; hence isinstance(age, bool) check first)
    if "age_days" not in ticket:
        problems.append("age_days is required")
    else:
        age = ticket["age_days"]
        if isinstance(age, bool) or not isinstance(age, int) or age < 0:
            problems.append("age_days must be an integer >= 0 (not boolean)")

    # Rule 5: priority must be 'low', 'normal', or 'high'
    if "priority" not in ticket or ticket["priority"] not in VALID_PRIORITIES:
        problems.append(f"priority must be one of {sorted(VALID_PRIORITIES)}")

    if problems:
        return None, f"{id_label} has invalid fields: {', '.join(problems)}"
    return ticket, None


def select_open_tickets(records):
    """Filter records to find all valid tickets with 'open' status.
    
    Preserves input order and leaves input records unchanged.
    
    Returns:
        (selected, issues): List of valid matching tickets, and list of validation error strings.
    """
    selected = []
    issues = []
    for record in records:
        valid_ticket, error_msg = validate_ticket(record)
        if error_msg:
            issues.append(error_msg)
        elif valid_ticket["status"] == "open":
            selected.append(valid_ticket)
    return selected, issues


def meets_follow_up_age(age_days):
    """Check if age meets minimum follow-up threshold.
    
    Boundary Bug Repair Note (Tuesday):
    The policy states tickets must be 'at least 2 days old'.
    The starter defect was 'age_days > 2', which excluded tickets at exactly 2 days.
    Repaired to 'age_days >= 2'.
    """
    return age_days >= 2


def matches_follow_up_v1(ticket):
    """Policy v1 (Tuesday): Valid, open, and at least 2 days old."""
    return ticket["status"] == "open" and meets_follow_up_age(ticket["age_days"])


def matches_follow_up_v2(ticket):
    """Policy v2 (Thursday): Valid, open, at least 2 days old, AND (high priority OR access category).
    
    Refactoring Note:
    - Reuses meets_follow_up_age for age threshold consistency.
    - Preserves mandatory open + age criteria; alternatives cannot bypass them.
    """
    is_open = ticket["status"] == "open"
    has_age = meets_follow_up_age(ticket["age_days"])
    has_qualifying_reason = (ticket["priority"] == "high") or (ticket["category"] == "access")
    return is_open and has_age and has_qualifying_reason


def select_follow_up(records, policy="v2"):
    """Filter records for tickets requiring follow-up under specified policy ('v1' or 'v2').
    
    Returns:
        (selected, issues): List of matching tickets in input order, and list of invalid record issues.
    """
    selected = []
    issues = []
    predicate = matches_follow_up_v2 if policy == "v2" else matches_follow_up_v1

    for record in records:
        valid_ticket, error_msg = validate_ticket(record)
        if error_msg:
            issues.append(error_msg)
        elif predicate(valid_ticket):
            selected.append(valid_ticket)
    return selected, issues


def format_ticket_row(ticket):
    """Format a single ticket into a readable aligned table row with column-based color coding."""
    pipe = style.style_pipe()
    tid = style.style_id(f"{ticket['id']:<5}")
    tstatus = style.style_status(f"{ticket['status']:<6}")
    tpriority = style.style_priority(ticket['priority'])
    tcategory = style.style_category(ticket['category'])
    tage = style.style_age(ticket['age_days'])
    return f"  {tid} {pipe} {tstatus} {pipe} {tpriority} {pipe} {tcategory} {pipe} {tage}"


def display_results(title, policy_desc, tickets, issues):
    """Display policy details, formatted matching tickets, counts, and validation issues."""
    divider = style.style_header("=" * 72)
    print(divider)
    print(style.style_header(f"REPORT: {title}"))
    print(f"Policy: {style.style_policy(policy_desc)}")
    print(divider)

    print(style.style_sub_header(f"\nMatching Tickets ({len(tickets)} total):"))
    if tickets:
        print(style.style_table_header())
        for t in tickets:
            print(format_ticket_row(t))
    else:
        print("  (No tickets matched this policy)")

    print(style.style_sub_header(f"\nRecords Needing Review / Invalid ({len(issues)} total):"))
    if issues:
        for issue in issues:
            print(f"  {style.style_badge()} {style.style_review_record(issue)}")
    else:
        print("  (None - all records were valid)")
    print()


def run_application():
    """Run full demonstration showing open tickets, policy v1, and final policy v2."""
    banner = style.style_header("#" * 70)
    print("\n" + banner)
    print(style.style_header("# HELP DESK TICKET AUDIT APPLICATION (AL01)"))
    print(banner + "\n")

    # 1. Open Tickets View
    open_tickets, open_issues = select_open_tickets(TICKETS)
    display_results(
        title="Open Tickets",
        policy_desc="Valid records where status == 'open'",
        tickets=open_tickets,
        issues=open_issues,
    )

    # 2. Follow-Up Tickets (Policy v1 - Tuesday)
    follow_up_v1, _ = select_follow_up(TICKETS, policy="v1")
    display_results(
        title="Follow-Up Queue (Policy v1 - Tuesday)",
        policy_desc="Valid, open, and at least 2 days old (age >= 2)",
        tickets=follow_up_v1,
        issues=open_issues,
    )

    # 3. Follow-Up Tickets (Policy v2 - Thursday Final)
    follow_up_v2, follow_up_issues = select_follow_up(TICKETS, policy="v2")
    display_results(
        title="Follow-Up Queue (Policy v2 - Thursday Final)",
        policy_desc="Valid, open, age >= 2, and either priority == 'high' OR category == 'access'",
        tickets=follow_up_v2,
        issues=follow_up_issues,
    )


if __name__ == "__main__":
    run_application()



