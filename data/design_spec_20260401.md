# Notion Template Design Specification

**Theme:** Travel Planner

---

# Notion Template Design Specification: Travel Planner

---

## 1. Purpose and Target Users

### Problem This Template Solves

Planning a trip involves juggling dozens of moving parts — flights, accommodations, daily itineraries, budgets, packing lists, and travel documents — often scattered across multiple apps, spreadsheets, and notes. This template consolidates every aspect of trip planning into a single, structured Notion workspace, eliminating the chaos of context-switching and reducing the risk of missing critical details.

### Primary Use Cases

- **Pre-trip planning**: Researching destinations, comparing accommodation options, booking flights, and setting a budget
- **Active trip management**: Following day-by-day itineraries, tracking expenses in real time, and storing confirmation numbers
- **Post-trip archiving**: Saving memories, photos, notes, and lessons learned for future reference
- **Multi-destination trip coordination**: Managing complex itineraries spanning several cities or countries
- **Group travel coordination**: Sharing plans, splitting costs, and assigning tasks among travel companions

### Target User Persona

**Primary Persona: "The Organized Explorer"**

| Attribute | Detail |
|---|---|
| **Name** | Alex Chen |
| **Age** | 28–42 |
| **Occupation** | Mid-level professional (marketing manager, software developer, consultant) |
| **Travel frequency** | 3–6 trips per year (mix of solo, couple, and group travel) |
| **Tech comfort** | Comfortable with productivity tools; already uses Notion for work or personal projects |
| **Pain points** | Loses booking confirmations in email, overspends without realizing it, forgets to pack essentials, struggles to coordinate with travel companions |
| **Goals** | Travel stress-free, stay within budget, make the most of limited vacation days, keep all information in one accessible place |
| **Devices** | MacBook for planning, iPhone for on-the-go access via Notion mobile app |

**Secondary Persona: "The Adventure Couple"**

| Attribute | Detail |
|---|---|
| **Profile** | Two partners who plan trips together and need shared visibility |
| **Key need** | Both partners can view and edit the same plan, assign tasks to each other, and track shared expenses |
| **Usage pattern** | Heavy planning 4–6 weeks before departure; light usage during the trip for reference |

---

## 2. Notion Database List and Column Definitions

### Database 1: 🌍 Trip Overview

**Purpose**: The master database for all trips. Each entry represents one trip and serves as the parent record that all other databases link back to.

| Column Name | Data Type | Description |
|---|---|---|
| Trip Name | Title | Name of the trip (e.g., "Japan Spring 2025", "Barcelona Solo") |
| Destination(s) | Multi-select | Countries or cities being visited |
| Status | Select | Current state: `🧠 Planning` / `✅ Booked` / `🧳 In Progress` / `🏁 Completed` |
| Departure Date | Date | Date of first travel day (with time) |
| Return Date | Date | Date of last travel day (with time) |
| Duration (Days) | Formula | `dateBetween(prop("Return Date"), prop("Departure Date"), "days") + 1` |
| Travelers | Multi-select | Names of people going on the trip |
| Total Budget | Number (Currency) | Planned total budget for the trip in home currency |
| Total Spent | Rollup | Sum of all expenses linked to this trip from the Expenses database |
| Budget Remaining | Formula | `prop("Total Budget") - prop("Total Spent")` |
| Cover Photo | Files & Media | Hero image for the trip (city skyline, map, etc.) |
| Trip Notes | Text | Free-form notes, links to inspiration boards, or general reminders |
| Visa Required | Checkbox | Check if a visa is required for any destination |
| Visa Status | Select | `Not Required` / `Applied` / `Approved` / `Not Started` |

---

### Database 2: ✈️ Flights & Transport

**Purpose**: Tracks all transportation bookings including flights, trains, buses, and ferry rides for every trip.

| Column Name | Data Type | Description |
|---|---|---|
| Route | Title | Descriptive label (e.g., "NYC → Tokyo (Outbound)") |
| Trip | Relation | Links to the **Trip Overview** database |
| Transport Type | Select | `✈️ Flight` / `🚂 Train` / `🚌 Bus` / `⛴️ Ferry` / `🚗 Car Rental` / `🚕 Taxi/Rideshare` |
| Carrier / Operator | Text | Airline name, train company, etc. (e.g., "ANA", "Eurostar") |
| Booking Reference | Text | Confirmation number or PNR code |
| Departure Airport/Station | Text | IATA code or station name (e.g., "JFK", "Gare du Nord") |
| Arrival Airport/Station | Text | IATA code or station name |
| Departure Date & Time | Date | Scheduled departure (with time and timezone) |
| Arrival Date & Time | Date | Scheduled arrival (with time and timezone) |
| Duration | Formula | `dateBetween(prop("Arrival Date & Time"), prop("Departure Date & Time"), "hours") + " hrs"` |
| Seat/Class | Text | Seat number and class (e.g., "34A, Economy") |
| Price Paid | Number (Currency) | Total cost of this booking |
| Booking URL | URL | Link to booking website or confirmation page |
| Booking Status | Select | `🔖 To Book` / `⏳ Pending` / `✅ Confirmed` / `❌ Cancelled` |
| E-Ticket / Document | Files & Media | Uploaded PDF of ticket or boarding pass |
| Notes | Text | Baggage allowance, layover details, terminal info |

