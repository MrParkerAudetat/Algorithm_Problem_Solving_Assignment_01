# AL01: Ticket Rules and Follow-Up

Name: Mark
Partners: Garrett, Parker
Shared repository: https://github.com/MrParkerAudetat/Algorithm_Problem_Solving_Assignment_01.git
My contribution:

## Run

Keep main.py, ticket_data.py, and test_assignment.py together.
Include any support modules you imported, such as console_style.py.

```
python main.py
python test_assignment.py
```

## Work Notes and Reflections

Append brief bullets as you work. Record meaningful observations, debugging
challenges, changes, and learnings; no fixed number of entries or essay is required.

Include the boundary repair, one changed/unchanged result under the revised
policy, and whether the final-policy tests stayed the same after your refactor.
Do not repeat the assignment or copy test output into another table.

- **Boolean age check:** In Python, `isinstance(True, int)` is `True`. Because ticket T10 has `age_days: True`, I had to check for `bool` first so it gets flagged as invalid instead of treated as day 1.
- **Boundary repair:** The starter had `age_days > 2`, which dropped tickets at exactly 2 days old. The rule says "at least 2 days", so I changed it to `age_days >= 2`. Now T02 and T09 correctly show up.
- **Policy change (v1 to v2):**
  - *Unchanged:* T02 stayed in the list because it's open, 2 days old, and high priority.
  - *Changed:* T03 dropped out under v2 because even though it's 3 days old, it's normal priority and software (not high priority or access).
- **Refactoring:** Moved the age and rule checks into helper functions and hooked up `console_style.py` for readable colored tables and red warnings for invalid records. All tests passed before and after with zero changes to results.

## Assistance

- Used supplied `ticket_data.py` without changes.
- Used Copilot to help draft the validation checks, set up the test cases, and build the ANSI color helpers in `console_style.py`.
- Checked everything by hand against the assignment rules and verified all tests pass.

## Instructor Comments

[Reserved for instructor feedback.]
