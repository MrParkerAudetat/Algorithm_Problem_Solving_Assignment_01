# AL01: Ticket Rules and Follow-Up

Name: Parker
Partners: Mark, Garrett
Shared repository: https://github.com/MrParkerAudetat/Algorithm_Problem_Solving_Assignment_01.git
My planned contribution: Add `select_open_tickets` and the age and follow-up
policy functions in `main.py`, then add the boundary-age and open ticket
selection tests to `test_assignment.py`.

## Run

To run the program and its tests, we keep `main.py`, `ticket_data.py`, and
`test_assignment.py` together, along with the support module `console_style.py`.

```powershell
python main.py
python test_assignment.py
```

## My Work and Reflections

I picked up after Garrett's validation work. `select_open_tickets` runs each
record through `validate_ticket` and keeps only valid tickets whose status is
`open`. Invalid records are collected separately so they can be reported instead
of silently dropped.

I then wrote the policy functions. `meets_follow_up_age` holds the age check,
`matches_follow_up_v1` and `matches_follow_up_v2` hold the two policy rules, and
`select_follow_up` applies whichever policy is requested (Tuesday v1 or Thursday
v2, defaulting to v2). Keeping each rule in its own small function made the
policies easy to compare and test.

I also fixed a boundary condition in the starter code. It used `age_days > 2`,
which excluded tickets that were exactly two days old, even though the rule says
"at least 2 days." I changed the comparison to `age_days >= 2`, so T02 and T09
are included.

When I applied the revised policy, T02 stayed in the results because it is open,
two days old, and high priority. T03 no longer qualified: although it is three
days old, it is a normal-priority software ticket, rather than a high-priority or
access ticket.

In `test_assignment.py` I wrote `test_boundary_age_repair`, which checks that a
ticket exactly two days old is included, and `test_select_open_tickets`, which
checks that only valid open tickets are selected.

## Thursday Update

For the Thursday change to policy v2 (valid, open, at least 2 days old, and
either high priority or the access category), I wrote `matches_follow_up_v2`.
My one small refactor was moving the age check into the shared helper
`meets_follow_up_age`. Both `matches_follow_up_v1` and `matches_follow_up_v2`
call it, so the `>= 2` boundary from Tuesday's repair now lives in one place.
The behavior did not change. I reran the tests after the refactor and they all
pass. Under v2, T02, T04, and T09 are selected.

## Assistance

I used the supplied `ticket_data.py` without making changes. I used Copilot to
help draft the selection and policy functions and to set up the test cases. I
checked my work against the assignment rules and verified that all tests pass.

## Planned Shift Handoffs

We plan to work in 20- to 30-minute shifts, moving from the top of `main.py`
and `test_assignment.py` toward the bottom. At each handoff, the next person
reviews what the previous person wrote and we agree on the next step.

1. **Garrett starts:** He sets up the imports and validation constants at the
   top of `main.py`, writes `validate_ticket`, and begins `test_assignment.py`
   with its imports and `test_validation_rules`.
2. **I continue:** I add `select_open_tickets` and the age and follow-up policy
   functions in `main.py`, then add the boundary-age and open ticket selection
   tests.
3. **Mark finishes:** He copies the provided ticket records into
   `ticket_data.py`, creates `console_style.py` with AI assistance, and finishes
   the lower part of `main.py` with the report-formatting and application-running
   functions. In `test_assignment.py`, he adds the policy comparison and
   empty-input tests and finishes the test runner.

At the end, we run the program and tests together and review the results as a
team.

## Instructor Comments




