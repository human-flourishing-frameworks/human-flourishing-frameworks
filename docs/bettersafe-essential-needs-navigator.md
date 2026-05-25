# BetterSafe Essential Needs Navigator

## Purpose

The Essential Needs Navigator is the first implementation path under the Pain anchor.

Pain is the anchor. The navigator is a manual, privacy-preserving tool for turning urgent human need into a concrete next action.

## Scope

The navigator helps with:

```text
food
money pressure
housing
utilities
transportation
phone/connectivity
child/family logistics
pets
work access
emotional overload under scarcity
```

It does not guarantee resources, make payments, provide legal/medical/financial authority, or replace human/community support.

## Current Mode

```text
manual-only
local/private first
no raw bank credentials
no live money movement
no unattended financial execution
no hidden telemetry
no public private data
no third-party outreach without user action
no child/private-person profiling
```

Money handling is not impossible forever. It is currently high-risk and requires evidence, consent, legal/compliance review, security, reversibility, limits, audit, and demonstrated benefit before activation.

## Navigator Intake

Use role labels and minimum-necessary details.

| Field | Prompt | Privacy note |
|---|---|---|
| Need category | What essential need is active? | Use categories, not private stories. |
| Deadline | When does this matter? | Use date/time if known. |
| Amount / quantity | What number matters? | Bills/amounts only if needed. |
| Current status | What is true now? | Separate known / unknown / assumed. |
| Owner | Who owns the next action? | Use roles unless explicit names are necessary. |
| Next action | What is the smallest useful step? | Must be physically actionable. |
| Resource path | Who/what can help? | Category first: 211, pantry, utility, bank, landlord, mechanic, school, etc. |
| Privacy sensitivity | What must not be recorded? | Redact private citizens by default. |
| Feedback | What happened after action? | Record only minimum useful result. |

## Essential Needs Triage

Use a bounded, context-aware order. It is not absolute.

```text
acute safety
food/water
shelter/housing
utilities
work/school access
transportation
phone/connectivity
child/family needs
pets
debt/fees/administrative pressure
```

The order can change based on deadline, severity, consent, and local reality.

## Pain-to-Action Worksheet

```text
Need:
Deadline:
Known facts:
Unknowns:
Amount / quantity:
Owner:
Smallest next action:
Resource/contact category:
Script needed? yes/no
Privacy sensitivity:
Status: unknown / blocked / in progress / done / needs follow-up
Feedback/result:
```

## Call / Message Script Templates

### 211 / resource routing

```text
I am looking for help with [food / utilities / housing / transportation / phone / pet food / other].
My deadline is [date/time if known].
I am not asking you to solve everything; I need the next available resource or referral.
What information should I have ready, and what is the fastest safe next step?
```

### Utility payment arrangement

```text
I need to discuss my bill and avoid shutoff if possible.
The amount due is [amount], and the due/shutoff date is [date].
What payment arrangement, assistance program, extension, or hardship option is available?
```

### Utility crisis: large past-due electric bill

Use this path when the bill is large, old, or shutoff risk is unclear.

Current example shape:

```text
electric / power bill
approximately $7,000
approximately 3 months old
shutoff status unknown
household pressure high
```

Do not keep building project features while the household may lose power unless
the operator explicitly chooses a bounded work block after the utility triage
step is assigned.

First 30-minute path:

```text
1. Find the latest bill or online account balance.
2. Write down account holder, utility company, account number, amount due,
   due date, shutoff/disconnect notice date if any, and service address.
3. Call the utility company and ask for the disconnection department or
   hardship/payment arrangement team.
4. Ask: Is there an active shutoff order? What exact payment prevents shutoff
   today? What payment plan, extension, medical hold, hardship program, or
   arrears-management option exists?
5. Call or search 211 for utility assistance in the county.
6. Use LIHEAP / energy assistance office lookup for the state or tribe.
7. If shutoff is imminent, ask the state public utility commission / consumer
   assistance line what protections or complaint/dispute path exists.
8. Record only the minimum result and next deadline.
```

