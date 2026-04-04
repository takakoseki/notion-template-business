# Notion Template Design Specification

**Theme:** Personal Finance

---

# Personal Finance & Investment Clarity Hub — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most individual investors and personal finance enthusiasts juggle multiple spreadsheets, brokerage dashboards, and note apps to track their financial life. This fragmentation creates blind spots: missed dividend payments, unclear ROI across asset classes, forgotten transaction costs, and no single view of net worth progression. This template consolidates **investment tracking, income/expense logging, goal setting, and performance analytics** into one cohesive Notion workspace — giving users the clarity to make confident, data-driven financial decisions.

### Primary Use Cases

- Tracking investment portfolio performance (stocks, ETFs, crypto, real estate, bonds)
- Logging distributions, dividends, and passive income received
- Calculating realized and unrealized profit/loss per holding
- Monitoring ROI across different asset classes and time horizons
- Budgeting monthly income and expenses alongside investment activity
- Setting and tracking progress toward financial goals (e.g., emergency fund, retirement, house down payment)
- Reviewing historical performance with a monthly/quarterly snapshot log

---

### Target User Persona

**Name:** Alex, 32 — The Clarity-Seeking DIY Investor

**Background:**
Alex works a full-time job in marketing, earns a comfortable income, and has been investing for 4–6 years through a mix of brokerage accounts, a 401(k), and some crypto holdings. Alex is not a financial professional but is financially literate and wants to be more intentional with money.

**Pain Points:**
- Has three separate spreadsheets and two brokerage apps but no unified picture
- Forgets to log dividend payments and loses track of total income from investments
- Cannot quickly answer "What is my actual ROI on Tesla?" or "How much passive income did I earn this quarter?"
- Struggles to see whether spending habits are aligned with financial goals

**Goals:**
- Achieve a clear, real-time snapshot of total net worth and portfolio performance
- Build toward a $500,000 investment portfolio by age 45
- Generate $2,000/month in passive income from dividends/distributions within 5 years
- Reduce unnecessary expenses by 15% over the next year

**Tech Comfort Level:** Intermediate Notion user — comfortable with databases, filters, and basic formulas, but does not want to build from scratch.

**Usage Frequency:** Updates the template weekly (investment entries), monthly (budget review, goal check-ins), and quarterly (performance snapshots).

---

## 2. Notion Database List and Column Definitions

### Database 1: 📊 Investment Holdings

**Purpose:** Master ledger of every investment position currently held. Each entry represents one distinct holding (e.g., Apple stock in Brokerage A, Bitcoin in Exchange B). This is the central database that feeds into most rollups and formulas across the template.

| Column Name | Data Type | Description |
|---|---|---|
| Asset Name | Title (Text) | Name of the investment (e.g., "Apple Inc.", "Vanguard S&P 500 ETF", "Bitcoin") |
| Ticker / Symbol | Text | Stock ticker, crypto symbol, or fund identifier (e.g., AAPL, BTC, VOO) |
| Asset Class | Select | Category: Stocks / ETF / Crypto / Real Estate / Bonds / Cash / Other |
| Account / Broker | Select | Where this asset is held (e.g., Fidelity, Robinhood, Coinbase, Vanguard) |
| Number of Shares / Units | Number | Total quantity of units currently held |
| Average Cost Basis (per unit) | Number | Average price paid per unit, including fees, formatted as currency |
| Total Cost Basis | Formula | `Number of Shares × Average Cost Basis` — total amount invested |
| Current Price (per unit) | Number | Most recently updated market price per unit |
| Current Market Value | Formula | `Number of Shares × Current Price` — current portfolio value of this position |
| Unrealized Gain/Loss ($) | Formula | `Current Market Value − Total Cost Basis` |
| Unrealized Gain/Loss (%) | Formula | `(Unrealized Gain/Loss $ / Total Cost Basis) × 100` |
| Total Distributions Received | Rollup | Sum of all distribution amounts from the Distributions database related to this holding |
| Total Realized Gain/Loss | Rollup | Sum of all realized gains from the Transactions database related to this holding |
| Overall ROI (%) | Formula | `((Current Market Value + Total Distributions + Total Realized G/L − Total Cost Basis) / Total Cost Basis) × 100` |
| Status | Select | Active / Closed / Watchlist |
| Date First Purchased | Date | The date of the very first purchase of this asset |
| Notes | Text | Free-form notes (e.g., investment thesis, rebalancing intentions) |
| Transactions | Relation | Links to all buy/sell entries in the Transactions database |
| Distributions | Relation | Links to all income events in the Distributions database |

---

### Database 2: 🔄 Transactions Log

**Purpose:** A chronological record of every buy and sell transaction across all investment accounts. Enables calculation of realized gains/losses and tracks cost basis changes over time.

