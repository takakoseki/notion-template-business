# Notion Template Design Specification

**Theme:** Study / Learning

---

# 📚 StudyOS — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most learners struggle with **fragmented study systems** — notes scattered across apps, no visibility into progress, forgotten resources, and inconsistent study habits. StudyOS consolidates every aspect of a learning workflow — course tracking, note-taking, resource management, review scheduling, and goal setting — into a single, interconnected Notion workspace.

### Primary Use Cases

- Tracking progress across multiple courses, books, or certifications simultaneously
- Capturing and organizing lecture notes, summaries, and key concepts
- Managing a reading/watching list of learning resources
- Scheduling spaced repetition reviews for better retention
- Setting weekly study goals and monitoring consistency
- Preparing for exams or certification deadlines

### Target User Persona

| Attribute | Detail |
|---|---|
| **Name** | Alex, 26 |
| **Background** | Working professional pursuing self-directed learning and side certifications |
| **Goals** | Complete 2 online courses per quarter, read 1 non-fiction book per month, prepare for AWS Solutions Architect exam |
| **Pain Points** | Loses track of where they left off, forgets to review material, has no single view of all active learning |
| **Tools Currently Used** | Scattered Google Docs, browser bookmarks, sticky notes, and calendar reminders |
| **Notion Experience** | Intermediate — comfortable with databases, basic relations, and filtered views |
| **Secondary Persona** | University students managing coursework across multiple subjects with assignment deadlines |

---

## 2. Notion Database List and Column Definitions

### Database 1: 🎓 Courses & Subjects

**Purpose:** The master registry of everything being studied. Each record represents one course, subject, book, or certification program.

