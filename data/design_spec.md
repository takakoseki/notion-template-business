# Notion Template Design Specification

**Theme:** Habit Tracker

---

# Habit Tracker — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most people struggle to build consistent habits because they lack a **centralized, visual system** that simultaneously tracks daily check-ins, measures long-term progress, reflects on wins and failures, and adjusts goals over time. Generic to-do apps treat habits like tasks — one-and-done. This template treats habits as ongoing behavioral systems that require **streaks, context, reflection, and analytics** working together in one place.

### Primary Use Cases

| Use Case | Description |
|---|---|
| **Daily habit logging** | Check off habits each day with optional notes and mood tags |
| **Streak tracking** | Automatically calculate current and best streaks per habit |
| **Weekly reviews** | Reflect on the past week — what worked, what didn't |
| **Habit library management** | Store, categorize, and archive habits with goals and triggers |
| **Progress analytics** | View completion rates, trend charts, and category breakdowns |
| **Goal-to-habit mapping** | Link each habit to a higher-level life goal |

### Target User Persona

---

**Primary Persona: "The Intentional Improver"**

> *"I know what I want to change about myself, but I always lose momentum after two weeks."*

- **Name:** Alex, 28–38 years old
- **Occupation:** Knowledge worker, freelancer, student, or entrepreneur
- **Tech comfort:** Intermediate Notion user — comfortable with databases and filtered views, but not a formula expert
- **Goals:**
  - Build 3–7 sustainable daily habits (exercise, reading, journaling, hydration, etc.)
  - Reduce decision fatigue around self-improvement routines
  - Have a single "home base" for personal development without switching between apps
- **Pain points:**
  - Starts strong in habit apps but abandons them within weeks
  - Can't see *why* habits are failing — missing reflection layer
  - Uses multiple disconnected tools (spreadsheets, sticky notes, phone apps)
- **Behavior patterns:**
  - Does a Sunday evening planning ritual
  - Motivated by visual streaks and completion percentages
  - Prefers minimal friction for daily check-ins (30 seconds or less)

---

**Secondary Persona: "The Wellness Coach Client"**

- A person in a coaching program who needs to report habit compliance weekly to an accountability partner or coach
- Uses the Weekly Review page to export reflections or share Notion pages

---

## 2. Notion Database List and Column Definitions

---

### Database 1: `📋 Habit Library`

**Purpose:** The master registry of all habits the user wants to build or is currently tracking. Each entry defines *what* the habit is, *how* it's categorized, and *why* it exists (linked to a life goal). This is the source of truth — habits are referenced from here in every daily log entry.

| Column Name | Data Type | Description |
|---|---|---|
| `Habit Name` | **Title** | The name of the habit (e.g., "Morning Run", "Read 20 Pages") |
| `Category` | **Select** | Life area: `🏃 Health`, `🧠 Mind`, `💼 Work`, `❤️ Relationships`, `💰 Finance`, `🧘 Wellbeing`, `🎨 Creative` |
| `Frequency Target` | **Select** | Expected cadence: `Daily`, `Weekdays Only`, `3x/Week`, `Weekly` |
| `Habit Type` | **Select** | `Build` (adding a behavior) or `Break` (removing a behavior) |
| `Linked Goal` | **Relation** → `🎯 Goals` | The higher-level life goal this habit supports |
| `Trigger / Cue` | **Text** | The situational cue that should prompt this habit (e.g., "After morning coffee") |
| `Minimum Viable Dose` | **Text** | The smallest acceptable version of this habit (e.g., "Even 5 minutes counts") |
| `Why This Habit` | **Text** | Personal motivation statement — why this habit matters to the user |
| `Start Date` | **Date** | When the user officially began tracking this habit |
| `Status` | **Select** | `🟢 Active`, `⏸️ Paused`, `🗄️ Archived` |
| `Difficulty` | **Select** | `Easy`, `Medium`, `Hard` — self-assessed difficulty level |
| `Icon / Emoji` | **Text** | An emoji the user picks to represent this habit visually |
| `Total Completions` | **Rollup** | COUNT of related `✅ Daily Log` entries where `Completed = true` |
| `Completion Rate (30d)` | **Formula** | `round((prop("Total Completions") / 30) * 100)` — approximates 30-day rate |
| `Notes` | **Text** | Freeform notes, research links, tips for maintaining this habit |

---

### Database 2: `✅ Daily Log`

**Purpose:** The heartbeat of the entire template. Every day, the user creates (or uses a template button to generate) entries for each active habit. This database captures binary completion, mood context, difficulty felt in the moment, and optional notes. It is the data source for all streaks, rollups, and analytics.

