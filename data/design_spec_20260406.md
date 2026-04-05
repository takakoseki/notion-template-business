# Notion Template Design Specification

**Theme:** Meeting Notes

---

# Notion Template Design Specification: Meeting Notes Hub

---

## 1. Purpose and Target Users

### Problem This Template Solves

Managing meetings without a structured system leads to scattered notes, forgotten action items, missed follow-ups, and zero accountability. Most teams rely on disconnected tools — a Google Doc here, a Slack message there, an email thread somewhere else — resulting in decisions that vanish and tasks that never get done. This template centralizes every meeting into one intelligent workspace, transforming raw notes into trackable outcomes.

### Primary Use Cases

- **Weekly team stand-ups and sprint reviews** — capture recurring meeting patterns and track velocity over time
- **One-on-one manager/employee meetings** — maintain a running history of conversations, goals, and feedback
- **Client and stakeholder meetings** — log decisions, commitments, and next steps with full context
- **Project kickoff and retrospective meetings** — document decisions that anchor future work
- **Cross-functional planning sessions** — connect meeting outputs directly to tasks and projects
- **Board and executive briefings** — maintain a professional, searchable archive of high-level decisions

### Detailed Target User Persona

---

#### Persona 1: Alex — The Overwhelmed Project Manager

- **Age:** 32
- **Role:** Senior Project Manager at a mid-size SaaS company
- **Team Size:** Manages 3–5 cross-functional teams
- **Pain Points:**
  - Attends 6–10 meetings per day
  - Action items get buried in Slack or forgotten entirely
  - Cannot easily recall what was decided in a meeting 3 weeks ago
  - Stakeholders ask for meeting summaries and Alex has no central source
- **Goals:**
  - Reduce follow-up emails asking "what did we decide?"
  - Ensure every meeting produces at least one documented outcome
  - Show leadership a clean record of decisions and accountability
- **Notion Experience:** Intermediate — uses Notion for project tracking but has never built a meeting system

---

#### Persona 2: Jordan — The Independent Consultant

- **Age:** 28
- **Role:** UX/Product Consultant working with 4–6 clients simultaneously
- **Pain Points:**
  - Struggles to separate notes across different clients
  - Forgets commitments made verbally in calls
  - Needs professional-looking meeting records to send to clients
  - Loses track of recurring discussion themes across engagements
- **Goals:**
  - Maintain a professional paper trail for each client
  - Quickly find any past meeting in under 10 seconds
  - Impress clients with structured, shareable summaries
- **Notion Experience:** Advanced — builds their own systems but lacks a polished meeting template

---

#### Persona 3: Morgan — The Remote Team Lead

- **Age:** 40
- **Role:** Engineering Team Lead managing a fully distributed team of 8
- **Pain Points:**
  - Team members in different time zones miss async updates
  - No shared memory of architectural decisions made in calls
  - Hard to distinguish what was discussed vs. what was actually decided
  - Onboarding new team members requires re-explaining past decisions
- **Goals:**
  - Build an institutional memory that outlasts any one employee
  - Make meetings useful for people who couldn't attend live
  - Connect meeting outcomes directly to the engineering backlog
- **Notion Experience:** Beginner-to-intermediate — comfortable with Notion but never used relational databases

---

## 2. Notion Database List and Column Definitions

---

### Database 1: 📅 Meetings

**Purpose:** The core database. Every meeting — past, present, and upcoming — is logged here. This is the single source of truth for all meeting activity.

| Column Name | Data Type | Description |
|---|---|---|
| Meeting Title | Title | Name of the meeting (e.g., "Q3 Product Review — July 15") |
| Date & Time | Date | Scheduled date and start time of the meeting; enable time and timezone |
| Duration (min) | Number | Length of the meeting in minutes (e.g., 30, 60, 90) |
| Meeting Type | Select | Category: `Stand-up` / `One-on-One` / `Team Sync` / `Client Call` / `Planning` / `Retrospective` / `Ad Hoc` / `Board Meeting` |
| Status | Select | `Upcoming` / `In Progress` / `Completed` / `Cancelled` |
| Facilitator | Person | The person who ran or will run the meeting |
| Attendees | Person | All participants; supports multi-person selection |
| Project / Context | Relation | Links to the **Projects** database to associate meeting with a project |
| Action Items | Relation | Links to the **Action Items** database; shows tasks generated from this meeting |
| Decisions Made | Text | Rich text field summarizing key decisions reached during the meeting |
| Agenda | Text | Bulleted list of topics planned before the meeting begins |
| Notes | Text | Full meeting notes — supports nested bullets, headers, callouts |
| Summary (AI-ready) | Text | A 3–5 sentence plain-language summary suitable for sharing or AI prompt input |
| Recording Link | URL | Link to Zoom, Loom, or Google Meet recording |
| Next Meeting | Date | Scheduled date for the follow-up meeting if applicable |
| Recurrence | Select | `None` / `Daily` / `Weekly` / `Bi-weekly` / `Monthly` |
| Tags | Multi-select | Flexible labels: `#decision` / `#blocker` / `#strategy` / `#urgent` / `#client` / `#internal` |
| Sentiment | Select | Post-meeting energy rating: `🟢 Productive` / `🟡 Mixed` / `🔴 Unresolved` |
| Preparation Done | Checkbox | Check when agenda and pre-read materials are prepared |
| Notes Shared | Checkbox | Check when the meeting summary has been distributed to attendees |

