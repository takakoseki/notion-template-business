# Notion Template Design Specification

**Theme:** CRM / Sales

---

# Notion CRM & Sales Template — Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Managing customer relationships and sales pipelines across spreadsheets, sticky notes, email threads, and disconnected tools creates chaos, lost deals, and missed follow-ups. This Notion CRM template consolidates every stage of the sales process — from first contact to closed deal — into a single, structured workspace that eliminates context-switching and gives sales professionals instant visibility into their pipeline health.

### Primary Use Cases

- Tracking leads from initial contact through qualification, proposal, negotiation, and close
- Managing a contact and company database with full relationship history
- Logging every interaction (calls, emails, meetings) against contacts and deals
- Setting and monitoring follow-up tasks with due dates and priorities
- Forecasting revenue based on deal stage probability weightings
- Analyzing win/loss patterns to improve sales strategy over time

### Target User Persona

---

**Persona 1 — "The Solo Consultant"**
- **Name:** Marcus T.
- **Role:** Independent B2B consultant / freelancer
- **Company size:** 1 person
- **Tech savvy:** Moderate — comfortable with Notion, uses Google Workspace
- **Pain points:** Loses track of which prospects he pitched last week; forgets follow-up dates; has no clear view of projected monthly income
- **Goal:** A lightweight but professional system to manage 20–40 active prospects without paying for Salesforce

---

**Persona 2 — "The Early-Stage Sales Rep"**
- **Name:** Priya K.
- **Role:** Account Executive at a 15-person SaaS startup
- **Company size:** Startup (seed to Series A)
- **Tech savvy:** High — already uses Notion for personal productivity
- **Pain points:** Company has no formal CRM; deals live in a shared Google Sheet that nobody keeps updated; no accountability for pipeline hygiene
- **Goal:** A team-ready CRM her manager can also view, with pipeline stages, deal values, and activity logs that update in real time

---

**Persona 3 — "The Small Business Owner"**
- **Name:** David & Sarah L.
- **Role:** Co-owners of a boutique marketing agency
- **Company size:** 8 employees, 2 on sales
- **Tech savvy:** Low-to-moderate — prefers visual, no-code tools
- **Pain points:** Clients fall through the cracks during busy periods; no record of what was promised during sales calls; invoicing is disconnected from the sales process
- **Goal:** A simple CRM that anyone on the team can open and immediately understand, with color-coded statuses and a Kanban pipeline view

---

## 2. Notion Database List and Column Definitions

### Database 1 — 📋 Contacts

**Purpose:** Stores every individual person the team interacts with — prospects, leads, existing clients, and referral partners. Serves as the central people directory linked to companies, deals, and activity logs.

| Column Name | Data Type | Description |
|---|---|---|
| Name | Title | Full name of the contact (primary field) |
| Email | Email | Primary business email address |
| Phone | Phone | Direct phone or mobile number |
| Job Title | Text | Contact's role at their company (e.g., "VP of Marketing") |
| Company | Relation → Companies DB | Links the contact to their employer in the Companies database |
| Lead Source | Select | How this contact was acquired: `Referral` / `LinkedIn` / `Cold Outreach` / `Inbound` / `Event` / `Website` / `Other` |
| Contact Status | Select | Current relationship stage: `Lead` / `Prospect` / `Active Client` / `Past Client` / `Partner` / `Unqualified` |
| Owner | Person | Notion team member responsible for this contact |
| Last Contact Date | Date | Date of the most recent interaction (manually updated or via rollup) |
| Next Follow-Up | Date | Scheduled date for the next outreach action |
| LinkedIn URL | URL | Link to the contact's LinkedIn profile |
| Notes | Text | Free-form notes about the contact's preferences, context, or history |
| Deals | Relation → Deals DB | All deals associated with this contact |
| Activities | Relation → Activity Log DB | All logged interactions with this contact |
| Tags | Multi-select | Flexible labels: `Decision Maker` / `Champion` / `Technical Buyer` / `Economic Buyer` / `Influencer` |
| Priority | Select | Outreach priority: `High` / `Medium` / `Low` |
| Date Added | Date | Date this record was created in the CRM |

---

### Database 2 — 🏢 Companies

**Purpose:** Stores organization-level data. Contacts and deals roll up to companies, providing a full account view — how many contacts exist at a company, the total value of all deals, and the current relationship health.