| Column Name | Data Type | Description |
|---|---|---|
| `Log Entry` | **Title** | Auto-named or manually set (e.g., "Morning Run — Jan 15") |
| `Habit` | **Relation** → `📋 Habit Library` | Which habit this log entry refers to |
| `Date` | **Date** | The calendar date for this log entry |
| `Completed` | **Checkbox** | `✅ true` = done, unchecked = missed |
| `Mood Before` | **Select** | Emotional state before attempting the habit: `😴 Tired`, `😐 Neutral`, `😊 Good`, `🔥 Energized` |
| `Difficulty Felt` | **Select** | How hard it was *in practice*: `Easy`, `Medium`, `Hard`, `Skipped — why below` |
| `Skip Reason` | **Select** | If skipped: `Sick`, `Travel`, `Forgot`, `Too Busy`, `Chose Not To`, `Rest Day` |
| `Notes / Reflection` | **Text** | Optional freeform note (what went well, what to improve) |
| `Duration (min)` | **Number** | Optional: how many minutes spent (for time-based habits) |
| `Quantity` | **Number** | Optional: measurable output (pages read, glasses of water, reps) |
| `Streak Day #` | **Formula** | Complex streak formula (see note below) |
| `Week Number` | **Formula** | `formatDate(prop("Date"), "W")` — for grouping by week |
| `Day of Week` | **Formula** | `formatDate(prop("Date"), "ddd")` — Mon/Tue/Wed etc. |
| `Linked Weekly Review` | **Relation** → `📅 Weekly Reviews` | Links this log entry to the review for its corresponding week |

> **Note on Streak Formula:** True streak calculation in Notion requires external formulas or manual tracking. The `Streak Day #` column uses a simplified formula approach: `if(prop("Completed"), 1, 0)` as a per-entry flag, while the actual *running streak* is calculated via Rollup on the Habit Library database for display purposes. For users wanting advanced streak logic, a linked automation via Notion API or Make.com is recommended.

---

### Database 3: `📅 Weekly Reviews`

**Purpose:** Structured end-of-week reflection journal. Created once per week (typically Sunday), this page synthesizes the past 7 days — celebrating wins, diagnosing slippage, and adjusting habits for the coming week. Linked to all daily log entries from that week.

| Column Name | Data Type | Description |
|---|---|---|
| `Week Title` | **Title** | e.g., "Week 3 — Jan 13–19, 2025" |
| `Week Start Date` | **Date** | Monday of the review week |
| `Overall Rating` | **Select** | `⭐ 1` through `⭐⭐⭐⭐⭐ 5` — subjective week quality |
| `Total Habits Completed` | **Rollup** | COUNT of related Daily Log entries where `Completed = true` |
| `Total Habits Attempted` | **Rollup** | COUNT of all related Daily Log entries |
| `Completion Rate` | **Formula** | `round((prop("Total Habits Completed") / prop("Total Habits Attempted")) * 100)` |
| `Biggest Win` | **Text** | One highlight — a habit or moment that stood out positively |
| `Biggest Challenge` | **Text** | What habit or situation was hardest this week |
| `Root Cause Analysis` | **Text** | Why did failures happen? (No judgment — just honest reflection) |
| `Next Week Intention` | **Text** | One or two adjustments or focus areas for the following week |
| `Energy Level (avg)` | **Select** | `Low`, `Medium`, `High` — overall energy for the week |
| `External Factors` | **Text** | Travel, illness, stress events that affected performance |
| `Daily Logs This Week` | **Relation** → `✅ Daily Log` | All individual log entries from this week |
| `Habits Modified` | **Relation** → `📋 Habit Library` | Any habits that were paused, adjusted, or added this week |

---

### Database 4: `🎯 Goals`

**Purpose:** The top-level "why" layer. Each goal represents a meaningful life outcome the user is working toward. Habits are linked to goals so that every daily check-in carries larger purpose. This database is intentionally kept small (3–7 goals maximum recommended).

| Column Name | Data Type | Description |
|---|---|---|
| `Goal Name` | **Title** | e.g., "Become Physically Fit", "Write My First Book" |
| `Life Area` | **Select** | Mirrors Habit Library categories: `Health`, `Mind`, `Work`, etc. |
| `Goal Description` | **Text** | What success looks like in concrete terms |
| `Target Date` | **Date** | Aspirational deadline or review date |
| `Status` | **Select** | `🌱 Just Started`, `📈 In Progress`, `🎉 Achieved`, `💤 On Hold` |
| `Linked Habits` | **Relation** → `📋 Habit Library` | All habits supporting this goal |
| `Habit Count` | **Rollup** | COUNT of linked habits |
| `Progress Note` | **Text** | Free-form current progress assessment |
| `Motivation Quote` | **Text** | A personal mantra or inspiring quote for this goal |
| `Created Date` | **Date** | When this goal was set |

---

### Database 5: `📊 Monthly Snapshots`

