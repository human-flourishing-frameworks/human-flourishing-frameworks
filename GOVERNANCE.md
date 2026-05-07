# Governance Charter

## Human Flourishing Frameworks Oversight Board

**Mission:** Ensure frameworks remain open, trustworthy, and protective of human flourishing.

**Authority:** Approve how frameworks can/cannot be used. Cannot revoke anyone's right to implement.

---

## Board Structure

### 12-Member Diverse Board

| Seat | Constituency | Purpose |
|------|--------------|---------|
| 1-2 | Civil Society | Protect individual rights (ACLU, EFF, Amnesty International) |
| 3-4 | Security Researchers | Technical integrity (independent, not affiliated with Big Tech) |
| 5-6 | Diverse Technologists | Implementation perspective (different companies, backgrounds) |
| 7-8 | Government Observers | Policy alignment (listen, learn, no voting) |
| 9-10 | Industry (Non-Monopoly) | Market perspective (diverse companies, not just FAANG) |
| 11-12 | Affected Communities | Human impact (workers, patients, monitored populations) |

**Chair:** Rotating annually (term-limited, no consecutive terms)

### Selection Process

**Who appoints each seat?**

- **Civil Society (1-2):** Nominated by EFF + ACLU + Amnesty International + Human Rights Watch
- **Researchers (3-4):** Nominated by IEEE + ACM + academic institutions
- **Technologists (5-6):** Nominated by open-source community (GitHub, Linux Foundation, etc.)
- **Government (7-8):** Self-selected (NSF, NIST, DoD observers only)
- **Industry (9-10):** Nominated by diverse companies (must exclude top 5 tech companies)
- **Communities (11-12):** Nominated by labor unions, patient advocacy, civil rights orgs

**Voting:**
- All 10 voting members (civil society + researchers + technologists + industry + communities)
- Government observers attend but do not vote
- Decisions require 80% consensus (8 of 10 votes)

**Term:** 2 years, staggered (50% new members each year to ensure continuity)

---

## Responsibilities

### What the Board Approves

1. **Ethical Use Guidelines**
   - Frameworks cannot be used for surveillance without consent
   - Frameworks cannot restrict freedom without public debate
   - Frameworks must not enable discrimination
   - Examples: approval for government deployment, corporate use, research

2. **Principles Enforcement**
   - Transparency: all uses publicly disclosed
   - Consent: cannot track individuals without permission
   - Fairness: demographic equity monitored
   - Freedom: hard-deny rules approved only if necessary and public
   - Accountability: violations exposed immediately

3. **Standards Evolution**
   - New versions of frameworks (80% consensus)
   - Bug fixes and security patches (simple majority)
   - Breaking changes (require public comment period + 90% consensus)

4. **Governance Board Composition**
   - Remove board members who violate ethics (80% vote)
   - Approve new procedures (80% consensus)
   - Set annual budget (simple majority)

### What the Board Does NOT Control

