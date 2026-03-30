# Notion Template Design Specification

**Theme:** Habit Tracker

---

# Habit Tracker — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most people struggle to build and maintain consistent habits because they lack a **centralized, visual system** that combines planning, daily logging, progress tracking, and reflection in one place. Existing habit-tracking apps are often siloed, lack flexibility, or don't connect habit performance to broader personal goals. This Notion template bridges that gap by providing a fully integrated workspace where users can define habits, log completions, monitor streaks, and review patterns — all without switching between multiple tools.

### Primary Use Cases

- **Daily habit logging** — Quickly check off habits each day in a structured, low-friction interface
- **Streak tracking** — Automatically calculate and visualize current and longest streaks per habit
- **Weekly & monthly reviews** — Reflect on completion rates and adjust habits for the upcoming period
- **Goal-to-habit alignment** — Link each habit to a higher-level life goal or area to maintain motivation
- **Onboarding new habits** — Gradually introduce habits with difficulty levels and start dates to avoid overwhelm

### Detailed Target User Persona

| Attribute | Details |
|---|---|
| **Name** | Alex, 29 |
| **Occupation** | Remote software developer / knowledge worker |
| **Goals** | Improve physical health, build a reading habit, reduce screen time, advance professionally |
| **Pain Points** | Starts habits with enthusiasm but loses track after 2–3 weeks; forgets to log; can't see patterns |
| **Notion Experience** | Intermediate — comfortable with databases and filters but doesn't want to build from scratch |
| **Motivation Style** | Data-driven; enjoys seeing numbers improve; responds well to visual progress indicators |
| **Device Usage** | Primarily desktop for setup and weekly review; mobile for daily quick-logging |
| **Secondary Persona** | Students building study routines; entrepreneurs tracking morning routines; wellness-focused individuals managing health habits |

---

## 2. Notion Database List and Column Definitions

### Database 1: 🎯 Habits (Master Habit Registry)

**Purpose:** The central database that defines every habit a user wants to track. Each entry represents a single habit with its configuration, category, and metadata.

| Column Name | Data Type | Description |
|---|---|---|
| **Habit Name** | Title | The name of the habit (e.g., "Morning Run", "Read 20 Pages", "Meditate") |
| **Category** | Select | Life area the habit belongs to: `Health 🏃`, `Mind 🧠`, `Career 💼`, `Relationships ❤️`, `Finance 💰`, `Creativity 🎨`, `Other ⚙️` |
| **Frequency** | Select | Target frequency: `Daily`, `Weekdays Only`, `Weekends Only`, `3x per Week`, `Weekly` |
| **Target Count** | Number | Number of times per frequency period (e.g., 1 per day, 3 per week). Defaults to 1 |
| **Unit** | Text | What is being measured (e.g., "pages", "minutes", "reps", "glasses") — optional for binary habits |
| **Difficulty** | Select | Habit effort level: `Easy 🟢`, `Medium 🟡`, `Hard 🔴` |
| **Cue / Trigger** | Text | The environmental or time-based cue that triggers this habit (e.g., "After morning coffee") |
| **Why I'm Doing This** | Text | Personal motivation statement — helps reconnect with purpose during low-motivation periods |
| **Linked Goal** | Relation | Links to the **Goals** database — associates the habit with a higher-level goal |
| **Start Date** | Date | The date the user officially began tracking this habit |
| **Is Active** | Checkbox | When unchecked, the habit is archived and excluded from daily views without deletion |
| **Icon / Emoji** | Text | A single emoji the user adds to the habit name or uses for visual identification |
| **Total Completions** | Rollup | Counts all related entries in the **Daily Log** database where `Completed = ✅` |
| **Current Streak** | Formula | Calculated using log entries — counts consecutive days (from today backwards) where the habit was completed. *(See formula note below)* |
| **Best Streak** | Number | Manually updated (or semi-automated) field for the user's all-time best streak for this habit |
| **Completion Rate (30d)** | Formula | `Total completions in last 30 days / expected completions in 30 days × 100` — expressed as a percentage |
| **Notes** | Text | Additional setup notes, modifications, or reminders about this habit |

> **Formula Note:** Notion's native formula engine has limitations with date-based rollup calculations. The `Current Streak` formula uses a simplified approach: it counts log entries marked complete in the most recent consecutive date range. For advanced streak tracking, a linked **Streak Snapshots** entry (manually or button-updated) is recommended as a companion field.

---

### Database 2: 📅 Daily Log (Habit Completion Records)

**Purpose:** The operational heart of the tracker. Each entry records whether a specific habit was completed on a specific day. This is the database users interact with most frequently.

