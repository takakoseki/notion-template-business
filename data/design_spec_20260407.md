# Notion Template Design Specification

**Theme:** Personal Finance

---

# Personal Finance & Investment Clarity Hub — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most individual investors and personal finance enthusiasts struggle with **fragmented financial data** scattered across brokerage apps, spreadsheets, bank portals, and mental notes. They lack a single, unified view that answers the three most critical questions:

> *"How much have I invested? How much have I made? And where does my money actually go?"*

This template consolidates **investment tracking, income/expense management, distribution logging, and ROI calculation** into one cohesive Notion workspace — eliminating the need for multiple tools and providing instant, visual clarity over personal financial health.

---

### Primary Use Cases

| Use Case | Description |
|---|---|
| **Investment Portfolio Tracking** | Log stocks, ETFs, crypto, real estate, and other assets with cost basis, current value, and realized/unrealized gains |
| **Distribution & Dividend Logging** | Record every dividend, interest payment, and capital distribution received |
| **ROI Calculation** | Automatically calculate return on investment per asset and across the entire portfolio |
| **Monthly Budget & Expense Tracking** | Set monthly budgets by category and track actual spending against targets |
| **Income Stream Management** | Log all income sources — salary, freelance, dividends, rental — in one place |
| **Net Worth Monitoring** | Aggregate assets and liabilities for a running net worth snapshot |
| **Goal Setting & Progress Tracking** | Define financial goals (e.g., emergency fund, retirement target) and track progress |

---

### Detailed Target User Persona

**Primary Persona — "The Intentional Individual Investor"**

| Attribute | Details |
|---|---|
| **Name (Archetype)** | Alex, 32 |
| **Occupation** | Mid-level software engineer / marketing manager / freelance consultant |
| **Income Range** | $60,000 – $150,000/year |
| **Investment Experience** | Intermediate — has been investing for 2–6 years, holds a mix of index funds, individual stocks, and possibly some crypto |
| **Current Pain Points** | Uses 3–4 different brokerage apps, has a dusty spreadsheet that never gets updated, doesn't know true ROI, loses track of dividends received |
| **Tech Comfort** | Comfortable with Notion; not a developer but can follow structured systems |
| **Goals** | Achieve financial independence, hit a specific net worth milestone by a target year, understand whether their investments are actually performing |
| **Behavior** | Reviews finances once a week or monthly; wants a system that requires minimal maintenance but gives maximum insight |

**Secondary Persona — "The Budget-Conscious Planner"**

| Attribute | Details |
|---|---|
| **Profile** | 25–35, building wealth from scratch, focused on saving rate and debt paydown |
| **Key Needs** | Expense categorization, savings rate tracking, goal milestones |
| **Template Usage** | Primarily uses Budget, Income, and Goals sections; investment section grows over time |

---

## 2. Notion Database List and Column Definitions

---

### Database 1: 📊 Investment Portfolio

**Purpose:** The core database. Tracks every investment position — when purchased, at what cost, current value, and calculated performance metrics.

| Column Name | Data Type | Description |
|---|---|---|
| **Asset Name** | Title (Text) | Name of the investment (e.g., "Apple Inc.", "Vanguard S&P 500 ETF", "Bitcoin") |
| **Ticker / Symbol** | Text | Trading symbol or identifier (e.g., AAPL, BTC, VTI) |
| **Asset Class** | Select | Category: `Stocks` / `ETFs` / `Crypto` / `Real Estate` / `Bonds` / `Cash Equivalents` / `Other` |
| **Account** | Relation | Links to **🏦 Accounts** database — which brokerage/wallet holds this asset |
| **Purchase Date** | Date | Date the position was opened or shares were first acquired |
| **Shares / Units Held** | Number | Total quantity of shares, coins, or units currently held |
| **Average Cost Per Share** | Number | Average purchase price per unit (cost basis per share) |
| **Total Cost Basis** | Formula | `Shares / Units Held × Average Cost Per Share` — total amount invested in this position |
| **Current Price Per Share** | Number | Manually updated current market price per unit |
| **Current Market Value** | Formula | `Shares / Units Held × Current Price Per Share` |
| **Unrealized Gain / Loss ($)** | Formula | `Current Market Value − Total Cost Basis` |
| **Unrealized ROI (%)** | Formula | `(Unrealized Gain / Loss ÷ Total Cost Basis) × 100` |
| **Total Distributions Received** | Rollup | Rolls up **Sum** of `Amount` from related **💸 Distributions** entries |
| **Total Return ($)** | Formula | `Unrealized Gain / Loss ($) + Total Distributions Received` |
| **Total ROI (%)** | Formula | `(Total Return ÷ Total Cost Basis) × 100` |
| **Status** | Select | `Active` / `Closed` / `Watchlist` |
| **Sector / Industry** | Select | Technology / Healthcare / Financials / Energy / Consumer / Industrials / Real Estate / Other |
| **Notes** | Text | Investment thesis, reminders, research notes |
| **Last Updated** | Date | Date the Current Price was last manually refreshed |
| **Tags** | Multi-select | Custom labels: `Core Holding` / `Speculative` / `Dividend` / `Long-Term` / `Tax-Advantaged` |