| Column Name | Data Type | Description |
|---|---|---|
| Transaction Name | Title (Text) | Auto-label or manual label (e.g., "Buy AAPL — Jan 2024") |
| Holding | Relation | Links to the corresponding entry in the Investment Holdings database |
| Transaction Type | Select | Buy / Sell / Transfer In / Transfer Out / Reinvestment |
| Transaction Date | Date | Date the transaction was executed |
| Number of Units | Number | Quantity of shares/units bought or sold in this transaction |
| Price per Unit | Number | Execution price per unit at time of transaction |
| Transaction Fees | Number | Commissions or fees paid for this transaction |
| Gross Transaction Value | Formula | `Number of Units × Price per Unit` |
| Net Transaction Value | Formula | `Gross Value + Fees` (for buys) or `Gross Value − Fees` (for sells) |
| Realized Gain/Loss ($) | Number | Manually entered or calculated realized gain/loss for sell transactions |
| Account | Select | Which brokerage/exchange account this transaction occurred in |
| Notes | Text | Optional context (e.g., "DCA purchase", "Tax-loss harvesting") |

---

### Database 3: 💰 Distributions & Passive Income

**Purpose:** Tracks every dividend, interest payment, rental income distribution, staking reward, or other passive income event generated by investments. Critical for calculating true total ROI and passive income progress.

| Column Name | Data Type | Description |
|---|---|---|
| Distribution Name | Title (Text) | Descriptive label (e.g., "AAPL Q3 Dividend", "BTC Staking Reward") |
| Holding | Relation | Links to the associated holding in the Investment Holdings database |
| Distribution Type | Select | Dividend / Interest / Rental Income / Staking Reward / Capital Gain Distribution / Other |
| Date Received | Date | Date the payment was received or credited |
| Amount Received ($) | Number | Gross amount of the distribution in dollars |
| Tax Withheld ($) | Number | Amount withheld for taxes, if applicable |
| Net Amount ($) | Formula | `Amount Received − Tax Withheld` |
| Reinvested? | Checkbox | Whether the distribution was automatically reinvested (DRIP) |
| Account | Select | Which account received the distribution |
| Month | Formula | Extracts the month from Date Received for monthly rollup grouping |
| Quarter | Formula | Extracts quarter (Q1/Q2/Q3/Q4) for quarterly passive income reports |
| Notes | Text | Optional notes (e.g., "Special dividend", "Annual payout") |

---

### Database 4: 💳 Budget Tracker (Income & Expenses)

**Purpose:** Monthly personal finance ledger for tracking all non-investment income (salary, freelance, etc.) and expenses. Allows users to see how much cash is available for investing and whether spending aligns with financial goals.

| Column Name | Data Type | Description |
|---|---|---|
| Entry Name | Title (Text) | Name of the income/expense (e.g., "Monthly Salary", "Spotify Subscription") |
| Type | Select | Income / Fixed Expense / Variable Expense / Investment Contribution / Savings |
| Category | Multi-select | Housing / Food / Transport / Entertainment / Healthcare / Insurance / Utilities / Education / Investing / Other |
| Amount ($) | Number | Dollar amount of the entry |
| Frequency | Select | One-time / Monthly / Quarterly / Annual |
| Date | Date | Date of the transaction or pay period |
| Month | Formula | Derived month label for grouping (e.g., "2024-03") |
| Planned vs. Actual | Select | Planned / Actual |
| Linked Goal | Relation | Optional link to a Financial Goal this expense/saving supports |
| Notes | Text | Additional context or memo |

---

### Database 5: 🎯 Financial Goals

**Purpose:** Tracks specific, measurable financial goals with progress monitoring. Each goal is linked to budget entries and can be manually updated with current saved amounts for progress visualization.

| Column Name | Data Type | Description |
|---|---|---|
| Goal Name | Title (Text) | Name of the goal (e.g., "Emergency Fund", "House Down Payment", "$500K Portfolio") |
| Goal Type | Select | Emergency Fund / Investment Target / Debt Payoff / Savings / Passive Income / Retirement / Other |
| Target Amount ($) | Number | The dollar target for this goal |
| Current Amount ($) | Number | Current progress amount (manually updated or tracked via linked entries) |
| Progress (%) | Formula | `(Current Amount / Target Amount) × 100` |
| Target Date | Date | Deadline or target completion date |
| Monthly Contribution Needed | Formula | `(Target Amount − Current Amount) / Months Until Target Date` |
| Priority | Select | High / Medium / Low |
| Status | Select | Not Started / In Progress / On Track / At Risk / Completed |
| Related Budget Entries | Relation | Links to Budget Tracker entries that contribute to this goal |
| Notes | Text | Strategy notes, milestones, or motivation |

---

### Database 6: 📅 Monthly Snapshot Log

**Purpose:** A quarterly/monthly record of key financial metrics captured at a point in time. This creates a historical performance timeline so users can visualize net worth growth and portfolio performance over months and years.

| Column Name | Data Type | Description |
|---|---|---|
| Snapshot Name | Title (Text) | Label for the snapshot (e.g., "March 2024 Snapshot") |
| Snapshot Date | Date | Date the snapshot was taken (typically month-end) |
| Total Portfolio Value ($) | Number | Manually entered total market value of all holdings at snapshot date |
| Total Cost Basis ($) | Number | Total amount invested as of snapshot date |
| Unrealized Gain/Loss ($) | Number | Portfolio value minus cost basis at snapshot date |
| Total Distributions YTD ($) | Number | Cumulative passive income received year-to-date |
| Total Realized Gains YTD ($) | Number | Cumulative realized gains/losses year-to-date |
| Net Worth Estimate ($) | Number | Rough total net worth at snapshot (assets minus liabilities) |
| Monthly Savings Rate (%) | Number | Percentage of income saved/invested this month |
| Notes / Highlights | Text | Key events, market conditions, or decisions made this month |