| Column Name | Data Type | Description |
|---|---|---|
| **Name** | Title | Name of the course, subject, or book |
| **Type** | Select | Category: `Online Course` / `Book` / `Certification` / `University Subject` / `Workshop` / `Podcast Series` |
| **Status** | Select | `Not Started` / `In Progress` / `Paused` / `Completed` / `Dropped` |
| **Platform / Source** | Text | Where the content lives (e.g., Udemy, Coursera, O'Reilly, University) |
| **URL** | URL | Direct link to the course or resource |
| **Instructor / Author** | Text | Name of the teacher, author, or institution |
| **Start Date** | Date | When the learner began this course |
| **Target End Date** | Date | Deadline or self-imposed completion date |
| **Priority** | Select | `High` / `Medium` / `Low` |
| **Total Lessons / Chapters** | Number | Total number of lessons, chapters, or modules |
| **Completed Lessons** | Number | Number of lessons/chapters finished so far |
| **Progress %** | Formula | `prop("Completed Lessons") / prop("Total Lessons / Chapters") * 100` — displays completion percentage |
| **Tags** | Multi-select | Topic tags: `Programming` / `Design` / `Business` / `Language` / `Science` / `Math` / `Health` etc. |
| **Certificate Earned** | Checkbox | Check when a certificate or credential has been received |
| **Rating** | Select | Personal rating after completion: `⭐` / `⭐⭐` / `⭐⭐⭐` / `⭐⭐⭐⭐` / `⭐⭐⭐⭐⭐` |
| **Notes Count** | Rollup | Counts related records in the Notes & Summaries database |
| **Cover Image** | Files & Media | Course thumbnail or book cover |

---

### Database 2: 📝 Notes & Summaries

**Purpose:** Stores all study notes, lecture summaries, chapter breakdowns, and concept explanations linked to their parent course.

| Column Name | Data Type | Description |
|---|---|---|
| **Title** | Title | Descriptive title of the note (e.g., "Chapter 3 — OSI Model Explained") |
| **Course** | Relation | Links to a record in the Courses & Subjects database |
| **Note Type** | Select | `Lecture Notes` / `Chapter Summary` / `Concept Deep-Dive` / `Mind Map` / `Q&A` / `Cheat Sheet` |
| **Date Taken** | Date | When the note was created or the lesson was studied |
| **Lesson / Module #** | Text | Reference to the specific lesson or chapter (e.g., "Module 4, Lesson 2") |
| **Key Takeaways** | Text | 3–5 bullet-point summary of the most important concepts |
| **Needs Review** | Checkbox | Flag notes that require a follow-up review session |
| **Difficulty** | Select | Self-assessed difficulty of the material: `Easy` / `Medium` / `Hard` |
| **Tags** | Multi-select | Concept-level tags (e.g., `Networking` / `Security` / `Algorithms`) |
| **Flashcard Created** | Checkbox | Indicates whether flashcards have been made from this note |
| **Last Reviewed** | Date | Date of the most recent review of this note |
| **Attachments** | Files & Media | Upload slides, PDFs, diagrams, or screenshots |

> 💡 **Note:** Each Notes page uses a full-page template with structured sections: **Overview**, **Key Concepts**, **Examples**, **Questions I Have**, and **Action Items**.

---

### Database 3: 📅 Study Sessions

**Purpose:** A log of every study session completed, enabling habit tracking, time analysis, and accountability.

| Column Name | Data Type | Description |
|---|---|---|
| **Session Title** | Title | Brief label for the session (e.g., "AWS EC2 Deep Dive - Sunday") |
| **Date** | Date | Date of the study session |
| **Course** | Relation | Links to the relevant course in Courses & Subjects |
| **Duration (minutes)** | Number | Total time spent studying in this session |
| **Topics Covered** | Text | Free-text description of what was studied |
| **Mood / Energy** | Select | `🔥 Focused` / `😐 Neutral` / `😴 Tired` / `⚡ Energized` |
| **Session Type** | Select | `New Material` / `Review` / `Practice / Exercises` / `Project Work` / `Reading` |
| **Goals Met** | Checkbox | Did the learner achieve what they planned for this session? |
| **Notes Taken** | Relation | Links to notes created during this session |
| **Distractions / Issues** | Text | Optional reflection on what interrupted or hindered the session |
| **Week Number** | Formula | `formatDate(prop("Date"), "W")` — extracts ISO week number for weekly grouping |

---

### Database 4: 🔁 Review Queue (Spaced Repetition Tracker)

**Purpose:** Manages scheduled review sessions to reinforce retention using a simplified spaced repetition system.

| Column Name | Data Type | Description |
|---|---|---|
| **Topic / Concept** | Title | The specific concept or topic to be reviewed |
| **Source Note** | Relation | Links to the original note in Notes & Summaries |
| **Course** | Relation | Links to the parent course |
| **First Learned** | Date | When the concept was first studied |
| **Next Review Date** | Date | The scheduled date for the next review |
| **Review Interval** | Select | Current spacing interval: `1 Day` / `3 Days` / `1 Week` / `2 Weeks` / `1 Month` / `Mastered` |
| **Times Reviewed** | Number | Count of how many times this concept has been reviewed |
| **Confidence Level** | Select | Self-assessed understanding: `1 – No Clue` / `2 – Vague` / `3 – Partial` / `4 – Good` / `5 – Mastered` |
| **Review Status** | Select | `Due Today` / `Upcoming` / `Overdue` / `Mastered` |
| **Is Overdue** | Formula | `if(prop("Next Review Date") < now() and prop("Review Status") != "Mastered", true, false)` |
| **Notes** | Text | Review session observations or updated understanding |

---

### Database 5: 📚 Resource Library

**Purpose:** A curated inbox and long-term archive of all learning resources — articles, videos, books, podcasts, tools — whether consumed or saved for later.

| Column Name | Data Type | Description |
|---|---|---|
| **Resource Title** | Title | Name of the article, video, tool, or book |
| **URL** | URL | Direct link to the resource |
| **Resource Type** | Select | `Article` / `Video` / `Book` / `Podcast` / `Tool` / `Research Paper` / `GitHub Repo` / `Course` |
| **Related Course** | Relation | Optionally links to a course in Courses & Subjects |
| **Topic Tags** | Multi-select | Subject area tags matching the Courses taxonomy |
| **Status** | Select | `Inbox` / `Reading / Watching` / `Completed` / `Archived` / `Recommended to Others` |
| **Date Saved** | Date | When the resource was added to the library |
| **Date Consumed** | Date | When the learner finished reading/watching |
| **Key Insight** | Text | One-sentence summary of the main takeaway |
| **Worth Revisiting** | Checkbox | Flags high-value resources for future reference |
| **Recommended By** | Text | Person, community, or source that recommended this resource |
| **Rating** | Select | `⭐` through `⭐⭐⭐⭐⭐` personal usefulness rating |

---

### Database 6: 🎯 Goals & Milestones

**Purpose:** Defines short-term and long-term learning goals with measurable outcomes and deadlines.

| Column Name | Data Type | Description |
|---|---|---|
| **Goal Title** | Title | Clear, specific goal statement (e.g., "Complete AWS SAA Certification by June 30") |
| **Goal Type** | Select | `Daily` / `Weekly` / `Monthly` / `Quarterly` / `Annual` / `Project-Based` |
| **Related Course** | Relation | Links to a course this goal supports |
| **Target Date** | Date | Deadline for achieving this goal |
| **Status** | Select | `Active` / `Completed` / `Missed` / `Revised` |
| **Success Metric** | Text | How completion will be measured (e.g., "Pass practice exam with ≥80%") |
| **Progress Notes** | Text | Running log of progress updates |
| **Completion Date** | Date | Actual date the goal was achieved |
| **Priority** | Select | `Critical` / `High` / `Medium` / `Low` |
| **Streak / Consistency** | Number | For recurring goals, track current streak in days |
| **Linked Sessions** | Rollup | Counts study sessions tied to the related course |

---

## 3. Page Structure

```
📚 StudyOS (Top-Level Workspace Page)
│
├── 🏠 Dashboard (Home)
│   ├── [View] Active Courses — Gallery view of In Progress courses
│   ├── [View] Today's Review Queue — filtered Review Queue (Due Today + Overdue)
│   ├── [View] Recent Notes — Notes & Summaries sorted by Date Taken (last 7 days)
│   ├── [View] This Week's Study Sessions — Study Sessions filtered by current week
│   ├── [View] Active Goals — Goals & Milestones filtered by Status = Active
│   └── [Callout Block] Weekly Study Time — manual or linked summary
│
├── 🎓 My Courses
│   ├── [Database: Courses & Subjects] — Full-page database
│   │   ├── View: All Courses (Table)
│   │   ├── View: By Status (Board — grouped by Status)
│   │   ├── View: By Priority (Table — sorted by Priority)
│   │   ├── View: Completed (Table — filtered Status = Completed)
│   │   └── View: In Progress (Gallery — filtered Status = In Progress)
│   └── [Sub-page] 📋 Course Template Instructions
│
├── 📝 Notes & Summaries
│   ├── [Database: Notes & Summaries] — Full-page database
│   │   ├── View: All Notes (Table)
│   │   ├── View: Needs Review (Table — filtered Needs Review = checked)
│   │   ├── View: By Course (Table — grouped by Course relation)
│   │   ├── View: By Note Type (Board — grouped by Note Type)
│   │   └── View: This Week (Table — filtered Date Taken = this week)
│   └── [Sub-page] 📄 Note-Taking Guide & Best Practices
│
├── ⏱️ Study Log
│   ├── [Database: Study Sessions] — Full-page database
│   │   ├── View: All Sessions (Table — sorted by Date descending)
│   │   ├── View: Calendar (Calendar — by Date)
│   │   ├── View: By Course (Table — grouped by Course)
│   │   ├── View: Weekly Summary (Table — grouped by Week Number)
│   │   └── View: This Month (Table — filtered current month)
│   └── [Sub-page] 📊 Study Time Analytics (manual chart area with progress bars)
│
├── 🔁 Review Queue
│   ├── [Database: Review Queue] — Full-page database
│   │   ├── View: Due Today (Table — filtered Next Review Date = today, sorted by Confidence)
│   │   ├── View: Overdue (Table — filtered Is Overdue = true)
│   │   ├── View: All Topics (Table — sorted by Next Review Date)
│   │   ├── View: By Confidence (Board — grouped by Confidence Level)
│   │   └── View: Mastered (Table — filtered Review Interval = Mastered)
│   └── [Sub-page] 🧠 How to Use Spaced Repetition (guide page)
│
├── 📚 Resource Library
│   ├── [Database: Resource Library] — Full-page database
│   │   ├── View: Inbox (Table — filtered Status = Inbox)
│   │   ├── View: Currently Reading/Watching (Table — filtered Status = Reading/Watching)
│   │   ├── View: All Resources (Gallery — with URL previews)
│   │   ├── View: By Type (Board — grouped by Resource Type)
│   │   └── View: Completed & Rated (Table — filtered Status = Completed, sorted by Rating)
│   └── [Sub-page] 🔖 Bookmarklet Save Instructions
│
├── 🎯 Goals & Milestones
│   ├── [Database: Goals & Milestones] — Full-page database
│   │   ├── View: Active Goals (Table — filtered Status = Active, sorted by Target Date)
│   │   ├── View: By Type (Board — grouped by Goal Type)
│   │   ├── View: Completed Goals (Table — filtered Status = Completed)
│   │   └── View: Timeline (Timeline — by Target Date)
│   └── [Sub-page] 🏆 Goal-Setting Framework (SMART goal guide)
│
└── ⚙️ Settings & Setup
    ├── [Sub-page] 🗂️ Template Instructions & Getting Started
    ├── [Sub-page] 🏷️ Tag Taxonomy Reference (master list of tags used)
    └── [Sub-page] 🔗 Database Relation Map (visual diagram of all connections)
```

---

### Database Relation Map (Summary)

```
Courses & Subjects ◄────── Notes & Summaries
        │                        │
        ▼                        ▼
Study Sessions ◄──────── Review Queue
        │
        ▼
Goals & Milestones
        │
        ▼
Resource Library (loosely linked via Related Course)
```

---

## 4. Getting-Started Flow (3 Steps)

---

### ✅ Step 1: Add Your First Course or Subject

Navigate to **🎓 My Courses** and open the **All Courses** table view. Click **+ New**