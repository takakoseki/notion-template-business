# Notion Template Design Specification

**Theme:** Life OS / Second Brain

---

# Life OS / Second Brain — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Modern knowledge workers, students, and ambitious individuals are drowning in fragmented information. Notes live in one app, tasks in another, goals are scribbled on sticky notes, and reading lists are buried in browser bookmarks. This **Life OS / Second Brain** template solves the "scattered mind" problem by creating a single, interconnected operating system for your entire life — capturing every input, processing it into actionable knowledge, and connecting it to meaningful goals.

### Primary Use Cases

- **Centralized knowledge management**: Capture notes, ideas, articles, books, and meeting summaries in one place
- **Goal-to-task alignment**: Connect daily tasks directly to quarterly goals and life areas
- **Personal knowledge base**: Build a searchable, linked library of everything you've learned
- **Weekly & daily review rituals**: Structured review pages to keep you on track
- **Project management**: Manage personal and professional projects from ideation to completion
- **Habit and life tracking**: Monitor habits, health, finances, and key metrics over time
- **Content consumption tracking**: Log books, articles, podcasts, and courses with notes and ratings

### Detailed Target User Persona

---

**Persona 1 — "The Overwhelmed Professional"**
- **Name**: Alex, 32
- **Role**: Product Manager at a mid-size tech company
- **Pain Points**: Attends 8+ meetings a day, ideas get lost, struggles to connect day-to-day work to long-term career goals, uses 5 different apps that don't talk to each other
- **Goals**: Build a personal knowledge library, reduce mental clutter, make progress on side projects
- **Tech Comfort**: High — uses Notion at work, comfortable with databases and relations

---

**Persona 2 — "The Ambitious Student"**
- **Name**: Priya, 24
- **Role**: Graduate student + freelance writer
- **Pain Points**: Manages coursework, freelance deadlines, personal goals, and reading all at once; lacks a system to connect learning to output
- **Goals**: Write a thesis, grow freelance income, read 30 books per year, track habits
- **Tech Comfort**: Medium — knows Notion basics, wants a ready-to-use system

---

**Persona 3 — "The Self-Improvement Enthusiast"**
- **Name**: Marcus, 40
- **Role**: Sales Director and aspiring entrepreneur
- **Pain Points**: Consumes a lot of content (books, podcasts, courses) but fails to retain or apply it; no system for turning inspiration into action
- **Goals**: Launch a side business, build consistent habits, document personal growth journey
- **Tech Comfort**: Medium-High — motivated to invest time in a system that works

---

## 2. Notion Database List and Column Definitions

### Database 1: 🗂️ Projects

**Purpose**: Track all active and archived personal/professional projects from start to finish, linked to life areas and goals.

| Column Name | Data Type | Description |
|---|---|---|
| Project Name | Title | Name of the project |
| Status | Select | `🌱 Idea` / `🔄 Active` / `⏸️ On Hold` / `✅ Done` / `🗃️ Archived` |
| Life Area | Relation | Links to the **Life Areas** database |
| Goal | Relation | Links to the **Goals** database (which goal this project advances) |
| Priority | Select | `🔴 High` / `🟡 Medium` / `🟢 Low` |
| Start Date | Date | When the project began or is planned to begin |
| Due Date | Date | Target completion date |
| Description | Text | Brief description of the project's purpose and desired outcome |
| Key Outcome | Text | The single most important deliverable or result |
| Progress | Formula | `prop("Tasks Done") / prop("Total Tasks") * 100` — shows % completion |
| Total Tasks | Rollup | Counts all related tasks from the **Tasks** database |
| Tasks Done | Rollup | Counts tasks with Status = "Done" from the **Tasks** database |
| Tags | Multi-select | e.g., `Work`, `Personal`, `Creative`, `Learning`, `Finance` |
| Cover Image | Files & Media | Optional project cover photo or icon |
| Notes | Text | Free-form field for context, links, or quick notes |

---

### Database 2: ✅ Tasks

**Purpose**: The universal task inbox and action tracker. Every next action, to-do, and commitment lives here.

| Column Name | Data Type | Description |
|---|---|---|
| Task Name | Title | Name of the action or to-do |
| Status | Select | `📥 Inbox` / `🔜 Next Action` / `🔄 In Progress` / `✅ Done` / `🗑️ Cancelled` |
| Project | Relation | Links to the **Projects** database |
| Goal | Relation | Links to the **Goals** database (optional direct link) |
| Life Area | Relation | Links to the **Life Areas** database |
| Due Date | Date | When this task must be completed |
| Scheduled Date | Date | When you plan to work on this task |
| Priority | Select | `🔴 High` / `🟡 Medium` / `🟢 Low` |
| Energy Required | Select | `⚡ High Focus` / `🔋 Medium` / `😴 Low Energy` |
| Estimated Time | Number | Estimated minutes to complete |
| Recurring | Checkbox | Is this a recurring task? |
| Recurrence Pattern | Select | `Daily` / `Weekly` / `Monthly` / `Quarterly` (visible if Recurring = true) |
| Context | Multi-select | `@Home` / `@Work` / `@Computer` / `@Phone` / `@Errands` |
| Notes | Text | Additional context, links, or subtask details |
| Completed On | Date | Actual completion date (set manually or via automation) |
| Week | Formula | `formatDate(prop("Scheduled Date"), "YYYY-[W]WW")` — groups by week |