---

### Database 3: 🏨 Accommodations

**Purpose**: Manages all lodging across every trip, from hotels to Airbnbs to hostels.

| Column Name | Data Type | Description |
|---|---|---|
| Property Name | Title | Name of the hotel, Airbnb, hostel, etc. |
| Trip | Relation | Links to the **Trip Overview** database |
| Accommodation Type | Select | `🏨 Hotel` / `🏡 Airbnb/VRBO` / `🛏️ Hostel` / `🏕️ Camping` / `🏠 Friend/Family` / `🏢 Serviced Apartment` |
| City | Select | City where the property is located |
| Address | Text | Full street address |
| Google Maps Link | URL | Direct link to property on Google Maps |
| Check-in Date | Date | Date and time of check-in |
| Check-out Date | Date | Date and time of check-out |
| Nights | Formula | `dateBetween(prop("Check-out Date"), prop("Check-in Date"), "days")` |
| Price Per Night | Number (Currency) | Nightly rate in home currency |
| Total Cost | Formula | `prop("Price Per Night") * prop("Nights")` |
| Booking Reference | Text | Confirmation or reservation number |
| Booking Status | Select | `🔖 To Book` / `✅ Confirmed` / `❌ Cancelled` |
| Booking URL | URL | Link to booking platform |
| Rating | Select | Personal rating: `⭐` / `⭐⭐` / `⭐⭐⭐` / `⭐⭐⭐⭐` / `⭐⭐⭐⭐⭐` |
| WiFi Included | Checkbox | Whether free WiFi is available |
| Breakfast Included | Checkbox | Whether breakfast is included in the rate |
| Free Cancellation | Checkbox | Whether the booking can be cancelled without penalty |
| Cancellation Deadline | Date | Last date to cancel without fees |
| Confirmation Doc | Files & Media | Upload of booking confirmation PDF |
| Notes | Text | Check-in instructions, host contact, parking info |

---

### Database 4: 📅 Daily Itinerary

**Purpose**: The day-by-day, activity-by-activity schedule for each trip. This is the operational core used during the trip itself.

| Column Name | Data Type | Description |
|---|---|---|
| Activity Name | Title | Name of the activity or event (e.g., "Visit Senso-ji Temple") |
| Trip | Relation | Links to the **Trip Overview** database |
| Date | Date | Date and start time of the activity |
| Day Number | Formula | `dateBetween(prop("Date"), prop("Trip").prop("Departure Date"), "days") + 1` |
| Category | Select | `🗺️ Sightseeing` / `🍽️ Food & Dining` / `🎭 Entertainment` / `🛒 Shopping` / `🏖️ Beach/Nature` / `🏛️ Museum/Culture` / `🚶 Free Time` / `🚌 Transit` |
| City | Select | City where the activity takes place |
| Location / Venue | Text | Specific venue name or address |
| Google Maps Link | URL | Link to location on Google Maps |
| Start Time | Date | Start time of the activity |
| End Time | Date | Estimated end time |
| Duration (hrs) | Formula | `dateBetween(prop("End Time"), prop("Start Time"), "hours")` |
| Estimated Cost | Number (Currency) | Expected cost per person |
| Reservation Required | Checkbox | Whether a reservation must be made in advance |
| Reservation Status | Select | `Not Required` / `To Book` / `Booked` / `Confirmed` |
| Booking Reference | Text | Reservation or ticket confirmation number |
| Priority | Select | `🔴 Must-Do` / `🟡 Want-To-Do` / `🟢 If Time Permits` |
| Status | Select | `📌 Planned` / `✅ Done` / `⏭️ Skipped` |
| Notes | Text | Opening hours, dress code, insider tips, website |
| Photos | Files & Media | Post-trip photos from this activity |

---

### Database 5: 💰 Expenses

**Purpose**: Tracks every expense during the trip to monitor spending against the budget in real time.