Emergency utility call script:

```text
I am calling because the electric bill is about [$amount] and about [age] old.
I need to prevent shutoff or restore a safe payment path.
Is there an active disconnect order or shutoff date?
What exact amount would stop shutoff today?
Can you offer a payment arrangement, hardship extension, arrears plan,
medical certificate hold, budget billing review, or referral to assistance?
Can you email or text the agreement and the next deadline?
```

211 / LIHEAP script:

```text
I need emergency electric bill help. The bill is about [$amount], about [age]
old, and shutoff status is [known/unknown].
What utility assistance, LIHEAP, community action, church/nonprofit, or
emergency fund can I contact today?
What documents should I have ready?
```

Documents to gather:

```text
latest utility bill or account screenshot
shutoff/disconnect notice if any
photo ID for account holder if required
proof of address
proof of income or benefit letter if applying for assistance
household size
medical electricity need documentation if relevant
any prior payment arrangement
```

Source routes:

```text
USAGov utility bill help: https://www.usa.gov/help-with-utility-bills
LIHEAP Clearinghouse local help: https://liheapch.acf.gov/get_help.htm
211 bill help: https://www.211.org/get-help/i-need-help-paying-my-bills
```

Boundary:

```text
BetterSafe does not pay, borrow, access accounts, impersonate the account
holder, or promise assistance. It helps make the next call, document list,
deadline, and follow-up visible.
```

### Bank fee / negative balance

```text
I need the exact amount required to bring the account positive or stop additional fees.
Please tell me:
1. current balance,
2. active fees,
3. whether fees continue daily/weekly/one-time,
4. minimum payment needed to restore necessary account function.
```

### Food pantry / emergency food

```text
I am checking whether emergency food help is available for the next few days.
What are your hours, requirements, and pickup process?
Do I need ID, proof of address, or an appointment?
```

### Housing assistance

```text
I need help understanding what assistance or payment-plan options may exist for rent/mortgage pressure.
The relevant date is [date].
What documents should I gather, and what is the next step?
```

### Transportation / work access

```text
I need help keeping work/school access stable.
The issue is [gas / ride / repair / registration / insurance / other].
The deadline is [date/time].
What low-cost, emergency, or local options exist?
```

### Phone / connectivity

```text
I need to keep phone/connectivity active for work/family logistics.
The bill or deadline is [amount/date].
Are there lower-cost, hardship, extension, or assistance options?
```

### Pet food / pet care

```text
I need help finding pet food or low-cost pet care resources.
The need is [food / medication / vet / other].
What local resources, pantry days, or assistance options are available?
```

## Safe-Fun Check

Every next action should stay inside the safe-fun band:

```text
safe enough to continue
fun/hopeful/humane enough to want to continue
```

Ask:

```text
Does this action reduce immediate Pain?
Does it preserve privacy and dignity?
Does it avoid coercion or shame?
Does it leave a return path?
Does it avoid dumping all burden on one person?
```

## Redaction Rules

Default durable records must use:

```text
private participant
household partner
trusted adult
protected minor
third party
resource worker
pilot user
```

Avoid storing:

```text
private-citizen names
contact information
workplaces
locations
raw transcripts
bank credentials
protected-minor details
third-party gossip
identifying anecdotes
```

## Pilot Feedback

After use, ask:

```text
Did this identify the next urgent need?
Did it reduce time to a real action?
Did a call/message/resource action happen?
Did it reduce overload?
Did it preserve privacy?
Did it create shame, pressure, or confusion?
Would the person use it again?
What failed?
What should change?
```

## Stop / Pivot Conditions

Stop, slow, or pivot if:

```text
private people are exposed
support increases household pressure
pilot user feels coerced or surveilled
BetterSafe creates false hope about money/housing/cars
operator overload worsens
repo work replaces material support
symbolic language outruns implementation
```

## Validation Phrase

```text
The Essential Needs Navigator succeeds only if it helps a person move from Pain to a concrete, privacy-protecting next action without promising rescue or replacing human consent.
```