---

### Database 2: ✅ Action Items

**Purpose:** Every task, commitment, or follow-up generated from a meeting lives here. This database ensures nothing falls through the cracks and provides a full accountability trail.

| Column Name | Data Type | Description |
|---|---|---|
| Task Name | Title | Clear description of the action item (e.g., "Send revised proposal to client by Friday") |
| Assigned To | Person | The person responsible for completing this task |
| Due Date | Date | Hard deadline for completion |
| Priority | Select | `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🟢 Low` |
| Status | Select | `Not Started` / `In Progress` / `Blocked` / `Completed` / `Cancelled` |
| Source Meeting | Relation | Links back to the **Meetings** database entry where this task originated |
| Project | Relation | Links to the **Projects** database for cross-referencing |
| Notes | Text | Any additional context, blockers, or sub-steps needed |
| Completion Date | Date | Actual date the task was marked complete |
| Blocked By | Text | Description of what is preventing progress (if Status = Blocked) |
| Recurring | Checkbox | If this action item appears after every instance of a recurring meeting |

---

### Database 3: 👥 Participants & Contacts

**Purpose:** A roster of all people who regularly attend meetings — internal team members and external contacts alike. Enables filtering meetings by person and building relationship history.

| Column Name | Data Type | Description |
|---|---|---|
| Name | Title | Full name of the participant |
| Role / Title | Text | Job title or role (e.g., "VP of Engineering", "Client Sponsor") |
| Organization | Text | Company or department name |
| Type | Select | `Internal` / `Client` / `Vendor` / `Advisor` / `Partner` |
| Email | Email | Primary contact email address |
| LinkedIn | URL | LinkedIn profile URL for quick reference |
| Meetings Attended | Relation | Links to all **Meetings** records this person appeared in |
| Action Items Owned | Relation | Links to all **Action Items** assigned to this person |
| Notes | Text | Relationship notes, communication preferences, or context |
| Last Met | Formula | Computed from Meetings Attended — displays the most recent meeting date |
| Total Meetings | Rollup | Count of all meetings linked via Meetings Attended relation |

---

### Database 4: 🗂️ Projects

**Purpose:** A lightweight project registry that provides context for meetings. Meetings and action items are tied to projects so you can view all activity related to a specific initiative.

| Column Name | Data Type | Description |
|---|---|---|
| Project Name | Title | Name of the project or initiative |
| Status | Select | `Active` / `On Hold` / `Completed` / `Cancelled` |
| Owner | Person | Primary person accountable for this project |
| Start Date | Date | Project kick-off date |
| Target End Date | Date | Projected completion date |
| Description | Text | Brief summary of what this project entails |
| Related Meetings | Relation | All **Meetings** linked to this project |
| Open Action Items | Rollup | Count of Action Items from related meetings with Status ≠ Completed |
| Total Meetings | Rollup | Total count of meetings linked to this project |
| Priority | Select | `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🟢 Low` |
| Tags | Multi-select | `#Q1` / `#Q2` / `#Q3` / `#Q4` / `#External` / `#Internal` / `#Strategic` |

---

### Database 5: 📋 Meeting Templates Library

**Purpose:** A reusable library of agenda templates for different meeting types. Users pull from this library when preparing a new meeting to ensure consistency and save preparation time.

| Column Name | Data Type | Description |
|---|---|---|
| Template Name | Title | Name of the template (e.g., "Weekly Team Stand-Up", "Client Kickoff Agenda") |
| Meeting Type | Select | Must match options in the Meetings database Meeting Type column |
| Agenda Structure | Text | Pre-written agenda with time blocks and discussion prompts |
| Suggested Duration | Number | Recommended meeting length in minutes |
| Key Questions | Text | Standard questions to ask during this type of meeting |
| Decision Framework | Text | What decisions should this meeting type produce? |
| Pre-Work Required | Text | What should attendees prepare or review before attending? |
| Post-Meeting Actions | Text | Standard follow-up steps that always apply to this meeting type |
| Usage Count | Number | Manually updated count of how many times this template has been used |

---

## 3. Page Structure