---

### Database 2: 💸 Distributions & Income Events

**Purpose:** Logs every cash distribution event tied to an investment — dividends, interest, rental income distributions, staking rewards, capital gains distributions.

| Column Name | Data Type | Description |
|---|---|---|
| **Distribution Name** | Title (Text) | Auto-named or custom label (e.g., "AAPL Q2 Dividend", "VTI Annual Distribution") |
| **Asset** | Relation | Links to **📊 Investment Portfolio** — which investment generated this distribution |
| **Distribution Type** | Select | `Dividend` / `Interest` / `Capital Gain Distribution` / `Rental Distribution` / `Staking Reward` / `Other` |
| **Amount** | Number | Cash received in dollars (or base currency) |
| **Per Share Amount** | Number | Distribution amount per share/unit (optional, for reference) |
| **Ex-Date** | Date | Date the asset was ex-dividend / ex-distribution |
| **Payment Date** | Date | Date the cash was actually received |
| **Reinvested?** | Checkbox | Check if this distribution was reinvested (DRIP) rather than taken as cash |
| **Account** | Relation | Links to **🏦 Accounts** — which account received the payment |
| **Tax Year** | Select | `2022` / `2023` / `2024` / `2025` (for tax reporting grouping) |
| **Qualified?** | Checkbox | Whether the dividend qualifies for lower tax rates |
| **Notes** | Text | Any relevant details, anomalies, or reminders |

---

### Database 3: 🏦 Accounts

**Purpose:** Defines all financial accounts (brokerage, bank, crypto wallet, retirement) so investments and transactions can be correctly attributed.

| Column Name | Data Type | Description |
|---|---|---|
| **Account Name** | Title (Text) | Descriptive name (e.g., "Fidelity Taxable", "Roth IRA – Vanguard", "Coinbase") |
| **Institution** | Text | Name of the financial institution or platform |
| **Account Type** | Select | `Taxable Brokerage` / `Traditional IRA` / `Roth IRA` / `401(k)` / `HSA` / `Crypto Wallet` / `Checking` / `Savings` / `Other` |
| **Currency** | Select | `USD` / `EUR` / `GBP` / `CAD` / `Other` |
| **Account Number (Last 4)** | Text | Last 4 digits only, for identification (never full number) |
| **Cash Balance** | Number | Current uninvested cash held in the account |
| **Total Invested (Rollup)** | Rollup | Rolls up **Sum** of `Total Cost Basis` from linked **📊 Investment Portfolio** entries |
| **Total Market Value (Rollup)** | Rollup | Rolls up **Sum** of `Current Market Value` from linked positions |
| **Account URL / Login Page** | URL | Link to institution login page for quick access |
| **Tax-Advantaged?** | Checkbox | Whether the account has tax advantages (IRA, 401k, HSA) |
| **Notes** | Text | Contribution limits, beneficiaries, special notes |
| **Status** | Select | `Active` / `Inactive` / `Closed` |

---

### Database 4: 💰 Income Log

**Purpose:** Tracks all income received across every source — salary, freelance, side hustles, investment income. Provides a complete picture of money coming in.

| Column Name | Data Type | Description |
|---|---|---|
| **Income Entry** | Title (Text) | Descriptive label (e.g., "March Salary", "Client Project – Website Build") |
| **Amount** | Number | Gross income received |
| **Net Amount** | Number | Take-home amount after taxes/deductions (if known) |
| **Income Type** | Select | `Salary` / `Freelance` / `Business` / `Rental` / `Dividend` / `Interest` / `Capital Gain` / `Gift` / `Other` |
| **Source** | Text | Employer, client name, or platform (e.g., "Acme Corp", "Upwork") |
| **Date Received** | Date | Date the income was deposited or received |
| **Month** | Formula | `formatDate(Date Received, "MMMM YYYY")` — for grouping by month |
| **Account** | Relation | Links to **🏦 Accounts** — where the income was deposited |
| **Tax Year** | Select | `2023` / `2024` / `2025` |
| **Taxable?** | Checkbox | Whether this income is subject to income tax |
| **Category Tag** | Multi-select | `Primary Income` / `Passive` / `Active` / `One-Time` / `Recurring` |
| **Notes** | Text | Invoice numbers, payer details, any relevant context |

---

### Database 5: 💳 Expenses & Budget Tracker

**Purpose:** Logs every expense and compares it against monthly budgets by category to reveal spending patterns and savings opportunities.