---

### Database 3: 🎯 Goals

**Purpose**: Define and track short-term, quarterly, annual, and life goals. The connective tissue between daily work and long-term vision.

| Column Name | Data Type | Description |
|---|---|---|
| Goal Name | Title | Clear, specific goal statement |
| Timeframe | Select | `🗓️ Weekly` / `📅 Monthly` / `📆 Quarterly` / `🌍 Annual` / `🔭 Life Goal` |
| Status | Select | `🌱 Not Started` / `🔄 In Progress` / `✅ Achieved` / `🗃️ Abandoned` |
| Life Area | Relation | Links to the **Life Areas** database |
| Parent Goal | Relation | Self-referential — links to a larger/parent goal (e.g., Annual → Life Goal) |
| Why | Text | The reason this goal matters — your personal "why" statement |
| Success Criteria | Text | What does "done" look like? How will you measure success? |
| Target Date | Date | Deadline or target completion date |
| Progress % | Number | Manual 0–100 progress slider |
| Key Projects | Rollup | Shows related project names from the **Projects** database |
| Key Tasks | Rollup | Count of linked tasks from the **Tasks** database |
| Review Notes | Text | Notes from periodic goal reviews |
| Tags | Multi-select | Free-form categorization |

---

### Database 4: 🧠 Notes / Knowledge Base

**Purpose**: The core of the Second Brain — capture, process, and connect all ideas, learnings, meeting notes, fleeting thoughts, and permanent notes.

| Column Name | Data Type | Description |
|---|---|---|
| Note Title | Title | Title of the note or idea |
| Type | Select | `💡 Idea` / `📝 Meeting Note` / `📖 Literature Note` / `🌲 Permanent Note` / `📌 Reference` / `🗺️ MOC (Map of Content)` |
| Status | Select | `📥 Inbox` / `🔍 Processing` / `✅ Processed` / `🌲 Evergreen` |
| Life Area | Relation | Links to the **Life Areas** database |
| Project | Relation | Links to the **Projects** database (if note belongs to a project) |
| Source | Relation | Links to the **Library** database (if note is from a book, article, etc.) |
| Related Notes | Relation | Self-referential — links to other notes in this database (bi-directional linking) |
| Tags | Multi-select | Topic tags: `Psychology`, `Productivity`, `Finance`, `Philosophy`, `Tech`, etc. |
| Created Date | Created time | Auto-populated timestamp |
| Last Edited | Last edited time | Auto-populated last edit timestamp |
| Review Flag | Checkbox | Mark for next review session |
| Summary | Text | 2–3 sentence summary of the note's core insight |
| Atomic Insight | Text | The single most important takeaway (for Permanent Notes) |

---

### Database 5: 📚 Library (Books, Articles, Podcasts, Courses)

**Purpose**: Track all media consumption — what you're reading, watching, listening to — with ratings, status, and linked notes.

| Column Name | Data Type | Description |
|---|---|---|
| Title | Title | Name of the book, article, podcast episode, or course |
| Type | Select | `📗 Book` / `📰 Article` / `🎙️ Podcast` / `🎬 Video` / `🎓 Course` / `🔗 Website` |
| Author / Creator | Text | Author, host, or creator name |
| Status | Select | `📋 Backlog` / `🔄 In Progress` / `✅ Completed` / `⏸️ On Hold` / `🗑️ Dropped` |
| Rating | Select | `⭐` / `⭐⭐` / `⭐⭐⭐` / `⭐⭐⭐⭐` / `⭐⭐⭐⭐⭐` |
| Genre / Topic | Multi-select | `Self-Help`, `Business`, `Science`, `Fiction`, `Technology`, `Philosophy`, etc. |
| Date Started | Date | When you started consuming this content |
| Date Finished | Date | When you finished |
| URL | URL | Link to the article, podcast episode, or course page |
| Notes Count | Rollup | Count of linked notes from the **Notes / Knowledge Base** database |
| Key Takeaway | Text | The most impactful insight or lesson from this content |
| Would Recommend | Checkbox | Toggle if you'd recommend this to others |
| Life Area | Relation | Links to the **Life Areas** database |

---

### Database 6: 🌿 Life Areas

**Purpose**: Define the key domains of your life. Acts as the master taxonomy that connects goals, projects, tasks, and notes.

