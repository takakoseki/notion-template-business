# Notion Template Design Specification

**Theme:** Personal Finance

---

# Personal Finance & Investment Clarity Hub — Notion Template Design Specification

---

## 1. Purpose and Target Users

### Problem This Template Solves

Most individual investors and personal finance enthusiasts struggle with fragmented financial data scattered across brokerage apps, spreadsheets, bank portals, and note-taking apps. They lack a **single, unified view** of their net worth, investment performance, income streams, and spending habits. Specifically, they cannot easily answer critical questions like:

- *"What is my actual ROI on each investment after fees and taxes?"*
- *"How much passive income (dividends, distributions) did I receive this quarter?"*
- *"Am I on track toward my savings and investment goals?"*
- *"Where is my money actually going every month?"*

This template eliminates that fragmentation by providing a **centralized personal finance command center** inside Notion — one workspace to track investments, transactions, income, goals, and net worth snapshots.

---

### Primary Use Cases

| Use Case | Description |
|---|---|
| **Investment Portfolio Tracking** | Log stocks, ETFs, crypto, real estate, and alternative assets; track cost basis, current value, and realized/unrealized gains |
| **Dividend & Distribution Logging** | Record every distribution event with date, amount, and source; auto-roll up annual income per asset |
| **Monthly Budget Monitoring** | Track income vs. expenses by category; compare actual spending against budget targets |
| **Net Worth Snapshot** | Monthly balance-sheet-style snapshots of assets and liabilities |
| **Financial Goal Setting** | Define savings, investment, and debt-payoff goals with progress tracking |
| **Tax Preparation Support** | Organized records of capital gains, distributions, and deductible expenses |

---

### Detailed Target User Persona

**Primary Persona — "The Clarity-Seeking Investor"**

> **Name:** Alex, 32
> **Occupation:** Software Engineer / Mid-level Professional
> **Income:** $90,000–$140,000/year
> **Financial Situation:** Has a 401(k), a brokerage account with 15–30 individual positions (stocks + ETFs), a small crypto portfolio, and a high-yield savings account. Recently started receiving quarterly dividends.

**Pain Points:**
- Opens 4–5 different apps to get a complete financial picture
- Has no easy way to calculate true ROI accounting for multiple buy-ins at different prices
- Forgets to log dividend income and loses track of annual totals
- Budgeting is done reactively (at month end) rather than proactively
- Spends 2–3 hours preparing data every tax season

**Goals:**
- Achieve financial independence by age 45
- Build a passive income stream of $2,000/month from dividends
- Maintain a clear, up-to-date net worth statement
- Reduce lifestyle inflation as income grows

**Notion Experience Level:** Intermediate — comfortable with databases, filters, and views; does not want to build complex formulas from scratch.

**Secondary Persona — "The Organized Saver"**

> A 25–35 year old early in their career who is focused on budgeting, building an emergency fund, and making first investments. Less investment-heavy, more budget and goal oriented. Needs the template to be approachable and motivational.

---

## 2. Notion Database List and Column Definitions

---

### Database 1: 💼 Investment Portfolio

**Purpose:** The master ledger of every investment position held. Each row represents one unique holding (one ticker/asset per account, or one row per lot if tracking tax lots separately).

| Column Name | Data Type | Description |
|---|---|---|
| **Asset Name** | Title (Text) | Name of the investment (e.g., "Apple Inc.", "Vanguard S&P 500 ETF", "Bitcoin") |
| **Ticker / Symbol** | Text | Ticker symbol or identifier (e.g., AAPL, VOO, BTC) |
| **Asset Class** | Select | Category: `Stocks`, `ETFs`, `Crypto`, `Real Estate`, `Bonds`, `Alternatives`, `Cash Equivalents` |
| **Account** | Relation → Accounts DB | Which account holds this asset |
| **Shares / Units** | Number | Total quantity owned (supports decimal for crypto) |
| **Average Cost Basis (per unit)** | Number | Average price paid per share/unit across all purchases |
| **Total Cost Basis** | Formula | `Shares / Units × Average Cost Basis (per unit)` — total amount invested |
| **Current Price (per unit)** | Number | Manually updated current market price per share/unit |
| **Current Market Value** | Formula | `Shares / Units × Current Price (per unit)` |
| **Unrealized Gain / Loss ($)** | Formula | `Current Market Value − Total Cost Basis` |
| **Unrealized Gain / Loss (%)** | Formula | `(Unrealized Gain / Loss $ ÷ Total Cost Basis) × 100` |
| **Realized Gains (Rollup)** | Rollup | Sum of `Realized Gain/Loss $` from related Transaction Log rows where Type = "Sell" |
| **Total Distributions Received** | Rollup | Sum of `Amount` from related Distribution Log rows |
| **Total Return ($)** | Formula | `Unrealized Gain/Loss $ + Realized Gains + Total Distributions Received` |
| **Total ROI (%)** | Formula | `(Total Return $ ÷ Total Cost Basis) × 100` |
| **Dividend Yield (%)** | Number | Manually entered annual yield percentage (from brokerage or financial site) |
| **Sector** | Select | `Technology`, `Healthcare`, `Financials`, `Energy`, `Consumer Discretionary`, `Utilities`, `Real Estate`, `Industrials`, `Materials`, `Communication`, `Other` |
| **Country / Region** | Select | `USA`, `International Developed`, `Emerging Markets`, `Global`, `Other` |
| **Status** | Select | `Active`, `Closed`, `Watching` |
| **First Purchase Date** | Date | Date of first buy for this holding |
| **Notes** | Text | Investment thesis, reminders, research notes |
| **Link to Research** | URL | Link to financial report, article, or analysis |

