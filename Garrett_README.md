# AL01: Ticket Rules and Follow-Up

Name: Garrett
Partners: Mark, Parker
Shared repository: https://github.com/MrParkerAudetat/Algorithm_Problem_Solving_Assignment_01.git
My planned contribution: Set up the imports and validation constants at the top
of `main.py`; implement `validate_ticket`; and begin `test_assignment.py` with
its imports and `test_validation_rules`.

## Run

To run the program and its tests, we keep `main.py`, `ticket_data.py`, and
`test_assignment.py` together, along with the support module `console_style.py`.

```powershell
python main.py
python test_assignment.py
```

## My Work and Reflections

I started the project by defining the validation constants at the top of
`main.py`: `VALID_STATUSES`, `VALID_CATEGORIES`, and `VALID_PRIORITIES`. Keeping
the allowed values in sets made the rules easy to read and easy to change.

`validate_ticket` checks one record against the five field rules (id, status,
category, age_days, and priority). It does not modify the input. It collects
every failing field into one message instead of stopping at the first problem,
so a bad record reports everything that is wrong with it. It returns
`(ticket, None)` for a valid record and `(None, error_message)` for an invalid
one. A record that is not a dictionary is rejected right away.

The trickiest rule was `age_days`. Python treats `bool` as a subclass of `int`,
so `isinstance(True, int)` returns `True`. Ticket T10 has `age_days: True`, so I
check for a boolean before checking for an integer. This lets the program flag
T10 as invalid instead of interpreting its age as one day.

In `test_assignment.py` I wrote the imports and `test_validation_rules`, which
covers valid records, missing fields, wrong values, whitespace-only ids, negative
ages, and the boolean age case.

## Thursday Update

After the team finished the v2 policy, I hardened `validate_ticket`. A list or
dictionary in `status`, `category`, or `priority` used to raise a `TypeError`
during the set lookup, because those values cannot be hashed. The function now
checks that each of those fields is text before checking the allowed values, so
a malformed record is reported as invalid instead of crashing. I added a test
for this to `test_validation_rules` and reran all the tests; they pass.

## Assistance

I used the supplied `ticket_data.py` without making changes. I used Copilot to
help draft the validation checks and set up the first test cases. I checked my
work against the assignment rules and verified that the validation tests pass.

## Planned Shift Handoffs

We plan to work in 20- to 30-minute shifts, moving from the top of `main.py`
and `test_assignment.py` toward the bottom. At each handoff, the next person
reviews what the previous person wrote and we agree on the next step.

1. **I start:** I set up the imports and validation constants at the top of
   `main.py`, write `validate_ticket`, and begin `test_assignment.py` with its
   imports and `test_validation_rules`.
2. **Parker continues:** He adds `select_open_tickets` and the age and follow-up
   policy functions in `main.py`, then adds the boundary-age and open ticket
   selection tests.
3. **Mark finishes:** He copies the provided ticket records into
   `ticket_data.py`, creates `console_style.py` with AI assistance, and finishes
   the lower part of `main.py` with the report-formatting and application-running
   functions. In `test_assignment.py`, he adds the policy comparison and
   empty-input tests and finishes the test runner.

At the end, we run the program and tests together and review the results as a
team.

## Instructor Comments




