# RAG Dollhouse Convergence Plan

Status: master repo planning record
Updated: 2026-05-30

## Purpose

The RAG Dollhouse is the master memory, sales, manufacturing, and product-orchestration layer for the Human Flourishing / Lantern OS physical-product program. It should not be treated as a standalone novelty product first. It is the source-of-truth structure where every customer, product, supplier, patent/spec packet, and shipment has a room.

## Core Model

Each major entity gets a room:

| Room | Purpose |
| --- | --- |
| Founder Room | Founder goals, cash runway, current decisions, priority gates. |
| Customer Room | Leads, outreach history, purchases, support state, consent records. |
| Product Room | Orion Watch MK1, Orion Charge Scarf, Memory Puck, Lantern Ring, ship kits. |
| Supplier Room | Vendors, quotes, MOQs, lead times, compliance documents, sample history. |
| Patent Room | Claim concepts, invention disclosures, prior-art review state, filing status. |
| Manufacturing Room | Samples, batch plans, QA checklists, defects, acceptance records. |
| Sales Room | Discord lead intake, Gmail follow-up, SMS consent/outreach, invoices, receipts. |
| Family Room | Caregiver and childcare insights, Courtney-style advisory feedback, language review. |
| Memory Room | Receipts, design rationale, conversations, convergence decisions. |

## Sales and Economics Flow

```text
Discord lead signal
  -> Sales MCP capture
  -> RAG Dollhouse Customer Room
  -> Gmail context follow-up
  -> SMS close only with explicit consent
  -> Payment receipt
  -> Product / Manufacturing Room update
  -> Fulfillment record
```

The Dollhouse is the system of record. Salesforce or another CRM can be added later as a sync target after the local economics loop proves itself.

## Physical Product Streams

| Stream | Product | First Shipping Strategy | Current Gate |
| --- | --- | --- | --- |
| A | Orion Watch MK1 | Donor-platform watch kit with face, strap, charger, ship kit. | Limited private pilot. |
| B | Orion Charge Scarf / Travel Wrap | Textile-first storefront product with hidden pocket and puck integration. | First revenue candidate. |
| C | Memory Puck / Local Tap Kit | Passive NFC/QR token, pouch, and quick-start card. | First accessory candidate. |
| D | Lantern Ring Audio Gate MK1 | Symbolic/design prototype and sizing study. | Hold custom electronics. |
| E | RAG Dollhouse Physical Kit | Miniature illuminated room model for demonstration and internal ritual. | Concept/sample only. |
| F | PPE / Exosuit Concepts | Internal research and design packet only. | Do not sell; safety/legal hold. |

## Manufacturing Gates

| Gate | Meaning | Allowed Quantity |
| --- | --- | ---: |
| G0 Concept | Repo spec, images, claim-safe language. | 0 |
| G1 Supplier Inquiry | Quotes/docs only. | 0 |
| G2 Sample | Buy physical samples. | 1-2 |
| G3 Validation | Fit, finish, safety, packaging, returns, claims review. | 0 public sales |
| G4 Pilot Batch | Small paid/private batch. | 10-50 |
| G5 Public Sale | Storefront listing, support, returns, QA process ready. | 50+ |
| G6 Repeatable Batch | Supplier, margin, QA, fulfillment proven. | 100+ |

## Claim Boundaries

Do not publicly claim:

- Patent pending unless an application has actually been filed.
- Medical, safety, rescue, waterproof, payment, certified battery, PPE, emergency, or surveillance capabilities without supporting certification/legal review.
- Custom RF, custom battery, custom PCB, or custom OS capability for Orion Watch MK1 while it remains donor-platform.

Allowed early language:

- Prototype.
- Donor-platform sample.
- Private review kit.
- Textile travel accessory.
- Passive NFC/QR memory token.
- Concept validation.
- Supplier evidence packet.

## Sales MCP Backbone

Minimum tools:

- capture_discord_lead
- qualify_lead
- create_opportunity
- log_gmail_outreach
- record_sms_consent
- log_sms_outreach
- attach_payment_receipt
- next_best_sales_action
- summarize_sales_pipeline

Minimum ledgers:

- data/sales/leads.jsonl
- data/sales/opportunities.jsonl
- data/sales/outreach-log.jsonl
- data/sales/sms-consent.jsonl
- data/sales/payment-receipts.jsonl

SMS outreach must be blocked unless explicit consent exists.

## Next Promotion Candidates

1. RAG Dollhouse room schema.
2. Orion physical product catalog.
3. Supplier registry.
4. Sales ledger UI.
5. Manufacturing dashboard.
6. Fulfillment dashboard.
7. Private-image/spec packet index.
8. Salesforce/CRM sync only after pipeline volume justifies it.

## Confidence Table

| Decision | Confidence |
| --- | ---: |
| RAG Dollhouse as system of record | 95% |
| Discord -> Gmail -> SMS funnel | 95% |
| Scarf / travel wrap as first revenue product | 90% |
| Memory Puck as first accessory product | 90% |
| Orion Watch MK1 as limited donor-platform pilot | 80% |
| Lantern Ring as production-ready | 40% |
| RAG Dollhouse physical kit as near-term sale | 35% |
| Salesforce needed immediately | 20% |
| MCP-first sales system | 95% |

## Operating Rule

Ship soft goods and passive accessories first. Pilot donor-platform watch kits second. Keep custom electronics, PPE, medical/safety claims, and patent-pending language behind review gates until evidence exists.
