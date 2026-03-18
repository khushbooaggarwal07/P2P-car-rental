# PeerDrive — Peer-to-Peer Car Rental Platform

A full-stack peer-to-peer car rental web app built with **Python Flask** and integrated with a **Large Language Model (LLM)** via the Anthropic Claude API.

---

## Emerging Technology: LLM Integration

This project integrates an **LLM (Large Language Model)** — specifically **Claude claude-sonnet-4-20250514** — to power an intelligent car recommendation assistant called **DriveBot**.

**How it works:**
1. User opens the chat widget on the website
2. The frontend sends the user's message + chat history to `/api/chat`
3. Flask calls the Anthropic Claude API with a system prompt containing live car listings
4. Claude reasons about the user's needs and recommends the best car
5. The response is streamed back to the user in real time

This means DriveBot has **live awareness** of all available cars, their prices, features, and availability — not just generic knowledge.

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
# On Mac/Linux:
export ANTHROPIC_API_KEY=your_api_key_here

# On Windows:
set ANTHROPIC_API_KEY=your_api_key_here
```
Get your key from: https://console.anthropic.com

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## Features

### For Renters
- **Browse Cars** — Filter by fuel type, transmission, availability
- **Book Instantly** — Pick dates, enter details, confirm in one click
- **AI Assistant (DriveBot)** — Chat with an LLM to get personalised car recommendations

### For Car Owners
- **List Your Car** — Fill a simple form, car goes live immediately
- **Set Your Price** — Choose your own daily rate
- **Track Availability** — Car auto-marked as booked when rented

### Platform
- Live stats: total cars, available cars, bookings, owners
- Fully responsive design
- No login required (demo mode)

---

## API Endpoints

| Method | Route            | Description              |
|--------|------------------|--------------------------|
| GET    | `/api/cars`      | List all cars (with filters) |
| GET    | `/api/cars/<id>` | Get single car details   |
| POST   | `/api/book`      | Book a car               |
| POST   | `/api/list-car`  | List a new car           |
| GET    | `/api/stats`     | Platform statistics      |
| POST   | `/api/chat`      | LLM chat (DriveBot)      |

---

## LLM Prompt Design

The `/api/chat` endpoint injects real-time car data into the system prompt:
- All available cars with prices, features, locations
- DriveBot understands Indian travel contexts (Manali trips, Delhi commutes, family outings)
- Maintains conversation history across turns

---

## Notes for Presentation

- The LLM integration is the key **emerging technology** — it makes the search experience intelligent instead of just filter-based
- The system prompt is dynamically built from the live database, so DriveBot always has up-to-date information
- In production, replace the in-memory `cars` list with a real database (SQLite, PostgreSQL)