| Column Name | Data Type | Description |
|---|---|---|
| Company Name | Title | Legal or trading name of the organization |
| Industry | Select | Sector: `SaaS` / `E-commerce` / `Healthcare` / `Finance` / `Education` / `Retail` / `Manufacturing` / `Agency` / `Non-profit` / `Other` |
| Company Size | Select | Headcount band: `1–10` / `11–50` / `51–200` / `201–1000` / `1000+` |
| Website | URL | Company's main website URL |
| HQ Location | Text | City and country of headquarters |
| Annual Revenue | Select | Estimated ARR bracket: `<$1M` / `$1M–$10M` / `$10M–$50M` / `$50M–$250M` / `$250M+` |
| Account Status | Select | `Prospect` / `Active Client` / `Churned` / `Partner` / `Blacklisted` |
| Account Owner | Person | Team member who owns the overall account relationship |
| Contacts | Relation → Contacts DB | All people at this company |
| Number of Contacts | Rollup | COUNT of related contacts |
| Deals | Relation → Deals DB | All deals associated with this account |
| Total Deal Value | Rollup | SUM of `Deal Value` from related deals |
| Open Deals | Rollup | COUNT of deals where Stage ≠ `Closed Won` or `Closed Lost` |
| Last Activity | Date | Date of the most recent logged activity (manually maintained) |
| Notes | Text | Strategic notes about the account, competitors used, contract details |
| Tags | Multi-select | Custom labels: `Enterprise` / `SMB` / `Strategic` / `High Churn Risk` / `Upsell Opportunity` |

---

### Database 3 — 💼 Deals (Pipeline)

**Purpose:** The core of the sales pipeline. Each record represents a single revenue opportunity. This is where win probability, deal value, and stage progression are tracked. Powers all pipeline and forecasting views.

| Column Name | Data Type | Description |
|---|---|---|
| Deal Name | Title | Descriptive name (e.g., "Priya K. — Enterprise Plan Upgrade") |
| Company | Relation → Companies DB | The account this deal belongs to |
| Primary Contact | Relation → Contacts DB | The main decision-maker for this deal |
| Deal Value | Number | Expected contract value in USD (or chosen currency) |
| Deal Stage | Select | `Lead` / `Qualified` / `Proposal Sent` / `Negotiation` / `Closed Won` / `Closed Lost` |
| Win Probability (%) | Number | Manual or stage-driven probability estimate (0–100) |
| Weighted Value | Formula | `Deal Value × (Win Probability / 100)` — for forecasting |
| Close Date (Expected) | Date | Anticipated date the deal will be closed |
| Close Date (Actual) | Date | The date the deal was actually won or lost |
| Deal Owner | Person | Sales rep responsible for driving this deal to close |
| Deal Type | Select | `New Business` / `Upsell` / `Cross-sell` / `Renewal` |
| Product / Service | Multi-select | Which offerings are included: `Starter Plan` / `Pro Plan` / `Enterprise Plan` / `Consulting` / `Implementation` / `Support` |
| Lost Reason | Select | Only used when Stage = `Closed Lost`: `Price` / `Competitor` / `No Budget` / `No Decision` / `Timing` / `Wrong Fit` |
| Activities | Relation → Activity Log DB | All logged interactions related to this deal |
| Activity Count | Rollup | COUNT of related activity records |
| Proposal URL | URL | Link to the Google Doc, PDF, or proposal tool link |
| Contract URL | URL | Link to the signed contract or DocuSign link |
| Notes | Text | Deal-specific context, negotiation notes, stakeholder concerns |
| Priority | Select | `High` / `Medium` / `Low` — internal prioritization |
| Created Date | Date | When this deal record was first created |
| Days in Stage | Formula | `dateBetween(now(), prop("Created Date"), "days")` — flag stale deals |

---

### Database 4 — 📞 Activity Log

**Purpose:** A chronological record of every interaction with contacts and deals — calls, emails, meetings, demos, LinkedIn messages, and notes. Keeps the full history accessible and links activity back to both the person and the opportunity.

| Column Name | Data Type | Description |
|---|---|---|
| Activity Title | Title | Short description of the interaction (e.g., "Discovery Call — Marcus") |
| Activity Type | Select | `Call` / `Email` / `Meeting` / `Demo` / `LinkedIn Message` / `Proposal Walkthrough` / `Follow-up` / `Note` |
| Date & Time | Date | When the activity occurred (include time for calendar alignment) |
| Duration (mins) | Number | Length of the interaction in minutes (for calls and meetings) |
| Contact | Relation → Contacts DB | The person this activity involved |
| Deal | Relation → Deals DB | The deal this activity is linked to (optional) |
| Direction | Select | `Outbound` (we initiated) / `Inbound` (they initiated) |
| Outcome | Select | `Positive` / `Neutral` / `Negative` / `No Answer` / `Left Voicemail` |
| Next Step | Text | What action was agreed upon as a result of this interaction |
| Next Step Due Date | Date | Deadline for the agreed next action |
| Logged By | Person | Team member who recorded this activity |
| Summary / Notes | Text | Key takeaways, what was discussed, objections raised, commitments made |
| Follow-up Created | Checkbox | Checked once a follow-up task has been created in the Tasks DB |

---

### Database 5 — ✅ Tasks & Follow-Ups

**Purpose:** A dedicated task manager for all sales-related actions — follow-up calls to book, proposals to send, contracts to chase. Linked to contacts and deals so tasks always have context. Prevents any ball from being dropped.

