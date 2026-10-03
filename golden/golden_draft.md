# Golden Dataset Draft

Hand-written test cases for the Nimbus Logistics RAG system.
Each case: question, expected answer, source document, and the trap it tests.

Trap types:
- Conflicting source: an outdated document gives a different answer
- Distractor value: a similar number elsewhere could be confused with the right one
- Awkward format: tables or lists that may chunk badly
- Multi-part answer: the full answer has more than one step
- Boundary: the edge of a rule
- Unanswerable: the corpus does not contain the answer

---

## GD-01: Individual health insurance coverage
- **Question:** What is the annual health insurance coverage for an individual employee?
- **Expected:** Up to PKR 800,000 per year
- **Source:** handbook/benefits.md
- **Trap type:** Distractor value, Awkward format
- **Trap detail:** The family coverage figure (PKR 500,000 per year) is a different value in the same table; the fact sits in a table that may chunk badly

## GD-02: Current annual leave
- **Question:** How many annual leave days do employees get?
- **Expected:** 22 working days
- **Source:** handbook/leave-policy.md
- **Trap type:** Conflicting source
- **Trap detail:** handbook/leave-policy-2023-archived.md says 18 working days

## GD-03: Premium economy eligibility
- **Question:** When is an employee allowed to fly premium economy on international travel?
- **Expected:** Flights over 8 hours
- **Source:** handbook/expenses-and-travel.md
- **Trap type:** Boundary
- **Trap detail:** See GD-04 for the negative edge case

## GD-04: Premium economy on a short flight
- **Question:** Can I book premium economy for a 6-hour international flight?
- **Expected:** No (only for flights over 8 hours)
- **Source:** handbook/expenses-and-travel.md
- **Trap type:** Boundary
- **Trap detail:** The model may say yes because premium economy is mentioned in the policy

## GD-05: OS update deadline
- **Question:** Within how many days must a new OS update be installed on a company laptop?
- **Expected:** Within 7 days of release
- **Source:** it/laptop-policy.md
- **Trap type:** Distractor value
- **Trap detail:** it/passwords-and-mfa.md also says "7 days" (password expiry reminder), so a correct-looking answer could come from the wrong document; it/software-requests.md says up to 10 working days for sensitive software review

## GD-06: VPN blocked on a public network
- **Question:** What should I do if a public network blocks the VPN?
- **Expected:** Use a mobile hotspot; if the issue persists, raise an IT ticket
- **Source:** it/vpn-setup.md
- **Trap type:** Multi-part answer
- **Trap detail:** A correct answer must include both steps; the model may give only the first

## GD-07: Parking (unanswerable)
- **Question:** Where can employees park their cars at the Lahore office?
- **Expected:** The system says the documents do not cover this
- **Source:** none
- **Trap type:** Unanswerable
- **Trap detail:** The model invents a parking policy (hallucination)