| Column Name | Data Type | Description |
|---|---|---|
| **Expense Name** | Title (Text) | What the expense was (e.g., "Whole Foods Grocery Run", "Netflix Subscription") |
| **Amount** | Number | Amount spent |
| **Category** | Select | `Housing` / `Food & Groceries` / `Transport` / `Utilities` / `Healthcare` / `Entertainment` / `Subscriptions` / `Investments` / `Education` / `Travel` / `Personal Care` / `Debt Payments` / `Other` |
| **Date** | Date | Date the expense occurred or was charged |
| **Month** | Formula | `formatDate(Date, "MMMM YYYY")` — for monthly grouping |
| **Payment Method** | Select | `Credit Card` / `Debit Card` / `Cash` / `Bank Transfer` / `PayPal` / `Other` |
| **Account** | Relation | Links to **🏦 Accounts** — which account was charged |
| **Vendor / Merchant** | Text | Name of the store, company, or payee |
| **Recurring?** | Checkbox | Is this a regular monthly/annual charge? |
| **Essential?** | Checkbox | Is this a need vs. a want? (useful for discretionary analysis) |
| **Receipt URL** | URL | Link to digital receipt stored in cloud (optional) |
| **Notes** | Text | Any context, split expense details, reimbursement notes |
| **Tags** | Multi-select | Custom spend labels: `Business Expense` / `Reimbursable` / `One-Time` |

---

### Database 6: 📅 Monthly Budget Targets

**Purpose:** Defines the planned spending limit per category per month, against which actual expenses (from the Expenses database) are compared.

| Column Name | Data Type | Description |
|---|---|---|
| **Budget Entry** | Title (Text) | Auto-label: Category + Month (e.g., "Food & Groceries – March 2025") |
| **Category** | Select | Mirrors the Category options from **💳 Expenses** database |
| **Month / Year** | Date | Set to the first day of the applicable month |
| **Budgeted Amount** | Number | Planned spending target for this category in this month |
| **Notes** | Text | Reasoning behind budget amount, seasonal adjustments |

> 💡 **Designer Note:** Actual vs. Budget comparison is displayed on the Dashboard using filtered views and linked databases — Notion doesn't natively support cross-database rollups without Relations, so a summary section using Callout blocks with manually updated totals or a linked view with filters by month is recommended.

---

### Database 7: 🎯 Financial Goals

**Purpose:** Tracks specific, measurable financial milestones — from building an emergency fund to hitting a retirement portfolio target.

| Column Name | Data Type | Description |
|---|---|---|
| **Goal Name** | Title (Text) | Name of the financial goal (e.g., "6-Month Emergency Fund", "Invest $50,000 by 2026") |
| **Goal Type** | Select | `Savings` / `Investment` / `Debt Paydown` / `Income` / `Net Worth` / `Other` |
| **Target Amount ($)** | Number | The dollar amount to be reached |
| **Current Amount ($)** | Number | Manually updated current progress amount |
| **Progress (%)** | Formula | `(Current Amount ÷ Target Amount) × 100` |
| **Target Date** | Date | Deadline or milestone date |
| **Months Remaining** | Formula | Approximate months between today and Target Date (using `dateBetween`) |
| **Status** | Select | `Not Started` / `In Progress` / `Achieved` / `Paused` / `Abandoned` |
| **Priority** | Select | `🔴 High` / `🟡 Medium` / `🟢 Low` |
| **Account / Fund** | Relation | Links to **🏦 Accounts** — where the savings/investment lives |
| **Milestone Notes** | Text | Breakdown of sub-milestones, strategy description |
| **Achieved Date** | Date | Date the goal was actually completed |
| **Celebration Note** | Text | A fun personal note when the goal is hit 🎉 |

---

### Database 8: 📋 Assets & Liabilities (Net Worth)

**Purpose:** A snapshot-style database for tracking all assets and liabilities to calculate net worth over time.

| Column Name | Data Type | Description |
|---|---|---|
| **Item Name** | Title (Text) | Name of the asset or liability (e.g., "Primary Residence", "Student Loan", "Car") |
| **Type** | Select | `Asset` / `Liability` |
| **Sub-Category** | Select | `Real Estate` / `Vehicle` / `Cash` / `Investment Account` / `Business Equity` / `Mortgage` / `Student Loan` / `Credit Card Debt` / `Personal Loan` / `Other` |
| **Value / Balance** | Number | Current estimated value (assets) or outstanding balance (liabilities) |
| **As Of Date** | Date | Date this value was last verified/updated |
| **Interest Rate (%)** | Number | For liabilities — the APR or interest rate |
| **Linked Account** | Relation | Links to **🏦 Accounts** if applicable |
| **Notes** | Text | Details, lender name, appraisal source, etc. |

---

## 3. Page Structure

```
📁 Personal Finance & Investment Clarity Hub  [Top-Level Page]
│
├── 🏠 Dashboard  [Primary landing page — no database, aggregates views]
│     ├── 💎 Net Worth Summary  [Callout block + linked DB view: Assets & Liabilities]
│     ├── 📊 Portfolio Overview  [Linked view of Investment Portfolio — Gallery/Table]
│     ├── 💸 Recent