| Column Name | Data Type | Description |
|---|---|---|
| Task Name | Title | Clear action item (e.g., "Send revised proposal to David L.") |
| Due Date | Date | Deadline for task completion |
| Priority | Select | `🔴 Urgent` / `🟠 High` / `🟡 Medium` / `🟢 Low` |
| Status | Select | `Not Started` / `In Progress` / `Waiting on Client` / `Completed` / `Cancelled` |
| Assigned To | Person | Team member responsible for completing this task |
| Related Contact | Relation → Contacts DB | The contact this task is associated with |
| Related Deal | Relation → Deals DB | The deal this task supports |
| Task Type | Select | `Follow-up Call` / `Send Email` / `Send Proposal` / `Schedule Meeting` / `Internal Review` / `Admin` / `Other` |
| Reminder Date | Date | Date to surface the task in a reminder view (earlier than due date) |
| Notes | Text | Additional context or instructions for completing the task |
| Completed Date | Date | Actual date the task was marked done |
| Recurring | Checkbox | Flag tasks that should repeat (e.g., weekly check-in calls) |

---

### Database 6 — 📊 Revenue Tracker

**Purpose:** A high-level financial record of closed deals, invoices, and payments received. Separate from the pipeline, this database tracks real money — what has been invoiced, what has been collected, and what remains outstanding.

| Column Name | Data Type | Description |
|---|---|---|
| Invoice / Revenue Name | Title | Reference name (e.g., "INV-2024-047 — Priya K.") |
| Deal | Relation → Deals DB | The closed deal this revenue record relates to |
| Company | Relation → Companies DB | The client company being invoiced |
| Invoice Amount | Number | Total amount invoiced (USD) |
| Amount Received | Number | Amount actually paid to date |
| Outstanding Balance | Formula | `Invoice Amount − Amount Received` |
| Invoice Date | Date | Date the invoice was issued |
| Due Date | Date | Payment due date |
| Payment Date | Date | Actual date payment was received |
| Payment Status | Select | `Draft` / `Sent` / `Partially Paid` / `Paid` / `Overdue` / `Cancelled` |
| Payment Method | Select | `Bank Transfer` / `Credit Card` / `PayPal` / `Stripe` / `Check` / `Other` |
| Invoice URL | URL | Link to the invoice file (PDF, FreshBooks, QuickBooks, etc.) |
| Notes | Text | Payment terms, late payment notes, partial payment context |
| Month | Formula | `formatDate(prop("Invoice Date"), "MMMM YYYY")` — for monthly grouping |

---

## 3. Page Structure

### Full Page Hierarchy

```
🏠 [ROOT] CRM & Sales Hub
│
├── 📊 Dashboard (Top-Level Page)
│   ├── Pipeline Snapshot (Deals DB → Board View by Stage)
│   ├── Today's Tasks (Tasks DB → Filtered View: Due Today)
│   ├── Revenue Summary (Revenue Tracker DB → Gallery/Table)
│   ├── Recent Activity (Activity Log DB → Last 7 days)
│   └── Quick-Add Buttons (Linked DB shortcuts to add Contact / Deal / Task)
│
├── 📋 Contacts & Companies
│   ├── [DATABASE] 📋 Contacts
│   │   ├── View: All Contacts (Table, sorted by Last Contact Date)
│   │   ├── View: My Contacts (Filtered: Owner = Me)
│   │   ├── View: Hot Leads (Filtered: Status = Lead, Priority = High)
│   │   ├── View: Follow-Up Queue (Filtered: Next Follow-Up ≤ Today + 3 days)
│   │   └── View: By Lead Source (Grouped by Lead Source)
│   │
│   └── [DATABASE] 🏢 Companies
│       ├── View: All Accounts (Table)
│       ├── View: Active Clients (Filtered: Account Status = Active Client)
│       ├── View: By Industry (Grouped by Industry)
│       └── View: Top Accounts (Sorted by Total Deal Value, descending)
│
├── 💼 Pipeline & Deals
│   ├── [DATABASE] 💼 Deals
│   │   ├── View: 🗂️ Kanban Pipeline (Board by Deal Stage) ← DEFAULT VIEW
│   │   ├── View: 📋 All Deals (Table, all fields visible)
│   │   ├── View: 🔥 My Active Deals (Filtered: Owner = Me, Stage ≠ Closed)
│   │   ├── View: 📅 Closing This Month (Filtered: Close Date within current month)
│   │   ├── View: 🏆 Closed Won (Filtered: Stage = Closed Won)
│   │   ├── View: ❌ Closed Lost (Filtered: Stage = Closed Lost, Grouped by Lost Reason)
│   │   └── View: ⚠️ Stale Deals (Filtered: Days in Stage > 14)
│   │
│   └── 📈 Forecasting Page (Inline content + linked Deals DB)
│       ├── Weighted Pipeline Total (Rollup / manual formula display)
│       ├── Deals by Stage (Gallery or Table grouped by stage)
│       └── Monthly Close Forecast (Filtered view: Close Date = this month)
│
├── 📞 Activity Log
│   └── [DATABASE] 📞 Activity Log
│       ├── View: All Activities (Table, sorted by Date descending)
│       ├── View: Today's Activities (Filtered: Date