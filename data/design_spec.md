# Notion Template Design Specification

**Theme:** Habit Tracker

---

# Habit Tracker — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most people struggle to build lasting habits because they lack a **centralized, visual system** that connects daily check-ins with long-term progress. Generic to-do apps treat habits like one-time tasks, and paper trackers are quickly abandoned. This template solves three core problems:

1. **Inconsistency** — No clear daily ritual or prompt to check in
2. **Lack of insight** — No way to see patterns, streaks, or correlation between habits
3. **Overwhelm** — Trying to track too many habits with no prioritization framework

### Primary Use Cases

| Use Case | Description |
|---|---|
| Daily habit logging | Check off habits each day with optional notes |
| Weekly review | Reflect on completion rates and adjust goals |
| Habit goal setting | Define habits with target frequency and category |
| Streak tracking | Visualize consecutive days of completion |
| Habit analytics | Identify which habits are thriving vs. slipping |
| Category-based tracking | Separate health, work, relationships, and mindset habits |

### Detailed Target User Persona

---

**Persona 1 — "The Rebuilder" (Primary)**

> *"I've tried every habit app and quit after two weeks. I need something I actually own."*

- **Name:** Alex, 32
- **Occupation:** Mid-level marketing manager, hybrid work schedule
- **Tech comfort:** Intermediate Notion user (uses it for work notes)
- **Goals:** Build consistent morning routine, exercise 4×/week, read 20 min daily
- **Pain points:** Forgets to log at end of day, doesn't know which habits to prioritize, feels guilt when streaks break
- **Behavior:** Checks Notion every morning at 9 AM, prefers visual dashboards over raw tables

---

**Persona 2 — "The Optimizer" (Secondary)**

> *"I track everything. I want data on my habits, not just checkboxes."*

- **Name:** Priya, 27
- **Occupation:** Software developer, fully remote
- **Tech comfort:** Advanced Notion user (builds her own templates)
- **Goals:** Track 8–12 habits across multiple life domains, analyze weekly trends, correlate sleep with productivity
- **Pain points:** Existing templates aren't flexible enough, rollups break, no formula for streaks
- **Behavior:** Does a thorough Sunday weekly review, wants export-friendly data structure

---

**Persona 3 — "The Beginner" (Tertiary)**

> *"I've never tracked habits before. I want something simple to start."*

- **Name:** Jordan, 21
- **Occupation:** University student
- **Tech comfort:** Basic Notion user (uses it for notes only)
- **Goals:** Study daily, drink more water, sleep by midnight
- **Pain points:** Intimidated by complex templates, doesn't know what habits to build
- **Behavior:** Uses Notion on mobile, needs a clean one-page experience

---

## 2. Notion Database List and Column Definitions

### Database 1: 📋 Habit Library

**Purpose:** The master list of all habits the user wants to track. Each habit is defined once here and referenced in daily logs. This is the "source of truth" for what habits exist, their goals, categories, and active status.

| Column Name | Data Type | Description |
|---|---|---|
| Habit Name | Title | The name of the habit (e.g., "Morning Run", "Read 20 min") |
| Category | Select | Life domain: `🏃 Health`, `🧠 Mindset`, `💼 Work`, `🤝 Relationships`, `💰 Finance`, `🎨 Creative` |
| Target Frequency | Select | How often the habit should occur: `Daily`, `5×/week`, `3×/week`, `Weekly` |
| Habit Type | Select | `Build` (adding a positive behavior) or `Break` (stopping a negative one) |
| Why (Motivation) | Text | A short personal note explaining why this habit matters to the user |
| Cue | Text | The trigger or context for doing this habit (e.g., "After morning coffee") |
| Difficulty | Select | `🟢 Easy`, `🟡 Medium`, `🔴 Hard` — used to balance habit stack |
| Active | Checkbox | If checked, this habit appears in daily logs; uncheck to archive without deleting |
| Icon | Text | A single emoji the user picks to represent the habit visually (e.g., 🏃) |
| Start Date | Date | The date the user committed to this habit |
| Total Completions | Rollup | Counts all related `✅` entries in the Daily Log database |
| Current Streak | Formula | *(See formula note below)* Calculates consecutive days logged |
| Completion Rate (30d) | Formula | `Total Completions in last 30 days / 30 × 100` — expressed as a percentage |
| Linked Daily Logs | Relation | One-to-many relation to the **Daily Log** database |
| Notes | Text | Any general notes, adaptations, or reference resources |

> **Formula Note — Current Streak:** Because Notion formulas cannot directly query dates across related records, the streak field will display a manual-entry number updated during the weekly review OR use a simplified formula based on the most recent log entry date: `if(dateBetween(now(), prop("Last Completed"), "days") <= 1, prop("Streak Days"), 0)`. The `Streak Days` and `Last Completed` columns below support this.

