# Notion Template Design Specification

**Theme:** Project Management

---

# Notion Project Management Template — Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Modern teams and freelancers struggle with project visibility — tasks fall through the cracks, deadlines are missed, and stakeholders lack a single source of truth. Existing tools are either too complex (Jira, Asana) or too simple (basic to-do lists). This Notion template bridges that gap by providing a **structured yet flexible project management system** that tracks projects, tasks, milestones, team members, and meeting notes — all within a single, interconnected workspace.

### Primary Use Cases

| Use Case | Description |
|---|---|
| **Multi-project tracking** | Manage several concurrent projects without losing context |
| **Team task delegation** | Assign tasks to team members and track ownership |
| **Deadline & milestone management** | Visualize timelines and critical due dates |
| **Client-facing reporting** | Generate clean status snapshots for stakeholders |
| **Sprint / weekly planning** | Plan work in focused cycles with clear priorities |
| **Meeting documentation** | Log decisions and action items tied to specific projects |

### Target User Persona

---

**Persona 1 — "The Busy Team Lead"**
- **Name:** Sarah, 34
- **Role:** Product Manager at a 30-person SaaS startup
- **Goals:** Keep 3–5 simultaneous projects on track, align engineers and designers, and report weekly status to the VP
- **Pain Points:** Context-switching between Slack, email, and spreadsheets; no single view of all project health; manual status updates to leadership
- **Notion Proficiency:** Intermediate — uses Notion daily but has not built relational databases before

---

**Persona 2 — "The Freelance Consultant"**
- **Name:** Marcus, 28
- **Role:** Independent UX/brand consultant managing 6–10 active clients
- **Goals:** Track deliverables per client, log hours, send status updates, never miss a deadline
- **Pain Points:** Clients ask "where are we?" too often; invoicing is disconnected from actual task completion; project scope creep
- **Notion Proficiency:** Beginner-to-intermediate — prefers drag-and-drop setup, minimal configuration

---

**Persona 3 — "The Agency Operations Manager"**
- **Name:** Priya, 42
- **Role:** Operations lead at a 12-person creative agency
- **Goals:** Standardize how all projects are kicked off, tracked, and closed; reduce onboarding time for new project managers
- **Pain Points:** Every PM uses a different system; no historical record of past projects for reference; resource allocation is invisible
- **Notion Proficiency:** Advanced — comfortable with formulas, rollups, and linked databases

---

## 2. Notion Database List and Column Definitions

### Database 1 — `📁 Projects`

**Purpose:** The master registry of every project. All other databases relate back to this one. Provides a bird's-eye health view of the entire portfolio.

| Column Name | Data Type | Description |
|---|---|---|
| `Project Name` | **Title** | The full name of the project (e.g., "Website Redesign Q3") |
| `Status` | **Select** | Current state: `🔵 Planning` / `🟡 In Progress` / `🟠 On Hold` / `🟢 Completed` / `🔴 Cancelled` |
| `Priority` | **Select** | `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🟢 Low` |
| `Project Type` | **Select** | `Product` / `Marketing` / `Design` / `Engineering` / `Operations` / `Client Work` |
| `Owner` | **Person** | The primary accountable individual for the project |
| `Team Members` | **Person** | All contributors working on the project |
| `Client / Stakeholder` | **Text** | Name of the client or internal stakeholder group |
| `Start Date` | **Date** | Official project kick-off date |
| `Target End Date` | **Date** | Planned completion date |
| `Actual End Date` | **Date** | Date the project was formally closed |
| `Budget (USD)` | **Number** | Total approved budget in US dollars |
| `Spent (USD)` | **Rollup** | Auto-sum of all `Cost` values from linked Tasks (Rollup → Tasks → Cost → Sum) |
| `Budget Remaining` | **Formula** | `prop("Budget (USD)") - prop("Spent (USD)")` |
| `% Complete` | **Formula** | `round(prop("Tasks Done") / max(prop("Total Tasks"), 1) * 100)` — shown as a percentage |
| `Total Tasks` | **Rollup** | Count of all related tasks (Rollup → Tasks → Task Name → Count All) |
| `Tasks Done` | **Rollup** | Count of tasks where Status = Done (Rollup → Tasks → Status → Count Values filtered) |
| `Open Risks` | **Rollup** | Count of linked Risks with Status = `Open` |
| `Description` | **Text** | Brief scope statement, objectives, and success criteria |
| `Project Brief URL` | **URL** | Link to full brief, SOW, or PRD document |
| `Tags` | **Multi-select** | Freeform labels: `Q1` / `Q2` / `Q3` / `Q4` / `Urgent` / `External` / `Internal` |
| `Health` | **Select** | Manual RAG status: `🟢 On Track` / `🟡 At Risk` / `🔴 Off Track` |
| `Related Milestones` | **Relation** | Links to `🏁 Milestones` database |
| `Related Tasks` | **Relation** | Links to `✅ Tasks` database |
| `Related Meeting Notes` | **Relation** | Links to `📝 Meeting Notes` database |
| `Related Risks` | **Relation** | Links to `⚠️ Risks & Issues` database |