| Column Name | Data Type | Description |
|---|---|---|
| Area Name | Title | Name of the life area (e.g., Health, Career, Finance) |
| Description | Text | Brief description of what this area covers |
| Icon / Emoji | Text | Emoji for quick visual identification |
| Focus Level | Select | `🔥 High Focus` / `✅ Maintenance` / `💤 Low Priority` |
| Current Score | Number | 1–10 self-assessment of current satisfaction in this area |
| Ideal Score | Number | 1–10 target satisfaction level |
| Active Goals | Rollup | Count of active goals in this area |
| Active Projects | Rollup | Count of active projects in this area |
| Color | Select | Color tag for visual dashboards: `Red`, `Blue`, `Green`, `Purple`, `Orange`, etc. |

**Suggested Life Areas** (pre-filled):
- 🏥 Health & Fitness
- 💼 Career & Work
- 💰 Finance & Wealth
- 🧠 Learning & Growth
- 👥 Relationships & Social
- 🎨 Creative & Hobbies
- 🏠 Home & Environment
- ✨ Mindfulness & Spirituality

---

### Database 7: 📓 Journal / Daily Log

**Purpose**: Daily reflection, gratitude, mood tracking, and intention-setting. The daily entry point for the Life OS.

| Column Name | Data Type | Description |
|---|---|---|
| Date | Title | Date as the title (e.g., "2024-01-15 — Monday") |
| Date (Structured) | Date | Structured date field for filtering and sorting |
| Day of Week | Formula | `formatDate(prop("Date (Structured)"), "dddd")` |
| Mood | Select | `😊 Great` / `🙂 Good` / `😐 Neutral` / `😔 Low` / `😤 Stressed` |
| Energy Level | Select | `⚡ High` / `🔋 Medium` / `😴 Low` |
| Morning Intention | Text | 1–3 sentences: what matters most today? |
| Top 3 Priorities | Text | The 3 most important tasks or outcomes for the day |
| Gratitude | Text | 3 things you're grateful for |
| Wins | Text | What went well today? |
| Challenges | Text | What was difficult? What would you do differently? |
| Evening Reflection | Text | Free-form end-of-day reflection |
| Hours Slept | Number | Sleep hours (previous night) |
| Exercise | Checkbox | Did you exercise today? |
| Word Count | Number | Daily writing/note word count (optional tracking) |
| Week Number | Formula | `formatDate(prop("Date (Structured)"), "YYYY-[W]WW")` |

---

### Database 8: 🔁 Habits Tracker

**Purpose**: Define habits and track daily/weekly completion. Monitor streaks and consistency over time.

| Column Name | Data Type | Description |
|---|---|---|
| Habit Name | Title | Name of the habit (e.g., "Morning Meditation") |
| Category | Select | `🏥 Health` / `🧠 Mind` / `💰 Finance` / `🎨 Creative` / `👥 Social` / `📚 Learning` |
| Frequency | Select | `Daily` / `Weekdays Only` / `3x Per Week` / `Weekly` |
| Target | Number | Target number of completions per week/month |
| Streak (Current) | Number | Manually updated or via automation |
| Best Streak | Number | Longest streak achieved |
| Start Date | Date | When you started tracking this habit |
| Active | Checkbox | Is this habit currently being tracked? |
| Life Area | Relation | Links to the **Life Areas** database |
| Goal | Relation | Links to the **Goals** database (which goal this habit supports) |
| Notes | Text | Why this habit matters; implementation intention |
| Cue | Text | The trigger that prompts this habit |
| Reward | Text | The reward or satisfaction tied to completion |

---

### Database 9: 📅 Weekly Reviews

**Purpose**: Structured weekly review template to close out the week, assess progress, and plan the next.

| Column Name | Data Type | Description |
|---|---|---|
| Week Title | Title | e.g., "Week 3 — January 2024" |
| Week Number | Text | e.g., `2024-W03` |
| Date Range | Date | Start date of the week |
| Overall Rating | Select | `⭐` through `⭐⭐⭐⭐⭐` — overall week quality |
| Energy Average | Select | `High` / `Medium` / `Low` |
| Top Wins | Text | 3–5 biggest wins of the week |
| Biggest Challenge | Text | Main obstacle or setback faced |
| Tasks Completed | Number | Number of tasks finished this week |
| Goals Progressed | Number | Number of goals you made progress on |
| Lessons Learned | Text | Key insights or learnings from the week |
| Next Week Focus | Text | Top 3 priorities or themes for the coming week |
| Projects Updated | Relation | Links to **Projects** reviewed this week |
| Gratitude | Text | What are you most grateful for this week? |
| Self-Care Score | Number | 1–10 rating of how well you took care of yourself |

---

### Database 10: 💰 Finance Tracker

**Purpose**: Track income, expenses, savings, and financial goals to maintain awareness and improve financial health.

| Column Name | Data Type | Description |
|---|---|---|
| Entry Name | Title | Description of the transaction or financial entry |