| Column Name | Data Type | Description |
|---|---|---|
| Last Completed | Date | Manually or via automation updated to the most recent completion date |
| Streak Days | Number | Current streak count (manually updated or via Zapier/Make automation) |

---

### Database 2: 📅 Daily Log

**Purpose:** The workhorse of the template. Every day, a new entry is created (or auto-generated via template button) for each active habit. This is where users actually check off their habits and leave notes about that specific day's performance.

| Column Name | Data Type | Description |
|---|---|---|
| Log Entry Name | Title | Auto-formatted as `[Habit Icon] [Habit Name] — [Date]` e.g., "🏃 Morning Run — 2025-07-14" |
| Date | Date | The calendar date for this log entry |
| Habit | Relation | Links to the corresponding habit in the **Habit Library** |
| Habit Category | Rollup | Pulls `Category` from the related Habit Library entry (display only) |
| Completed | Checkbox | Core interaction — user checks this off when habit is done |
| Completion Time | Select | When the habit was done: `Morning`, `Afternoon`, `Evening`, `Night` |
| Quality | Select | Subjective rating: `⭐ Poor`, `⭐⭐ Okay`, `⭐⭐⭐ Good`, `⭐⭐⭐⭐ Great` |
| Duration (min) | Number | Optional — how many minutes the habit took (useful for exercise, reading, etc.) |
| Notes / Reflection | Text | Free-form note about this specific session (e.g., "Ran 3km, felt tired but pushed through") |
| Mood Before | Select | Emotional state before the habit: `😔 Low`, `😐 Neutral`, `😊 Good`, `🤩 Energized` |
| Mood After | Select | Emotional state after the habit — compare with Mood Before to identify patterns |
| Skipped Reason | Select | If not completed: `Sick`, `Travel`, `Forgot`, `No Time`, `Chose to Skip`, `Other` |
| Week Number | Formula | `formatDate(prop("Date"), "W")` — used to group logs by week in views |
| Day of Week | Formula | `formatDate(prop("Date"), "ddd")` — Mon/Tue/Wed etc. for pattern analysis |
| Month | Formula | `formatDate(prop("Date"), "MMMM YYYY")` — used for monthly rollup views |

---

### Database 3: 📆 Weekly Review

**Purpose:** Once per week (recommended: every Sunday), the user creates a weekly review entry. This database aggregates the week's performance, captures reflections, and sets intentions for the next week. It serves as the "meta-layer" above daily logging.

| Column Name | Data Type | Description |
|---|---|---|
| Review Title | Title | Auto-named as `Week [#] Review — [Date Range]` e.g., "Week 28 Review — Jul 7–13, 2025" |
| Week Start Date | Date | The Monday of the review week |
| Week End Date | Date | The Sunday of the review week |
| Overall Completion Rate | Number | User manually enters or calculates: `habits completed / habits possible × 100` |
| Energy Level (Avg) | Select | Average energy felt during the week: `Low`, `Medium`, `High` |
| Top Win | Text | The single biggest habit success of the week |
| Biggest Challenge | Text | The habit or situation that was hardest to navigate |
| What Worked | Text | Specific tactics, environments, or cues that helped |
| What Didn't Work | Text | Friction points, obstacles, or patterns to address |
| Habit Adjustments | Text | Any changes to make: habits to pause, modify, or intensify |
| Intentions for Next Week | Text | 2–3 specific focus areas or mini-goals for the coming week |
| Rating (1–10) | Number | Subjective overall rating of the week (1 = terrible, 10 = perfect) |
| Linked Daily Logs | Relation | Optional: manually link that week's Daily Log entries for reference |
| Mood Trend | Select | Overall emotional tone of the week: `📉 Declining`, `➡️ Stable`, `📈 Improving` |
| Habit Count (Active) | Number | How many habits were actively tracked this week |

---

### Database 4: 🎯 Habit Goals & Milestones

**Purpose:** Long-term goal tracking. Users set milestone targets for each habit (e.g., "Complete 30-day challenge", "Reach a 60-day streak") and mark them as achieved. This provides motivational checkpoints beyond daily/weekly tracking.

| Column Name | Data Type | Description |
|---|---|---|
| Milestone Name | Title | The goal name, e.g., "30-Day No Sugar Challenge" or "100 Meditations" |
| Related Habit | Relation | Links to the **Habit Library** |
| Milestone Type | Select | `Streak Goal`, `Total Count`, `Duration Challenge`, `Custom` |
| Target Number | Number | The quantitative goal (e.g., 30 for a 30-day streak, 100 for 100 completions) |
| Current Progress | Rollup | Pulls total completions from Daily Log via Habit Library relation |
| Progress % | Formula | `round(prop("Current Progress") / prop("Target Number") * 100)` |
| Target Date | Date | Deadline for achieving this milestone |
| Achieved | Checkbox | Mark when the milestone is completed |
| Date Achieved | Date | When it was accomplished — useful for celebrating wins |
| Reward | Text | What the user promises themselves when they hit this milestone (optional but motivating) |
| Notes | Text | Any context about this goal |