```
📁 Meeting Notes Hub [Top-Level Page / Dashboard]
│
├── 🏠 Dashboard [Sub-page]
│   ├── 📊 This Week's Meetings [Gallery or Calendar view of Meetings DB filtered to current week]
│   ├── ✅ My Open Action Items [Filtered view of Action Items DB — current user, Status ≠ Completed]
│   ├── 🔴 Overdue Tasks [Filtered view — Due Date < Today, Status ≠ Completed]
│   └── 📌 Quick Add Buttons [Template buttons to create new meeting or action item instantly]
│
├── 📅 All Meetings [Sub-page]
│   ├── 📋 Full Table View [All meetings, sortable by date]
│   ├── 📆 Calendar View [Monthly calendar layout by meeting date]
│   ├── 🗂️ Board View — By Status [Kanban: Upcoming / In Progress / Completed / Cancelled]
│   ├── 🏷️ Gallery View — By Type [Visual cards grouped by Meeting Type]
│   └── 🔍 Search & Filter Bar [Preset filters: By Person / By Project / By Tag / By Date Range]
│
├── ✅ Action Items [Sub-page]
│   ├── 📋 All Tasks Table [Full table with all columns visible]
│   ├── 🗂️ Board View — By Status [Kanban: Not Started / In Progress / Blocked / Completed]
│   ├── 👤 Grouped by Assignee [Table grouped by Assigned To person]
│   ├── 📅 Timeline View [Gantt-style by Due Date]
│   └── 🔴 Overdue View [Filtered: Due Date past, Status ≠ Completed, sorted by urgency]
│
├── 👥 People & Contacts [Sub-page]
│   ├── 📋 Full Directory Table [All participants with role, org, and type]
│   ├── 🏢 By Organization [Table grouped by Organization field]
│   └── 🔗 Individual Contact Pages [Each person page auto-shows their meetings and action items via relation]
│
├── 🗂️ Projects [Sub-page]
│   ├── 📋 Projects Table [All projects with status, owner, and rollup counts]
│   ├── 🗂️ Board View — By Status [Active / On Hold / Completed]
│   └── 🔗 Individual Project Pages [Each project page shows linked meetings and open action items]
│
├── 📋 Meeting Templates Library [Sub-page]
│   ├── 📄 Templates Table [All templates listed by type]
│   └── 🔗 Individual Template Pages [Full agenda and framework for each meeting type]
│
├── 📖 How to Use This Template [Sub-page]
│   ├── Getting Started Guide [3-step flow — see Section 4]
│   ├── Field Definitions Glossary [Plain-language explanation of every column]
│   ├── Tips & Best Practices [Recommended workflows]
│   └── FAQ [Common questions and troubleshooting]
│
└── 🗃️ Archive [Sub-page]
    └── 📦 Archived Meetings [Filtered view: Status = Cancelled + meetings older than 90 days]
```

### Database Placement Summary

| Database | Primary Home Page | Also Visible In |
|---|---|---|
| Meetings | `/All Meetings` | Dashboard, Projects (via relation), People (via relation) |
| Action Items | `/Action Items` | Dashboard (filtered), Meetings (inline relation), Projects (via rollup) |
| Participants & Contacts | `/People & Contacts` | Meetings (inline via Person field) |
| Projects | `/Projects` | Meetings (relation), Action Items (relation), Dashboard |
| Meeting Templates Library | `/Meeting Templates Library` | Referenced during new meeting creation |

---

## 4. Getting-Started Flow (3 Steps)

---

### ✅ Step 1: Set Up Your Workspace (5 minutes)

**Before logging your first meeting, personalize the template foundation.**

1. Navigate to the **📖 How to Use This Template** page and read the one-page quick-start overview.
2. Open the **🗂️ Projects** database and add at least 2–3 projects or contexts relevant to your work (e.g., "Q4 Product Launch", "Client: Acme Corp", "Team Operations"). Even single entries like "General / Misc" are fine — the goal is to have something to link meetings to.
3. Open the **👥 People & Contacts** database and add the people you meet with most frequently. Fill in their name, role, organization, and type (`Internal` vs. `Client`). You do not need to add everyone upfront — you can add new contacts as meetings come up.
4. Visit the **📋 Meeting Templates Library** and review the pre-built agenda templates. Select one that matches your most common meeting type and read through its structure — this is what you will use in Step 2.

> 💡 **Pro Tip:** Duplicate an existing template entry in the Templates Library to create a custom agenda format for a meeting type unique to your workflow.

---

### ✅ Step 2: Log Your First Meeting (10 minutes)

**Create your first real meeting entry and experience the full workflow.**

1. From the **🏠 Dashboard**, click the **"+ New Meeting"** quick-add button (or navigate to **📅 All Meetings** and click `+ New`).
2. Fill in the core fields:
   - **Meeting Title** → give it a specific, searchable name (e.g., "Product Team Weekly Sync — Week 28")
   - **Date & Time** → set the exact date and start time
   - **Meeting Type** → choose the closest match from the dropdown
   - **Attendees** → tag everyone who attended or will attend
   - **Project / Context** → link to the relevant project you created in Step 1
   - **Agenda** → paste in the agenda structure from your chosen template in Step 1
3. During or immediately after the meeting, return to this entry and fill in:
   - **Notes** → raw meeting notes, decisions, and discussion points
   - **Decisions Made** → extract and summarize the 2–3 key decisions reached
   - **Summary** → write a 3–5