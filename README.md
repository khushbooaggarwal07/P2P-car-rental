# PeerDrive — Peer-to-Peer Car Rental Platform

A full-stack peer-to-peer car rental web app built with Python Flask, Firebase Firestore, and an LLM (Large Language Model) powered AI assistant called DriveBot.

---

## Emerging Technologies Used

| Technology | Role |
|---|---|
| LLM via Groq API | AI DriveBot assistant that recommends cars based on user needs |
| Firebase Firestore | Real-time cloud database that stores all listings and bookings permanently |

---

## Project Structure

```
carshare/
├── app.py                  
├── index.html              
├── serviceAccountKey.json  
├── requirements.txt
├── README.md
└── static/
```

---

## Setup in 4 Steps

### Step 1 - Install dependencies
```
pip install -r requirements.txt
```

### Step 2 - Add Firebase key
Download serviceAccountKey.json from Firebase Console and place it in the project folder.
Firebase Console - Project Settings - Service Accounts - Generate New Private Key

### Step 3 - Get Groq API key
Go to https://console.groq.com, sign up, and create a free API key.

### Step 4 - Run the app
```
set GROQ_API_KEY=your_groq_key_here
python app.py
```

Open http://localhost:5000 in your browser.

---

## Features

For Renters:
- Browse Cars - Filter by fuel type, transmission, availability
- Book Instantly - Pick dates, enter details, confirm in one click
- AI Assistant DriveBot - Chat with an LLM to get car recommendations

For Car Owners:
- List Your Car - Fill a simple form, car goes live immediately
- Set your own price per day
- Car is auto-marked as booked when rented

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | /api/cars | List all cars with optional filters |
| GET | /api/cars/id | Get single car details |
| POST | /api/book | Book a car |
| POST | /api/list-car | List a new car |
| GET | /api/stats | Platform statistics |
| POST | /api/chat | LLM DriveBot chat |

---

## How LLM Integration Works

1. User opens the chat widget on the website
2. Frontend sends the user message to /api/chat
3. Flask fetches live car listings from Firebase
4. A prompt is built with car data and sent to Groq API
5. LLaMA 3.3 model reasons about the user needs and recommends the best car
6. Reply is returned and shown in the chat widget

DriveBot has live awareness of all available cars, their prices, features, and availability from Firebase.

---
