# Notion Template Design Specification

**Theme:** Meeting Notes

---

# Meeting Notes — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Professionals and teams struggle with scattered, inconsistent meeting documentation. Notes live in random documents, action items get lost in email threads, decisions are forgotten, and follow-ups slip through the cracks. This template consolidates every aspect of the meeting lifecycle — preparation, documentation, action tracking, and follow-up — into a single, structured Notion workspace.

### Primary Use Cases

- **Pre-meeting preparation**: Building agendas, assigning pre-read materials, and clarifying objectives before the meeting starts
- **Live note-taking**: Capturing decisions, discussion points, and action items in real time during the meeting
- **Post-meeting follow-up**: Tracking action items to completion, sharing summaries with stakeholders, and archiving decisions for future reference
- **Cross-meeting visibility**: Searching across all past meetings by project, team, attendee, or date range
- **Accountability management**: Ensuring owners are assigned to every action item with clear due dates

### Target User Persona

| Attribute | Detail |
|---|---|
| **Name** | Alex Rivera |
| **Role** | Project Manager / Team Lead |
| **Team Size** | 5–25 people |
| **Industry** | Tech, Consulting, Marketing, or any knowledge-work field |
| **Pain Points** | Forgetting what was decided in last week's standup; asking "who owns this?" repeatedly; re-litigating decisions already made |
| **Goals** | Run tighter meetings, maintain a searchable decision log, never miss a follow-up |
| **Notion Experience** | Intermediate — comfortable with databases and linked views |
| **Also Useful For** | Executive assistants, product managers, department heads, freelancers managing multiple client accounts, remote-first teams |

---

## 2. Notion Database List and Column Definitions

### Database 1: 📅 Meetings

**Purpose**: The central record of every meeting. Each row represents one meeting instance and links to all related databases.

| Column Name | Data Type | Description |
|---|---|---|
| **Meeting Title** | Title | Name of the meeting (e.g., "Q3 Roadmap Planning") |
| **Date & Time** | Date (include time) | Scheduled start date and time of the meeting |
| **End Time** | Date (include time) | Scheduled end time; used to calculate duration |
| **Duration (min)** | Formula | `dateBetween(prop("End Time"), prop("Date & Time"), "minutes")` — auto-calculates meeting length |
| **Meeting Type** | Select | Options: `Standup` / `Brainstorm` / `Decision` / `Retrospective` / `Client Call` / `One-on-One` / `All-Hands` / `Workshop` |
| **Status** | Select | Options: `Scheduled` / `In Progress` / `Completed` / `Cancelled` |
| **Project / Team** | Relation → Projects & Teams DB | Links the meeting to one or more projects or teams |
| **Attendees** | Relation → People DB | Links to all participants |
| **Facilitator** | Relation → People DB | The person running the meeting |
| **Meeting Goal** | Text (rich text) | One-sentence objective: what "done" looks like for this meeting |
| **Agenda** | Text (rich text) | Bulleted list of agenda items with time allocations |
| **Pre-Read Materials** | URL or File & Media | Links to docs, decks, or files attendees should review beforehand |
| **Meeting Notes** | Text (rich text) | Full live notes taken during the meeting |
| **Decisions Made** | Text (rich text) | Explicit log of decisions reached (structured as a numbered list) |
| **Follow-Up Required?** | Checkbox | Checked if the meeting generated action items or a follow-up meeting |
| **Action Items Count** | Rollup | Rolls up count of related Action Items (Count All) |
| **Open Actions Count** | Rollup | Rolls up count of Action Items where Status ≠ `Done` |
| **Recording Link** | URL | Link to Zoom, Loom, or Google Meet recording |
| **Tags** | Multi-select | Freeform labels: e.g., `Urgent`, `Strategic`, `External`, `Recurring` |
| **Recurring Meeting?** | Checkbox | Flag for meetings that repeat on a schedule |
| **Recurrence Pattern** | Select | Options: `Daily` / `Weekly` / `Bi-weekly` / `Monthly` / `Ad hoc` (only relevant if Recurring = checked) |
| **Satisfaction Rating** | Select | Post-meeting self-rating: `⭐ Poor` / `⭐⭐ Fair` / `⭐⭐⭐ Good` / `⭐⭐⭐⭐ Great` |
| **Created By** | Created by | Auto-filled Notion user who created the record |
| **Last Edited** | Last edited time | Auto-updated timestamp |

---

### Database 2: ✅ Action Items

**Purpose**: Tracks every task, commitment, or follow-up generated from meetings. This is the accountability engine of the template.