---

### Database 2 — `✅ Tasks`

**Purpose:** The operational heartbeat of the template. Every piece of work — large or small — is logged here, assigned to a team member, and tied to a parent project.

| Column Name | Data Type | Description |
|---|---|---|
| `Task Name` | **Title** | Short, action-oriented description (e.g., "Design homepage wireframes") |
| `Project` | **Relation** | Links to `📁 Projects` — every task must belong to a project |
| `Milestone` | **Relation** | Optional link to `🏁 Milestones` — marks this task as part of a milestone |
| `Assigned To` | **Person** | The single owner responsible for completing this task |
| `Status` | **Select** | `📋 Backlog` / `🔜 To Do` / `⚙️ In Progress` / `👀 In Review` / `✅ Done` / `🚫 Blocked` |
| `Priority` | **Select** | `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🟢 Low` |
| `Due Date` | **Date** | Deadline for task completion |
| `Start Date` | **Date** | When work on this task should begin |
| `Estimated Hours` | **Number** | Planned effort in hours |
| `Actual Hours` | **Number** | Actual hours logged upon completion |
| `Cost` | **Formula** | `prop("Actual Hours") * prop("Hourly Rate")` — feeds into Project budget rollup |
| `Hourly Rate` | **Number** | Rate per hour for this task (can reflect contractor or internal rate) |
| `Task Type` | **Select** | `Design` / `Development` / `Research` / `Writing` / `Review` / `Meeting` / `Admin` |
| `Sprint / Week` | **Select** | Sprint label or week identifier for planning cycles (e.g., `Sprint 1`, `Week 12`) |
| `Blocked By` | **Relation** | Self-referential relation — links to another Task that is blocking this one |
| `Blocking` | **Relation** | Self-referential relation — tasks this one is currently blocking |
| `Completed On` | **Date** | Actual date the task was marked Done |
| `Notes` | **Text** | Context, links to files, or additional instructions |
| `Checkbox: Done?` | **Checkbox** | Quick toggle — when checked, auto-reflects in project rollup |
| `Days Overdue` | **Formula** | `if(prop("Status") != "✅ Done" and prop("Due Date") < now(), dateBetween(now(), prop("Due Date"), "days"), 0)` |

---

### Database 3 — `🏁 Milestones`

**Purpose:** Captures the major checkpoints within a project. Milestones are not tasks themselves — they represent significant deliverable moments (e.g., "Phase 1 Complete," "Client Approval Received").

| Column Name | Data Type | Description |
|---|---|---|
| `Milestone Name` | **Title** | Clear, outcome-oriented name (e.g., "Beta Launch Ready") |
| `Project` | **Relation** | Links to `📁 Projects` |
| `Target Date` | **Date** | When this milestone must be achieved |
| `Status` | **Select** | `⏳ Upcoming` / `🔄 In Progress` / `✅ Achieved` / `❌ Missed` |
| `Owner` | **Person** | Accountable person for this milestone |
| `Related Tasks` | **Relation** | All tasks that must be completed to reach this milestone |
| `Tasks Complete` | **Rollup** | Count of related tasks with Status = Done |
| `Total Tasks` | **Rollup** | Total count of related tasks |
| `Completion %` | **Formula** | `round(prop("Tasks Complete") / max(prop("Total Tasks"), 1) * 100)` |
| `Deliverable Description` | **Text** | What must exist or be true for this milestone to be considered achieved |
| `Approved By` | **Person** | Stakeholder who signs off on milestone completion |
| `Approval Date` | **Date** | Date formal approval was received |
| `Notes` | **Text** | Blockers, decisions, or context relevant to this milestone |

---

### Database 4 — `👥 Team Members`

**Purpose:** A directory of all people involved across projects. Enables resource allocation views and workload balancing. Relates to tasks and projects for rollup insights.