- Who can implement frameworks (anyone can, it's open)
- How implementations work (only that they follow the spec)
- Who can use frameworks (anyone can, licenses are permissive)
- What organizations deploy (anyone can deploy)
- Pricing or business models (implementers decide)

---

## Decision-Making Process

### Regular Decisions (Meeting-Based)

1. **Motion:** Any board member proposes action
2. **Discussion:** 2-week public comment period (on GitHub)
3. **Vote:** At monthly board meeting
4. **Threshold:** 80% consensus (8 of 10 votes)
5. **Publish:** Decision and reasoning published within 48 hours

### Emergency Decisions (Urgent)

**Circumstances:** Security vulnerability, imminent harm

1. **Fast-track:** 48-hour comment period instead of 2 weeks
2. **Vote:** Emergency board meeting (within 72 hours)
3. **Threshold:** 80% consensus required
4. **Publish:** Decision and reasoning within 24 hours

### Reconsideration

- Any decision can be reconsidered if substantial new evidence appears
- Requires written petition from 3 board members
- Same voting threshold and process as original decision

---

## Meetings & Transparency

### Public Board Meetings

- **Frequency:** Monthly (first Thursday of each month, 6 PM PT)
- **Format:** Livestreamed on YouTube
- **Duration:** 2 hours (1.5 hours discussion + 0.5 hours Q&A from public)
- **Attendance:** Open to public (anyone can watch)
- **Questions:** Public can submit written questions 24 hours in advance

### Meeting Materials

- Agenda published 1 week in advance
- Supporting documents published 48 hours in advance
- Minutes published within 48 hours of meeting
- All voting records public (who voted which way, why)

### Annual Report

- Published by December 31 each year
- Reports on: decisions made, principles violations, framework changes
- Includes: metrics on adoption, audit results, emerging issues
- Invites: public comment on board performance

---

## Conflict of Interest

### Prohibited Activities

Board members cannot:
- Have financial interest in implementations (must divest)
- Represent employers in discussions (speak as individuals)
- Accept payments from organizations they oversee
- Have family members on other board seats

### Disclosure Requirements

- Board members must disclose: employment, investments, relationships
- Recusal from votes where they have direct interest
- Annual conflict-of-interest certification

### Violations

- Undisclosed conflicts: 6-month suspension
- Financial violations: removal from board
- Repeated violations: permanent ban + public notice

---

## Principles Enforcement

### Detecting Violations

**Sources:**
- Public reports (anyone can report)
- Whistleblowers (protected by law)
- Board monitoring (transparency dashboard)
- Audits (annual + ad-hoc)

### Investigation Process

1. **Report received** → documented
2. **Preliminary review** → assess seriousness (24 hours)
3. **Investigation** → fact-gathering (2 weeks)
4. **Hearing** → accused can respond (1 week)
5. **Vote** → board decides (monthly meeting)
6. **Remediation** → fix or removal (30 days)
7. **Public notice** → violation published (48 hours)

### Consequences

| Violation | Consequence |
|-----------|-------------|
| First minor violation | Public warning |
| First major violation | Required remediation + monitoring |
| Repeated violations | Public listing as violator |
| Severe violations (harm to people) | Referral to law enforcement |
| Refusal to remediate | Public delisting from trusted implementers |

### Whistleblower Protection

- Reporters cannot be identified (anonymous reporting)
- Retaliation forbidden (protected by law)
- Compensation available for harm (case-by-case)

---

## Standards Evolution

### New Features or Versions

**Process:**
1. Community proposes improvement (GitHub issue)
2. Discussion period (4 weeks, public comment)
3. Board review (technical soundness, ethical implications)
4. Approval (80% consensus required)
5. Implementation period (6 months, old + new coexist)
6. Sunset (old version deprecated after 12 months)

**Backwards Compatibility:**
- New versions must support old implementations for 12 months
- Breaking changes require 90% consensus (not 80%)
- Minimum 6-month notice before breaking change

### Security Updates

- Can be deployed immediately if no breaking changes
- Require documentation of vulnerability and fix
- Published within 7 days of discovery

---

## Budget & Resources

### Funding

**Sources (no single source >30% of budget):**
- Community donations (tax-deductible through nonprofit)
- Government grants (NSF, NIST, international equivalents)
- Corporate sponsorships (non-exclusive, no governance rights)
- Foundation support (Gates, Ford, Mozilla, etc.)

**Restrictions:**
- No funding from military/defense (except transparent government)
- No funding from surveillance companies
- No funding with strings attached (governance independence)

### Annual Budget

- **Approved by:** Board simple majority
- **Published:** 30 days before fiscal year
- **Spent on:**
  - Board operations (meetings, admin)
  - Community infrastructure (GitHub, website, email)
  - Documentation and outreach
  - Security audits and penetration testing

### Accountability

- Independent annual audit (published publicly)
- Detailed expense reporting (quarterly)
- Community review (anyone can request information)

---

## Dispute Resolution

### When Board Members Disagree

1. **Healthy disagreement:** Part of process, voting settles it
2. **Repeated obstruction:** Requires investigation
3. **Bad faith:** Can lead to removal

### When Community Disagrees with Board

1. **Written petition:** 100+ community members
2. **Board reconsideration:** forced review (30 days)
3. **Community vote:** If board unmoved, let community vote (non-binding but heavily weighted)
4. **Escalation:** Unanimous appeal to external mediator (chosen mutually)

### External Mediation

- Used only when board deadlocked (≤1 decision per year target)
- Mediator chosen by mutual agreement of disputing parties
- Decision is binding
- Cost split 50/50 between parties

---

## Sunset & Dissolution

### When Does This Board End?

- **Natural end:** When frameworks become government standard (unlikely, but possible)
- **Crisis end:** If unable to function (never happened in similar orgs)
- **Planned transition:** After 25 years, community votes to continue or dissolve

### If Board Dissolves

- All assets transferred to public domain
- Frameworks become pure open-source (no governance)
- Community forks manage evolution
- Archives preserved indefinitely

---

## Getting Started

### Current Status (2026)

- Board formation beginning
- Initial members being recruited
- First meeting: June 2026
- Operating budget: $500K/year (first 3 years)

### How to Get Involved

- **Vote to form board:** Community vote (Spring 2026)
- **Nominate board members:** Nominating orgs select (Summer 2026)
- **First meeting:** Public livestream (Summer 2026)
- **Join governance:** Governance board grows to 12 by Fall 2026

---

## The Principle Behind This Governance

> **Power should be distributed, transparent, and accountable to those affected.**

This board structure ensures:

- ✓ No single entity controls frameworks
- ✓ Government has no veto power (only observer status)
- ✓ Tech companies have limited influence
- ✓ Affected communities have voice
- ✓ Decisions are public and explainable
- ✓ Violations are exposed immediately
- ✓ Systems remain open forever

The frameworks themselves enforce this governance (governance logged in meta-AAPF, fairness checked by meta-PCSF, principles encoded in meta-NAP).

---

**Status:** Governance charter ready for community approval

**Next step:** Community votes to form board (Spring 2026)