| Column Name | Data Type | Description |
|---|---|---|
| **Action Item** | Title | Clear, verb-first description of the task (e.g., "Draft proposal for client X") |
| **Source Meeting** | Relation → Meetings DB | The meeting where this action item was created |
| **Owner** | Relation → People DB | The single person responsible for completing this task |
| **Due Date** | Date | Deadline for completion |
| **Priority** | Select | Options: `🔴 High` / `🟡 Medium` / `🟢 Low` |
| **Status** | Select | Options: `Not Started` / `In Progress` / `Blocked` / `Done` / `Cancelled` |
| **Done?** | Checkbox | Quick toggle; syncs with Status logic |
| **Days Until Due** | Formula | `dateBetween(prop("Due Date"), now(), "days")` — shows urgency |
| **Overdue?** | Formula | `if(prop("Due Date") < now() and prop("Done?") == false, true, false)` |
| **Project / Team** | Relation → Projects & Teams DB | Optionally links to a project for cross-project action tracking |
| **Notes / Context** | Text (rich text) | Background or clarifying information for the assignee |
| **Completion Date** | Date | Actual date the task was marked done |
| **Completion Notes** | Text (rich text) | Brief note on outcome or any blockers encountered |
| **Tags** | Multi-select | e.g., `Needs Approval`, `External Dependency`, `Waiting On`, `Quick Win` |
| **Created Date** | Created time | Auto-filled when the record is created |

---

### Database 3: 👤 People

**Purpose**: A directory of all meeting participants — team members, stakeholders, or external contacts. Centralizes attendee management across all meetings.

| Column Name | Data Type | Description |
|---|---|---|
| **Full Name** | Title | Person's full name |
| **Role / Title** | Text | Job title or role (e.g., "Senior Engineer", "Client Sponsor") |
| **Team / Department** | Select | Options: `Engineering` / `Design` / `Marketing` / `Sales` / `Leadership` / `External` / `HR` / `Finance` |
| **Email** | Email | Work email address for follow-up correspondence |
| **Meetings Attended** | Relation → Meetings DB (bidirectional) | All meetings this person has been linked to |
| **Actions Owned** | Relation → Action Items DB (bidirectional) | All action items assigned to this person |
| **Total Meetings** | Rollup | Count of Meetings Attended (Count All) |
| **Open Actions** | Rollup | Count of Actions Owned where Status ≠ `Done` |
| **Facilitator For** | Rollup | Count of meetings where this person is listed as Facilitator |
| **Notion User** | Person | Links to actual Notion workspace member (for @mention and notifications) |
| **Active?** | Checkbox | Uncheck to archive people who have left the team |
| **Notes** | Text (rich text) | Any relevant context (e.g., time zone, communication preferences) |

---

### Database 4: 🗂️ Projects & Teams

**Purpose**: Organizes meetings and actions by project or team context, enabling cross-functional visibility and project-level rollups.

| Column Name | Data Type | Description |
|---|---|---|
| **Project / Team Name** | Title | Name of the project or team (e.g., "Website Redesign", "Engineering Team") |
| **Type** | Select | Options: `Project` / `Team` / `Department` / `Client` |
| **Status** | Select | Options: `Active` / `On Hold` / `Completed` / `Archived` |
| **Lead / Owner** | Relation → People DB | The DRI (directly responsible individual) for this project/team |
| **Start Date** | Date | Project kick-off or team formation date |
| **End Date** | Date | Expected or actual completion date |
| **Meetings** | Relation → Meetings DB (bidirectional) | All meetings associated with this project/team |
| **Action Items** | Relation → Action Items DB (bidirectional) | All tasks linked to this project/team |
| **Total Meetings** | Rollup | Count of all linked meetings |
| **Open Action Items** | Rollup | Count of linked action items where Status ≠ `Done` |
| **Total Action Items** | Rollup | Count of all linked action items |
| **Description** | Text (rich text) | Brief description of the project scope or team purpose |
| **Color / Icon** | Select | Optional visual label for dashboard views: `🔵 Blue` / `🟢 Green` / `🟠 Orange` / `🔴 Red` / `🟣 Purple` |

---

### Database 5: 📋 Meeting Templates (Agenda Templates)

**Purpose**: A reusable library of agenda and note structures for recurring meeting types, reducing the time to prepare for common meetings.

| Column Name | Data Type | Description |
|---|---|---|
| **Template Name** | Title | Name of the template (e.g., "Weekly Standup", "Sprint Retrospective") |
| **Meeting Type** | Select | Mirrors Meeting Type options from Meetings DB |
| **Agenda Structure** | Text (rich text) | Pre-built agenda with section headers, time blocks, and prompt questions |
| **Note-Taking Structure** | Text (rich text) | Pre-built notes skeleton (e.g., headers for Decisions, Blockers, Next Steps) |
| **Typical Duration (min)** | Number | Suggested meeting length in minutes |
| **Recommended Attendees** | Text | Description of who should typically attend |
| **Tips & Best Practices** | Text (rich text) | Facilitator notes and guidance for running this type of meeting effectively |
| **Use Count** | Number | Manually track or note how often this template has been used |
| **Last Updated** | Last edited time | Auto-updated when template content changes |