| Column Name | Data Type | Description |
|---|---|---|
| `Name` | **Title** | Full name of the team member |
| `Notion User` | **Person** | Linked Notion account for @mention functionality |
| `Role` | **Select** | `Project Manager` / `Designer` / `Developer` / `Copywriter` / `Analyst` / `Client` / `Stakeholder` / `Consultant` |
| `Department` | **Select** | `Engineering` / `Design` / `Marketing` / `Operations` / `Finance` / `External` |
| `Email` | **Email** | Work email address |
| `Availability` | **Select** | `Full-time` / `Part-time` / `Contractor` / `On Leave` |
| `Hourly Rate (USD)` | **Number** | Standard billing or cost rate per hour |
| `Active Projects` | **Relation** | Links to `📁 Projects` this person is contributing to |
| `Assigned Tasks` | **Relation** | Links to `✅ Tasks` assigned to this person |
| `Total Tasks Assigned` | **Rollup** | Count of all assigned tasks |
| `Tasks Completed` | **Rollup** | Count of assigned tasks with Status = Done |
| `Completion Rate` | **Formula** | `round(prop("Tasks Completed") / max(prop("Total Tasks Assigned"), 1) * 100)` shown as `%` |
| `Skills` | **Multi-select** | e.g., `Figma` / `React` / `SEO` / `Copywriting` / `Data Analysis` |
| `Start Date` | **Date** | Date they joined the team or engagement |
| `Notes` | **Text** | Relevant context, contractual notes, preferences |

---

### Database 5 — `📝 Meeting Notes`

**Purpose:** Centralizes all project-related meeting records. Ensures decisions and action items are never lost and are traceable back to their originating project.

| Column Name | Data Type | Description |
|---|---|---|
| `Meeting Title` | **Title** | Descriptive name (e.g., "Sprint 3 Kickoff — Mobile App") |
| `Project` | **Relation** | Links to `📁 Projects` |
| `Meeting Date` | **Date** | Date and time the meeting took place (include time) |
| `Meeting Type` | **Select** | `Kickoff` / `Status Update` / `Retrospective` / `Client Check-in` / `Planning` / `Ad Hoc` |
| `Attendees` | **Person** | All people present at the meeting |
| `Facilitator` | **Person** | Who ran the meeting |
| `Agenda` | **Text** | Pre-meeting agenda items |
| `Key Decisions` | **Text** | Bullet list of decisions made during the meeting |
| `Action Items` | **Text** | Specific next steps with owner names and due dates noted inline |
| `Action Item Tasks` | **Relation** | Links to `✅ Tasks` created as a result of this meeting |
| `Recording URL` | **URL** | Link to Zoom/Loom/Google Meet recording |
| `Transcript URL` | **URL** | Link to auto-generated transcript (e.g., Otter.ai) |
| `Follow-up Required?` | **Checkbox** | Flags this meeting as needing a follow-up meeting |
| `Follow-up Date` | **Date** | Scheduled date of the next meeting if follow-up is needed |
| `Sentiment` | **Select** | Team mood indicator: `😊 Positive` / `😐 Neutral` / `😟 Concerned` |

---

### Database 6 — `⚠️ Risks & Issues`

**Purpose:** Proactive risk tracking and issue logging to prevent surprises. Separates identified risks (potential future problems) from active issues (current problems).

| Column Name | Data Type | Description |
|---|---|---|
| `Risk / Issue Name` | **Title** | Clear description (e.g., "Key developer unavailable in Week 8") |
| `Type` | **Select** | `⚠️ Risk` (future threat) / `🔥 Issue` (current problem) |
| `Project` | **Relation** | Links to `📁 Projects` |
| `Status` | **Select** | `Open` / `Monitoring` / `Mitigated` / `Resolved` / `Accepted` |
| `Severity` | **Select** | `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🟢 Low` |
| `Probability` | **Select** | `Very Likely` / `Likely` / `Possible` / `Unlikely` — for Risks only |
| `Risk Score` | **Formula** | Maps Severity × Probability to a numeric score for prioritization |
| `Owner` | **Person** | Person responsible for monitoring or resolving this item |
| `Date Identified` | **Date** | When this risk or issue was first logged |
| `Target Resolution Date` | **Date** | Deadline for resolution or mitigation |
| `Mitigation Plan` | **Text** | Steps being taken to reduce likelihood or impact |
| `Contingency Plan` | **Text** | Backup plan if the risk materializes |
| `Impact Description` | **Text** | What happens to the project if this is not addressed |
| `Related Tasks` | **Relation** | Links to `✅ Tasks` created to address this risk/issue |
| `Resolved On` | **Date** | Date the item was formally closed |

---

## 3. Page Structure

```
📊 PROJECT HUB (Top-Level Dashboard Page)
│
├── 🏠 Dashboard                          ← Main landing page with linked views
│   ├── [View] All Projects — Gallery     (from 📁 Projects)
│   ├── [View] My Open Tasks — Board      (from ✅ Tasks, filtered by Assigned = Me)
│   ├── [View] Upcoming Milestones        (from 🏁 Milestones, next 30 days)
│   ├──