---

## 3. Page Structure

### Full Page Hierarchy

```
🏠 Habit Tracker [Top-Level Dashboard]
│
├── 📊 Dashboard (Main View)
│   ├── [Gallery View] — Today's Habits
│   ├── [Progress Bars] — Active Habit Streaks
│   ├── [Linked View] — This Week at a Glance
│   └── [Callout Block] — Daily Intention / Quote
│
├── 📋 Habit Library [Database Page]
│   ├── View: All Active Habits (Table)
│   ├── View: By Category (Board)
│   ├── View: By Difficulty (Gallery)
│   └── View: Archived Habits (Table, filtered: Active = false)
│
├── 📅 Daily Log [Database Page]
│   ├── View: Today (Filter: Date = Today)
│   ├── View: This Week (Filter: Week Number = current)
│   ├── View: Calendar View (Full month calendar)
│   ├── View: Completed Today (Filter: Date = Today, Completed = true)
│   └── View: Missed This Week (Filter: Week = current, Completed = false)
│
├── 📆 Weekly Reviews [Database Page]
│   ├── View: All Reviews (Table, sorted by Week Start Date desc)
│   ├── View: Current Week (Filter: Week Start = current week)
│   └── View: Gallery (Card view with rating and mood)
│
├── 🎯 Goals & Milestones [Database Page]
│   ├── View: Active Goals (Filter: Achieved = false)
│   ├── View: Achieved (Filter: Achieved = true)
│   └── View: By Habit (Board grouped by Related Habit)
│
├── 📖 Habit Resources [Static Sub-page]
│   ├── [Section] Habit Stacking Guide
│   ├── [Section] The 2-Minute Rule Explained
│   ├── [Section] Recommended Reading List
│   └── [Section] Template Instructions
│
└── ⚙️ Settings & Setup [Static Sub-page]
    ├── [Template Buttons] — Create Today's Log Entries
    ├── [Instructions] How to Add a New Habit
    ├── [Instructions] How to Archive a Habit
    └── [Instructions] Weekly Review Workflow
```

---

### Dashboard Layout Detail

The **Dashboard** is the homepage and the page users see every time they open the template. It is a **regular Notion page** (not a database) composed of linked database views and visual blocks.

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 HABIT TRACKER                          [Date: Today]     │
│  "Small steps. Big life."                                    │
├─────────────────────────────────────────────────────────────┤
│  ✨ DAILY INTENTION                                          │
│  [Callout block — editable each morning]                    │
├──────────────────────────┬──────────────────────────────────┤
│  ✅ TODAY'S HABITS        │  📈 STREAK LEADERS               │
│  [Linked DB: Daily Log]  │  [Linked DB: Habit Library]      │
│  Filter: Date = Today    │  Sorted by Streak Days desc      │
│  View: Gallery/Checklist │  View: Table (Name, Streak, Cat) │
├──────────────────────────┴──────────────────────────────────┤
│  📅 THIS WEEK AT A GLANCE                                   │
│  [Linked DB: Daily Log]                                     │
│  Filter: Week = Current | View: Board grouped by Day        │
├──────────────────────────┬──────────────────────────────────┤
│  🎯 ACTIVE MILESTONES    │  📝 LATEST WEEKLY REVIEW         │
│  [Linked DB: Goals]      │  [Linked DB: Weekly Reviews]     │
│  Filter: Achieved = No   │  Filter: 1 most recent entry     │
│  View: List w/ progress  │  View: Single card preview       │
└──────────────────────────┴──────────────────────────────────┘
```

---

### Database Placement Summary

| Database | Lives At | Primary Entry Point |
|---|---|---|
| Habit Library | `/Habit Library` sub-page | Dashboard → "Today's Habits" view |
| Daily Log | `/Daily Log` sub-page | Dashboard → Daily Habits section |
| Weekly Reviews | `/Weekly Reviews` sub-page | Dashboard → Latest Review section |
| Goals & Milestones | `/Goals & Milestones` sub-page | Dashboard → Active Milestones section |

All databases are also **linked** (not embedded) in the Dashboard to preserve clean navigation without duplicating data.

---

## 4. Getting-Started Flow (3 Steps)

---

### ✅ Step 1: Define Your Habits in the Habit Library *(~10 minutes)*

Navigate to the **📋 Habit Library** page. This is where you build the foundation of your tracker.

1. Click **"+ New"** to create your first habit
2. Fill in the following fields for each habit:
   - **Habit Name** — Be specific: *"Read fiction