---

## 3. Page Structure

```
📁 Meeting Notes (Top-Level Workspace Page)
│
├── 🏠 Dashboard (Home Page)
│   ├── [Linked View] Upcoming Meetings — Calendar View (Meetings DB, filtered: Status = Scheduled, Date ≥ Today)
│   ├── [Linked View] My Open Action Items — Table View (Action Items DB, filtered: Owner = Me, Status ≠ Done)
│   ├── [Linked View] Recent Meetings — Gallery View (Meetings DB, sorted: Date descending, limit 6)
│   ├── [Linked View] Overdue Actions — Table View (Action Items DB, filtered: Overdue? = true)
│   └── Quick Stats (Callout blocks): Total Meetings This Month | Open Actions | Meetings This Week
│
├── 📅 All Meetings (Sub-Page)
│   ├── [Full Database] Meetings DB — Table View (primary view, all columns visible)
│   ├── [View] Board View — grouped by Status
│   ├── [View] Calendar View — by Date & Time
│   ├── [View] By Project — grouped by Project / Team
│   ├── [View] By Meeting Type — grouped by Meeting Type
│   └── [View] This Week — filtered: Date between Monday and Sunday of current week
│
├── ✅ Action Tracker (Sub-Page)
│   ├── [Full Database] Action Items DB — Table View (primary view)
│   ├── [View] My Actions — filtered: Owner = Me
│   ├── [View] Board View — grouped by Status
│   ├── [View] By Owner — grouped by Owner
│   ├── [View] Overdue — filtered: Overdue? = true, sorted by Due Date ascending
│   ├── [View] High Priority — filtered: Priority = High
│   └── [View] Completed — filtered: Status = Done, sorted by Completion Date descending
│
├── 👥 People Directory (Sub-Page)
│   ├── [Full Database] People DB — Table View
│   ├── [View] Gallery View — showing name, role, open actions count
│   └── [View] Active Members Only — filtered: Active? = checked
│
├── 🗂️ Projects & Teams (Sub-Page)
│   ├── [Full Database] Projects & Teams DB — Table View
│   ├── [View] Active Projects — filtered: Status = Active
│   ├── [View] Board View — grouped by Status
│   └── [View] By Type — grouped by Type
│
├── 📋 Agenda Templates (Sub-Page)
│   ├── [Full Database] Meeting Templates DB — Gallery View (primary view)
│   ├── [View] Table View — for editing and managing templates
│   └── [View] By Meeting Type — grouped by Meeting Type
│
├── 📊 Analytics & Insights (Sub-Page)
│   ├── [Linked View] Meetings Per Month — Table View (Meetings DB, grouped by month)
│   ├── [Linked View] Action Item Completion Rate — Table View (Action Items DB, grouped by Status)
│   ├── [Linked View] Most Active Projects — sorted by Total Meetings descending
│   ├── [Linked View] Top Action Item Owners — People DB, sorted by Open Actions descending
│   └── Explanatory text blocks with interpretation guidance
│
└── 📖 How to Use This Template (Sub-Page)
    ├── Getting Started (3 Steps)
    ├── Database Relationship Diagram (image or visual)
    ├── FAQ block
    └── Changelog / Version notes
```

### Relationship Diagram Summary

```
Meetings DB ←——→ Projects & Teams DB
     ↕                    ↕
Action Items DB ←——→ Projects & Teams DB
     ↕
  People DB ←——→ Meetings DB
```

---

## 4. Getting-Started Flow (3 Steps)

---

### ✅ Step 1: Set Up Your People and Projects

> **Goal**: Populate the two foundation databases before logging any meetings.

1. Navigate to the **👥 People Directory** sub-page and open the `People` database.
2. Add a row for every person who will regularly attend or facilitate meetings — include yourself first. Fill in their **Full Name**, **Role / Title**, **Team / Department**, and **Email**. If they are a Notion workspace member, connect them in the **Notion User** column so they receive @mention notifications.
3. Next, go to the **🗂️ Projects & Teams** sub-page and create a row for each active project or team you'll be tracking. Give it a clear name (e.g., `Product Launch Q4`), set its **Type** (Project or Team), set **Status** to `Active`, and assign a **Lead / Owner** by linking to a person you just created.

> **Why first?** Every meeting and action item will reference these two databases via Relations. Populating them upfront avoids empty dropdowns and broken links later.

---

### 📅 Step 2: Log Your First Meeting

> **Goal**: Create a meeting record before or during your next meeting.

1. Go to the **📅 All Meetings** sub-page and click `+ New` to create a new row in the Meetings database.
2. Fill in the essential fields:
   - **Meeting Title** — be specific (e.g., "Product Team Weekly Sync — Oct 14")
   - **Date & Time** and **End Time** — the Duration formula will auto-calculate
   - **Meeting Type** — select the closest match (e.g., `Standup