| Column Name | Data Type | Description |
|---|---|---|
| Expense Name | Title | Short description (e.g., "Dinner at Ichiran Ramen") |
| Trip | Relation | Links to the **Trip Overview** database |
| Date | Date | Date the expense was incurred |
| Category | Select | `✈️ Transport` / `🏨 Accommodation` / `🍽️ Food & Drink` / `🎟️ Activities` / `🛒 Shopping` / `💊 Health` / `📡 Communication` / `🔧 Miscellaneous` |
| Amount (Local Currency) | Number | Amount paid in local/foreign currency |
| Local Currency | Select | Currency code: `JPY` / `EUR` / `GBP` / `USD` / `THB` / etc. |
| Exchange Rate | Number | Exchange rate used at time of purchase |
| Amount (Home Currency) | Formula | `prop("Amount (Local Currency)") / prop("Exchange Rate")` |
| Payment Method | Select | `💳 Credit Card` / `💵 Cash` / `📱 Mobile Pay` / `🏦 Debit Card` |
| Paid By | Select | Name of the traveler who paid (for group trip splitting) |
| Split With | Multi-select | Names of others splitting this expense |
| Receipt | Files & Media | Photo or PDF of the receipt |
| Notes | Text | Additional context or memo |

---

### Database 6: 🎒 Packing List

**Purpose**: A reusable, categorized checklist of items to pack for any trip. Can be filtered by trip or used as a universal master list.

| Column Name | Data Type | Description |
|---|---|---|
| Item Name | Title | Name of the item (e.g., "Passport", "Power Adapter") |
| Trip | Relation | Links to the **Trip Overview** database (optional, for trip-specific items) |
| Category | Select | `📄 Documents` / `👔 Clothing` / `🧴 Toiletries` / `💊 Health & Medical` / `💻 Electronics` / `🔧 Gear` / `🎒 Carry-On` / `🏖️ Beach` / `🌨️ Winter` / `🍼 Baby/Kids` |
| Packed | Checkbox | Check when item has been packed |
| Quantity | Number | How many of this item to pack |
| Essential | Checkbox | Mark as absolutely critical (passport, medication, etc.) |
| Notes | Text | Brand preference, where to find it, size info |

---

### Database 7: 📋 Task Manager

**Purpose**: Tracks all pre-trip and post-trip to-do items — from booking tasks to things to prepare at home before leaving.

| Column Name | Data Type | Description |
|---|---|---|
| Task | Title | Description of the task (e.g., "Apply for Japan e-Visa") |
| Trip | Relation | Links to the **Trip Overview** database |
| Category | Select | `📝 Booking` / `🛂 Documents` / `💰 Finance` / `🏠 Home Prep` / `🎒 Packing` / `🌐 Research` / `🔔 Notifications` / `📸 Post-Trip` |
| Assigned To | Select | Person responsible (for group trips) |
| Due Date | Date | Deadline for completing the task |
| Status | Select | `🔖 To Do` / `🔄 In Progress` / `✅ Done` / `⏭️ Skipped` |
| Priority | Select | `🔴 High` / `🟡 Medium` / `🟢 Low` |
| Notes | Text | Additional details, links, or instructions |

---

### Database 8: 📍 Saved Places

**Purpose**: A personal travel wishlist and research database for restaurants, attractions, and hidden gems discovered during research — before they get added to the itinerary.

| Column Name | Data Type | Description |
|---|---|---|
| Place Name | Title | Name of the restaurant, attraction, or venue |
| Trip | Relation | Links to the **Trip Overview** database |
| Category | Select | `🍽️ Restaurant` / `☕ Café` / `🍸 Bar` / `🏛️ Museum` / `🌿 Nature` / `🏖️ Beach` / `🛒 Market` / `🎭 Venue` / `🏨 Hotel Option` / `🎯 Activity` |
| City | Select | City where this place is located |
| Address | Text | Street address |
| Google Maps Link | URL | Link to location |
| Website | URL | Official website or booking page |
| Source | Text | Where you found this recommendation (e.g., "Eater NY", "Reddit r/travel") |
| Rating (External) | Select | Michelin / Google rating category: `⭐ Acclaimed` / `👍 Highly Rated` / `📌 To Investigate` |
| Price Range | Select | `💲 Budget` / `💲💲 Moderate` / `💲💲💲 Upscale` / `💲💲💲💲 Luxury` |
| Status | Select | `💡 Idea` / `✅ Added to Itinerary` / `❌ Decided Against` |
| Opening Hours | Text | Days and times open |
| Reservation Required | Checkbox | Whether booking in advance is necessary |
| Notes | Text | Personal notes, must-try dishes, tips |

---

## 3. Page Structure

```
📁 ✈️ Travel Planner (Top-Level Workspace Page)
│
├── 🏠 Dashboard (Home)
│   ├── 👋 Welcome Banner + Quick-Start Guide
│   ├── 📊 Stats Summary (Rollup: trips taken, total spent, countries visited)
│   ├── 🗓️ Upcoming Trips (Filtered Gallery View — Trip Overview DB)
│   ├── 📌 Active Trip Spotlight (Filter: Status = "In Progress")
│   ├── ✅ Today's Tasks (Filtered Table View — Task Manager DB, Due Date = Today)
│   └── 📦 Quick Links (Nav buttons to all sub-pages)
│
├── 🌍