---

### Database 2: 📋 Transaction Log

**Purpose:** A granular record of every buy, sell, or transfer event. Each row is one transaction. This is the source of truth for calculating realized gains and tracking trade history.

| Column Name | Data Type | Description |
|---|---|---|
| **Transaction ID** | Title (Text) | Auto-label or manual identifier (e.g., "AAPL-BUY-2024-03-15") |
| **Date** | Date | Date the transaction was executed |
| **Asset** | Relation → Investment Portfolio | The asset involved in this transaction |
| **Transaction Type** | Select | `Buy`, `Sell`, `Transfer In`, `Transfer Out`, `Dividend Reinvestment (DRIP)` |
| **Account** | Relation → Accounts DB | Account where transaction occurred |
| **Shares / Units** | Number | Number of shares/units bought or sold |
| **Price per Unit** | Number | Execution price per share/unit |
| **Total Amount** | Formula | `Shares / Units × Price per Unit` |
| **Fees / Commissions** | Number | Any trading fees or commissions paid |
| **Net Amount** | Formula | `Total Amount + Fees / Commissions` (cost for buys; proceeds for sells) |
| **Realized Gain / Loss ($)** | Number | For sell transactions only: manually enter or calculate realized gain/loss |
| **Holding Period** | Select | `Short-term (<1 year)`, `Long-term (≥1 year)` — for tax classification |
| **Notes** | Text | Reason for trade, market context, or broker confirmation number |

---

### Database 3: 💰 Distribution & Income Log

**Purpose:** Track every passive income event — dividends, ETF distributions, rental income, interest payments. Rolled up into the Investment Portfolio for total return calculations.

| Column Name | Data Type | Description |
|---|---|---|
| **Distribution ID** | Title (Text) | Auto-label (e.g., "VOO-DIV-Q1-2024") |
| **Date Received** | Date | Date the distribution was credited to the account |
| **Asset** | Relation → Investment Portfolio | Source investment that generated the income |
| **Account** | Relation → Accounts DB | Account that received the payment |
| **Distribution Type** | Select | `Ordinary Dividend`, `Qualified Dividend`, `Capital Gain Distribution`, `Return of Capital`, `Interest`, `Rental Income`, `Other` |
| **Amount ($)** | Number | Gross amount received before taxes |
| **Tax Withheld ($)** | Number | Any taxes withheld at source |
| **Net Amount ($)** | Formula | `Amount $ − Tax Withheld $` |
| **Reinvested?** | Checkbox | Whether the distribution was automatically reinvested (DRIP) |
| **Quarter** | Select | `Q1`, `Q2`, `Q3`, `Q4` — for easy quarterly reporting |
| **Tax Year** | Number | The tax year this income belongs to (e.g., 2024) |
| **Notes** | Text | Any relevant notes (e.g., special distribution, one-time event) |

---

### Database 4: 🏦 Accounts

**Purpose:** Master list of all financial accounts. Used as a relation anchor for Portfolio, Transactions, and Distributions, enabling filtering by account.

| Column Name | Data Type | Description |
|---|---|---|
| **Account Name** | Title (Text) | Friendly name (e.g., "Fidelity Brokerage", "Coinbase", "Chase Checking") |
| **Institution** | Text | Name of the financial institution or platform |
| **Account Type** | Select | `Taxable Brokerage`, `401(k)`, `IRA (Traditional)`, `IRA (Roth)`, `HSA`, `Checking`, `Savings`, `Crypto Exchange`, `Real Estate`, `Other` |
| **Currency** | Select | `USD`, `EUR`, `GBP`, `CAD`, `Other` |
| **Current Balance** | Number | Manually updated current account balance |
| **Account Number (Last 4)** | Text | Last 4 digits for identification (security-conscious) |
| **Tax Treatment** | Select | `Taxable`, `Tax-Deferred`, `Tax-Free` |
| **Status** | Select | `Active`, `Closed` |
| **Opened Date** | Date | When the account was opened |
| **Notes / URL** | Text | Link to institution login or relevant notes |

---

### Database 5: 💳 Monthly Budget & Expenses

**Purpose:** Track monthly income and spending by category. Each row is one transaction or recurring budget entry. Used to build the monthly budget dashboard view.