---

## 3. Page Structure

```
📁 Personal Finance & Investment Clarity Hub  ← Top-Level Page (Dashboard)
│
├── 🏠 HOME DASHBOARD                         ← Main landing page with linked views
│   ├── [Callout] Quick Stats Bar
│   │   ├── Total Portfolio Value (linked number)
│   │   ├── Total Unrealized Gain/Loss
│   │   ├── Passive Income This Month
│   │   └── Top Performing Asset
│   ├── [Gallery View] Active Holdings — card view of top positions
│   ├── [Chart View] Portfolio by Asset Class — pie chart via board grouping
│   ├── [Gallery View] Financial Goals — progress bars
│   └── [List View] Recent Transactions (last 10)
│
├── 📊 PORTFOLIO                              ← Sub-page
│   ├── [Full Database View] Investment Holdings
│   │   ├── View: All Holdings (Table)
│   │   ├── View: By Asset Class (Board)
│   │   ├── View: By Account (Board)
│   │   ├── View: Watchlist (Filtered)
│   │   └── View: Top Performers (Sorted by ROI%)
│   └── 📋 Holdings Detail Pages
│       └── (Each holding opens as a full Notion page with transaction history)
│
├── 🔄 TRANSACTIONS                           ← Sub-page
│   ├── [Full Database View] Transactions Log
│   │   ├── View: All Transactions (Table, sorted by date)
│   │   ├── View: Buys Only (Filtered)
│   │   ├── View: Sells Only (Filtered)
│   │   └── View: This Year (Date filtered)
│   └── [Callout] Instructions for logging a new transaction
│
├── 💰 PASSIVE INCOME                         ← Sub-page
│   ├── [Full Database View] Distributions & Passive Income
│   │   ├── View: All Distributions (Table)
│   │   ├── View: By Month (Group by Month formula)
│   │   ├── View: By Distribution Type (Group by Type)
│   │   └── View: This Quarter (Date filtered)
│   ├── [Callout] Monthly Passive Income Total (manual summary)
│   └── [Callout] Quarterly Passive Income Total (manual summary)
│
├── 💳 BUDGET                                 ← Sub-page
│   ├── [Full Database View] Budget Tracker
│   │   ├── View: This Month — All Entries (Filtered by current month)
│   │   ├── View: Income Only (Filtered by Type = Income)
│   │   ├── View: Expenses by Category (Group by Category)
│   │   ├── View: Planned vs. Actual (Group by Planned vs Actual)
│   │   └── View: Annual Overview (Table, grouped by Month formula)
│   └── [Callout] Monthly Budget Summary (Net Income after expenses)
│
├── 🎯 GOALS                                  ← Sub-page
│   ├── [Full Database View] Financial Goals
│   │   ├── View: All Goals (Gallery with progress bar)
│   │   ├── View: By Priority (Board grouped by Priority)
│   │   ├── View: Active Goals (Status ≠ Completed)
│   │   └── View: Completed Goals (Status = Completed)
│   └── [Callout] Goal-Setting Instructions & Tips
│
├── 📅 MONTHLY SNAPSHOTS                      ← Sub-page
│   ├── [Full Database View] Monthly Snapshot Log
│   │   ├── View: All Snapshots (Table, newest first)
│   │   └── View: Net Worth Timeline (sorted chronologically)
│   └── [Callout] How to take your monthly snapshot (instructions)
│
└── 📖 GUIDE & SETTINGS                       ← Sub-page
    ├── [Page] How to Use This Template
    ├── [Page] Formula Reference Sheet
    ├── [Page] Account & Broker List (customize your Select options)
    └── [Page] Glossary of Terms
```

---

### Database Placement Summary

| Database | Primary Location | Also Referenced In |
|---|---|---|
| Investment Holdings | 📊 PORTFOLIO page | HOME DASHBOARD (gallery view), PASSIVE INCOME (via relation) |
| Transactions Log | 🔄 TRANSACTIONS page | PORTFOLIO (linked from each holding's detail page) |
| Distributions & Passive Income | 💰 PASSIVE INCOME page | HOME DASHBOARD (summary callout), PORTFOLIO (rollup in holdings) |
| Budget Tracker | 💳 BUDGET page | GOALS (linked entries) |
| Financial Goals | 🎯 GOALS page | HOME DASHBOARD (gallery view) |
| Monthly Snapshot Log | 📅 MONTHLY SNAPSHOTS page | HOME DASHBOARD (linked summary) |

---

## 4. Getting-Started Flow (3 Steps)

---

### ✅ Step 1: Set Up Your Holdings — Enter What You Own

> **Time required: 15–30 minutes**

Navigate to the **📊 PORTFOLIO** page and open the **Investment Holdings** database. For every investment you currently own — stocks, ETFs, crypto,