| Column Name | Data Type | Description |
|---|---|---|
| **Log Entry Name** | Title | Auto-named using format: `[Habit Name] — [Date]` (e.g., "Morning Run — 2025-01-15") |
| **Habit** | Relation | Links to the **Habits** database — identifies which habit this log entry belongs to |
| **Date** | Date | The calendar date for this log entry |
| **Completed** | Checkbox | The primary check — did the user complete this habit on this date? |
| **Actual Count** | Number | Optional: If the habit has a unit (e.g., pages, minutes), record the actual amount completed |
| **Mood** | Select | How the user felt during or after completing the habit: `😊 Great`, `😐 Okay`, `😔 Low`, `💪 Energized`, `😴 Tired` |
| **Effort Level** | Select | Subjective effort for that day: `Easy`, `Moderate`, `Hard`, `Skipped — Intentional`, `Skipped — Forgot` |
| **Day of Week** | Formula | `formatDate(prop("Date"), "ddd")` — Automatically displays Mon, Tue, Wed, etc. |
| **Week Number** | Formula | `formatDate(prop("Date"), "WW")` — Displays ISO week number for weekly grouping |
| **Month** | Formula | `formatDate(prop("Date"), "MMMM YYYY")` — Used for monthly filter views |
| **Notes / Reflection** | Text | Optional daily micro-reflection: what made it easy or hard today? |
| **Habit Category** | Rollup | Pulls the `Category` from the linked Habit record — enables filtering logs by life area |
| **Habit Difficulty** | Rollup | Pulls `Difficulty` from the linked Habit — used in analytics views |

---

### Database 3: 🏆 Goals (Life Areas & High-Level Objectives)

**Purpose:** Provides the "why" behind each habit. Users define broad life goals or areas, then link their habits to these goals. This creates a motivational layer that connects micro-actions to macro-intentions.

| Column Name | Data Type | Description |
|---|---|---|
| **Goal Name** | Title | The name of the goal or life area (e.g., "Become Physically Fit", "Read 24 Books This Year") |
| **Goal Type** | Select | `Outcome Goal` (specific result) or `Identity Goal` (type of person to become) |
| **Target Date** | Date | Optional deadline or milestone date for the goal |
| **Status** | Select | `Active 🚀`, `Achieved ✅`, `Paused ⏸️`, `Abandoned ❌` |
| **Description** | Text | Detailed description of what success looks like for this goal |
| **Linked Habits** | Relation | Reverse relation — shows all habits connected to this goal |
| **Active Habit Count** | Rollup | Counts the number of active habits linked to this goal |
| **Progress Notes** | Text | Running log of milestones, reflections, or updates toward this goal |
| **Priority** | Select | `High 🔴`, `Medium 🟡`, `Low 🟢` — helps the user focus when goals compete |
| **Cover Image** | Files & Media | Optional: upload an inspirational image that represents achieving this goal |

---

### Database 4: 📝 Weekly Reviews (Reflection & Planning Records)

**Purpose:** Structured weekly check-ins where users assess the past week, celebrate wins, identify patterns, and set intentions for the coming week. Each entry = one week.

| Column Name | Data Type | Description |
|---|---|---|
| **Review Title** | Title | Auto-named as `Week [#] Review — [Date Range]` (e.g., "Week 03 Review — Jan 13–19") |
| **Review Date** | Date | The date the review was completed (typically Sunday evening or Monday morning) |
| **Week Start** | Date | The Monday of the reviewed week |
| **Week End** | Date | The Sunday of the reviewed week |
| **Overall Completion Rate** | Number | User-entered percentage of habits completed that week (can be referenced from daily log views) |
| **Energy Level This Week** | Select | `High ⚡`, `Medium 〰️`, `Low 🔋` — overall energy/motivation level for the week |
| **Top Win** | Text | The single biggest habit success of the week |
| **Biggest Challenge** | Text | The habit or situation that was hardest this week |
| **What Helped** | Text | Conditions, strategies, or circumstances that supported habit completion |
| **What Hindered** | Text | Obstacles, distractions, or circumstances that made habits harder |
| **Habits to Adjust** | Text | Specific habits to modify, add, pause, or remove next week |
| **Intentions for Next Week** | Text | 1–3 focus areas or specific commitments for the upcoming week |
| **Rating (1–10)** | Number | Overall satisfaction score for the week (1 = very poor, 10 = excellent) |
| **Linked Log Entries** | Relation | Optional: manually link key daily log entries from the week for reference |

---

### Database 5: 📊 Streak Snapshots (Streak History Log)

**Purpose:** Because Notion formulas can't reliably calculate live streaks across thousands of entries, this lightweight database captures periodic streak data points. Users (or a simple manual process) update this once daily to preserve streak history.

| Column Name | Data Type | Description |
|---|---|---|
| **Snapshot Name** | Title | Auto-named as `[Habit Name] — Streak on [Date]` |
| **Habit** | Relation | Links to the **Habits** database |
| **Snapshot Date** | Date | The date this snapshot was recorded |
| **Current Streak (Days)** | Number | The user's active streak count as of this date |
| **Is New Best** | Checkbox | Check if this streak count surpasses the previous best streak |
| **Note** | Text | Optional context (e.g., "Broke 30-day barrier!", "Restarting after travel break") |