| Column Name | Data Type | Description |
|---|---|---|
| **Description** | Title (Text) | Brief description (e.g., "March Rent", "Spotify Subscription", "Freelance Payment") |
| **Date** | Date | Date of transaction or budget period start |
| **Month** | Select | `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec` |
| **Year** | Number | Calendar year (e.g., 2024) |
| **Type** | Select | `Income`, `Fixed Expense`, `Variable Expense`, `Savings Transfer`, `Investment Contribution` |
| **Category** | Select | `Housing`, `Food & Groceries`, `Transportation`, `Utilities`, `Healthcare`, `Entertainment`, `Subscriptions`, `Clothing`, `Education`, `Travel`, `Personal Care`, `Gifts & Donations`, `Debt Payments`, `Investments`, `Emergency Fund`, `Salary`, `Freelance`, `Bonus`, `Side Income`, `Other` |
| **Budgeted Amount ($)** | Number | Planned amount for this category/period |
| **Actual Amount ($)** | Number | Real amount spent or received |
| **Variance ($)** | Formula | `Budgeted Amount − Actual Amount` (positive = under budget, negative = over budget) |
| **Account** | Relation → Accounts DB | Account used for this transaction |
| **Recurring?** | Checkbox | Whether this is a recurring monthly item |
| **Payment Method** | Select | `Cash`, `Credit Card`, `Debit Card`, `Bank Transfer`, `Auto-Pay`, `Check`, `Other` |
| **Receipt / Proof** | URL | Link to receipt image or file |
| **Notes** | Text | Additional context |

---

### Database 6: 🎯 Financial Goals

**Purpose:** Define and track progress toward specific financial targets — savings milestones, investment targets, debt payoff goals, and income goals.

| Column Name | Data Type | Description |
|---|---|---|
| **Goal Name** | Title (Text) | Name of the goal (e.g., "Emergency Fund", "Max Roth IRA 2024", "Pay Off Car Loan") |
| **Goal Type** | Select | `Savings`, `Investment`, `Debt Payoff`, `Income`, `Net Worth`, `Other` |
| **Target Amount ($)** | Number | The financial target to reach |
| **Current Progress ($)** | Number | Manually updated current amount saved/paid/invested |
| **Progress (%)** | Formula | `(Current Progress ÷ Target Amount) × 100` |
| **Progress Bar** | Formula | Visual text progress bar using formula (e.g., `"████░░░░░░ 40%"` using rounding logic) |
| **Target Date** | Date | Deadline or goal completion date |
| **Priority** | Select | `🔴 Critical`, `🟠 High`, `🟡 Medium`, `🟢 Low` |
| **Status** | Select | `Not Started`, `In Progress`, `On Track`, `At Risk`, `Completed`, `Paused` |
| **Linked Account** | Relation → Accounts DB | The account where progress is being tracked |
| **Monthly Contribution ($)** | Number | How much to contribute each month toward this goal |
| **Months to Goal** | Formula | `(Target Amount − Current Progress) ÷ Monthly Contribution` |
| **Notes / Strategy** | Text | Plan details, motivation notes, or strategy description |

---

### Database 7: 📊 Net Worth Snapshots

**Purpose:** Monthly point-in-time records of total assets, liabilities, and net worth. Enables trend visualization over time.

| Column Name | Data Type | Description |
|---|---|---|
| **Snapshot Label** | Title (Text) | Month-Year label (e.g., "January 2024") |
| **Date** | Date | Date snapshot was taken (typically the 1st or last day of the month) |
| **Total Investment Value ($)** | Number | Sum of all investment account values at snapshot date |
| **Cash & Savings ($)** | Number | Total liquid cash across checking and savings accounts |
| **Real Estate Value ($)** | Number | Estimated market value of real estate owned |
| **Other Assets ($)** | Number | Vehicles, business equity, collectibles, etc. |
| **Total Assets ($)** | Formula | `Total Investment Value + Cash & Savings + Real Estate Value + Other Assets` |
| **Mortgage / Loans ($)** | Number | Outstanding mortgage, student loans, auto loans |
| **Credit Card Debt ($)** | Number | Total revolving credit card balances |
| **Other Liabilities ($)** | Number | Any other debts |
| **Total Liabilities ($)** | Formula | `Mortgage / Loans + Credit Card Debt + Other Liabilities` |
| **Net Worth ($)** | Formula | `Total Assets − Total Liabilities` |
| **Month-over-Month Change ($)** | Number | Manually entered change from prior month (or tracked separately) |
| **Notes** | Text | Context for significant changes (market crash, big purchase, windfall, etc.) |

---

## 3. Page Structure

```
📁 PERSONAL FINANCE & INVESTMENT CLARITY HUB (Top-Level Page)
│
├── 🏠 DASHBOARD (Main Hub Page)
│   ├── 📌 Quick Stats (Linked DB Views — Summary Callout Blocks)
│   │     - Total Portfolio Value
│   │     - Total Distributions YTD
│   │     - Net Worth (Latest Snapshot)
│   │     - Monthly Budget Status (Income vs. Expenses)
│   ├── 📊 Net Worth Trend (Linked DB View → Net Worth Snapshots — Table/Chart)
│   ├── 🎯 Active Goals Overview (Linked DB View → Financial Goals — Board by Status)
│   ├── 💼 Portfolio Summary (Linked