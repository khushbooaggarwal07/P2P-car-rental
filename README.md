# PeerDrive — Peer-to-Peer Car Rental with Firebase + LLM

A full-stack peer-to-peer car rental app built with **Python Flask**, **Firebase Firestore** (real-time cloud database), and **Claude LLM** (AI assistant).

---

## Emerging Technologies Used

| Technology | Role |
|---|---|
| **LLM (Claude API)** | AI DriveBot assistant — recommends cars based on user needs |
| **Firebase Firestore** | Real-time cloud database — stores all listings & bookings permanently |

---

## Project Structure

```
carshare/
├── app.py                  ← Flask backend + Firebase + LLM
├── serviceAccountKey.json  ← YOUR Firebase key (you create this)
├── requirements.txt
├── README.md
└── index.html
    

---

## Setup in 5 Steps

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Create a Firebase project
1. Go to **https://console.firebase.google.com**
2. Click **"Add Project"** → give it a name (e.g. `peerdrive`)
3. Disable Google Analytics (not needed) → Create Project

### Step 3 — Set up Firestore
1. In your Firebase project, go to **Build → Firestore Database**
2. Click **"Create database"**
3. Choose **"Start in test mode"** (allows all reads/writes for 30 days)
4. Select a region (e.g. `asia-south1` for India) → Done

### Step 4 — Get your Service Account Key
1. In Firebase Console → **Project Settings** (gear icon)
2. Go to **"Service accounts"** tab
3. Click **"Generate new private key"** → Download the JSON file
4. **Rename it to `serviceAccountKey.json`**
5. **Place it in the `carshare/` folder** (same folder as `app.py`)

### Step 5 — Set your Anthropic API key & run
```bash
# Mac/Linux
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

# Windows
set ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

# Run the app
python app.py
```

Open **http://localhost:5000** in your browser ✅

---

## How Firebase Works in This App

```
User submits "List My Car" form
        ↓
Flask receives POST /api/list-car
        ↓
firebase_admin writes to Firestore "cars" collection
        ↓
Data saved permanently in the cloud 
        ↓
Next visitor opens the app → Flask reads from Firestore
        ↓
All listings show up instantly (even after server restart)
```

### Firestore Collections

| Collection | What it stores |
|---|---|
| `cars` | All car listings (owner, model, price, availability, etc.) |
| `bookings` | All confirmed bookings (renter, dates, total cost) |

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/api/cars` | Get all cars (supports ?fuel= ?transmission= ?available= filters) |
| GET | `/api/cars/<id>` | Get single car |
| POST | `/api/book` | Book a car (updates Firestore) |
| POST | `/api/list-car` | List a new car (saves to Firestore) |
| GET | `/api/stats` | Live platform stats from Firestore |
| POST | `/api/chat` | LLM DriveBot (reads live Firestore data) |

---

## Security Note

- Never commit `serviceAccountKey.json` to GitHub — add it to `.gitignore`
- For production, move to Firebase Security Rules to restrict access

---