**Purpose:** A lightweight monthly record used as a historical archive. Created once per month, it stores high-level statistics pulled via rollups from the Daily Log. Useful for long-term trend analysis and motivation ("look how far I've come").

| Column Name | Data Type | Description |
|---|---|---|
| `Month` | **Title** | e.g., "January 2025" |
| `Month Start` | **Date** | First day of the month |
| `Daily Logs This Month` | **Relation** → `✅ Daily Log` | All log entries from this month |
| `Total Completions` | **Rollup** | COUNT of completed log entries this month |
| `Total Possible` | **Rollup** | COUNT of all log entries this month |
| `Monthly Completion Rate` | **Formula** | `round((prop("Total Completions") / prop("Total Possible")) * 100)` |
| `Best Habit` | **Text** | Manually noted: which habit had the best streak/rate |
| `Hardest Habit` | **Text** | Manually noted: which habit struggled most |
| `Month Reflection` | **Text** | 2–3 sentence narrative summary |
| `Active Habit Count` | **Number** | How many habits were being tracked this month |

---

## 3. Page Structure

```
🏠 HABIT TRACKER (Top-Level Page / Dashboard)
│
├── 📌 [Pinned Callout Block] — Daily Check-In Quick Access Button
│     └── Button: "+ Log Today's Habits" (opens filtered Daily Log view)
│
├── 📊 Dashboard Overview (Inline Section)
│     ├── [Gallery View] Active Habits — from 📋 Habit Library (Status = Active)
│     ├── [Board View] Today's Log — from ✅ Daily Log (filtered: Date = Today)
│     └── [Progress Bars / Linked Views] Weekly Completion Rate widget
│
├── 📋 Habit Library (Sub-page)
│     ├── Full database: 📋 Habit Library
│     ├── [Gallery View] "Active Habits" — filtered by Status = Active
│     ├── [Gallery View] "By Category" — grouped by Category
│     ├── [Table View] "All Habits" — full master list
│     └── [Table View] "Archived" — filtered by Status = Archived
│
├── ✅ Daily Log (Sub-page)
│     ├── Full database: ✅ Daily Log
│     ├── [Calendar View] "Monthly Calendar" — entries plotted by date
│     ├── [Table View] "Today" — filtered: Date = Today
│     ├── [Table View] "This Week" — filtered: Week Number = current week
│     ├── [Table View] "By Habit" — grouped by Habit relation
│     └── [Table View] "Missed Days" — filtered: Completed = false
│
├── 📅 Weekly Reviews (Sub-page)
│     ├── Full database: 📅 Weekly Reviews
│     ├── [Table View] "All Reviews" — sorted by Week Start Date descending
│     ├── [Gallery View] "Review Cards" — visual card layout with rating
│     └── 📝 [Template] Weekly Review Template
│           └── Pre-filled page with reflection prompts as H2 headers
│
├── 🎯 Goals (Sub-page)
│     ├── Full database: 🎯 Goals
│     ├── [Board View] "By Status" — grouped by Status
│     ├── [Table View] "All Goals" — with linked habit count rollup visible
│     └── [Gallery View] "Goal Cards" — visual motivational layout
│
├── 📊 Monthly Snapshots (Sub-page)
│     ├── Full database: 📊 Monthly Snapshots
│     ├── [Table View] "All Months" — sorted chronologically
│     └── [Gallery View] "Snapshot Cards" — with completion rate visible
│
├── 📈 Analytics Hub (Sub-page — View-Only Linked Databases)
│     ├── Section: "Habit Performance"
│     │     └── [Table View — Linked] Habit Library showing Total Completions + Rate
│     ├── Section: "Weekly Trend"
│     │     └── [Table View — Linked] Weekly Reviews showing Completion Rate + Rating
│     ├── Section: "Category Breakdown"
│     │     └── [Table View — Linked] Daily Log grouped by Habit → Category
│     └── Section: "Monthly Progress"
│           └── [Table View — Linked] Monthly Snapshots with all rate columns
│
└── 📖 Guide & Setup (Sub-page)
      ├── Welcome message and philosophy
      ├── How to use each section (step-by-step)
      ├── FAQ (What if I miss a day? How do I pause a habit?)
      ├── Recommended habit stack for beginners (starter examples)
      └── Credits and version notes
```

---

### Page Hierarchy Summary

| Level | Page / Section | Contains |
|---|---|---|
| **Level 0** | 🏠 Habit Tracker (Dashboard) | Pinned callout, inline gallery views, quick-log button |
| **Level 1** | 📋 Habit Library | Habit Library database + 4 views |
| **Level 1** | ✅ Daily Log | Daily Log database + 5 views |
| **Level 1** | 📅 Weekly Reviews | Weekly Reviews database + 2 views + template |
| **Level 1** | 🎯 Goals | Goals database + 3 views |
| **Level 1** |