---

## 3. Page Structure

```
📚 HABIT TRACKER (Top-Level Workspace Page)
│
├── 🏠 Dashboard (Main Hub Page)
│   ├── [Header] Welcome banner + current date
│   ├── [Gallery/Board] Today's Habits — filtered view of Daily Log
│   │   showing only today's date, grouped by Habit Category
│   ├── [Progress Bar Section] Weekly completion percentage callout blocks
│   ├── [Linked Database] Active Habits — gallery view of Habits DB
│   │   filtered: Is Active = ✅, sorted by Category
│   └── [Callout Block] Quick Links to sub-pages
│
├── ✅ Daily Check-In (Sub-Page)
│   ├── [Instructional text] "Check off your habits for today"
│   ├── [Linked Database View] Today's Log
│   │   • View type: Table or Board
│   │   • Filter: Date = Today
│   │   • Properties shown: Habit, Completed, Actual Count, Mood, Notes
│   └── [Button] "➕ Add Missing Habit Entry" — opens new Daily Log entry
│
├── 📋 My Habits (Sub-Page)
│   ├── [Linked Database] Habits — Full Table View
│   │   • All columns visible
│   │   • Filter toggle: Active Only vs. All Habits
│   │   • Sorted by: Category, then Difficulty
│   ├── [Linked Database] Habits — Gallery View (visual card layout)
│   │   • Shows: Habit Name, Category, Streak, Completion Rate
│   └── [Button] "➕ Add New Habit" — opens new Habits entry with template
│
├── 📈 Analytics & Progress (Sub-Page)
│   ├── [Section Header] "30-Day Overview"
│   ├── [Linked Database] Daily Log — Calendar View
│   │   • Color-coded by Completed status
│   │   • Filter: Last 30 days
│   ├── [Linked Database] Daily Log — Table View grouped by Month
│   │   • Shows completion rates per month
│   ├── [Linked Database] Habits — Table View
│   │   • Shows: Habit Name, Total Completions, Completion Rate (30d), Best Streak
│   │   • Sorted by Completion Rate descending
│   ├── [Linked Database] Streak Snapshots — Timeline View
│   │   • Shows streak progression over time per habit
│   └── [Callout] "📌 Tip: Review this page every Sunday during your Weekly Review"
│
├── 🏆 Goals (Sub-Page)
│   ├── [Linked Database] Goals — Board View grouped by Status
│   ├── [Linked Database] Goals — Table View (detailed)
│   │   • Shows all columns including Active Habit Count rollup
│   └── [Button] "➕ Add New Goal"
│
├── 📝 Weekly Reviews (Sub-Page)
│   ├── [Instructional Callout] "Complete this every Sunday. Takes 10–15 minutes."
│   ├── [Linked Database] Weekly Reviews — Table View (newest first)
│   ├── [Linked Database] Weekly Reviews — Gallery View (visual cards)
│   └── [Button] "➕ Start This Week's Review" — opens new entry with template
│
├── 📊 Streak Log (Sub-Page)
│   ├── [Instructional text] "Update your streaks daily for accurate tracking"
│   ├── [Linked Database] Streak Snapshots — Table View
│   │   • Sorted by Snapshot Date descending
│   │   • Grouped by Habit
│   └── [Button] "➕ Log Today's Streaks"
│
└── 📖 Guide & Setup (Sub-Page)
    ├── [Section] How to Use This Template (overview)
    ├── [Section] Getting Started Checklist (checkbox list)
    ├── [Section] Habit Design Tips (callout blocks)
    ├── [Section] Frequently Asked Questions
    └── [Section] Keyboard Shortcuts & Notion Tips
```

### Database Placement Summary

| Database | Primary Home Page | Additional Views Located |
|---|---|---|
| **Habits** | My Habits page | Dashboard (gallery), Analytics page |
| **Daily Log** | Daily Check-In page | Dashboard (today view), Analytics (calendar + table) |
| **Goals** | Goals page | My Habits page (linked context) |
| **Weekly Reviews** | Weekly Reviews page | — |
| **Streak Snapshots** | Streak Log page | Analytics page (timeline) |

---

## 4. Getting-Started Flow (3 Steps)

---

### ✅ Step 1: Define Your Habits (5–10 minutes)

> **Navigate to: 📋 My Habits → Click "➕ Add New Habit"**

Before you can track anything, you need to tell the system *what* to track. Start by creating **3 to 5 habits maximum** — beginners who start with too many habits at once tend to quit within two weeks.

For each habit, fill in the following fields:

1. **Habit Name** — Use action-oriented language (e.g., "Do 10 push-ups" not "Exercise more")
2. **Category** — Choose the life area this habit belongs to
3. **Frequency**