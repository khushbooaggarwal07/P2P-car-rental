from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from groq import Groq

app = Flask(__name__, template_folder='.')

# groq setup
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# seed cars
def seed_cars():
    cars_ref = db.collection("cars")
    existing = list(cars_ref.limit(1).stream())
    if existing:
        return
    default_cars = [
        {
            "owner": "Rahul Sharma", "owner_phone": "98100-11111",
            "model": "Maruti Swift", "year": 2022, "location": "Connaught Place, Delhi",
            "price_per_day": 1200, "fuel": "Petrol", "seats": 5,
            "transmission": "Manual", "rating": 4.8, "reviews": 24,
            "available": True,
            "features": ["AC", "Bluetooth", "USB Charging", "Power Windows"],
            "description": "Well-maintained Swift, perfect for city drives.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Priya Kapoor", "owner_phone": "98100-22222",
            "model": "Hyundai Creta", "year": 2023, "location": "Hauz Khas, Delhi",
            "price_per_day": 2200, "fuel": "Diesel", "seats": 5,
            "transmission": "Automatic", "rating": 4.9, "reviews": 17,
            "available": True,
            "features": ["AC", "Sunroof", "360 Camera", "Android Auto"],
            "description": "Premium SUV, great for highway trips.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Amit Verma", "owner_phone": "98100-33333",
            "model": "Tata Nexon EV", "year": 2023, "location": "Dwarka, Delhi",
            "price_per_day": 1800, "fuel": "Electric", "seats": 5,
            "transmission": "Automatic", "rating": 4.7, "reviews": 31,
            "available": True,
            "features": ["AC", "Fast Charging", "Apple CarPlay"],
            "description": "Eco-friendly EV with 312km range.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Sneha Gupta", "owner_phone": "98100-44444",
            "model": "Honda City", "year": 2021, "location": "Lajpat Nagar, Delhi",
            "price_per_day": 1500, "fuel": "Petrol", "seats": 5,
            "transmission": "Manual", "rating": 4.6, "reviews": 42,
            "available": False,
            "features": ["AC", "Sunroof", "Touchscreen"],
            "description": "Reliable sedan, great mileage.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Vikram Singh", "owner_phone": "98100-55555",
            "model": "Mahindra Thar", "year": 2022, "location": "Rohini, Delhi",
            "price_per_day": 3500, "fuel": "Diesel", "seats": 4,
            "transmission": "Manual", "rating": 4.9, "reviews": 12,
            "available": True,
            "features": ["4WD", "Convertible Top", "Off-road Tyres"],
            "description": "Adventure vehicle, perfect for Manali trips.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Neha Joshi", "owner_phone": "98100-66666",
            "model": "Toyota Innova Crysta", "year": 2022, "location": "Saket, Delhi",
            "price_per_day": 2800, "fuel": "Diesel", "seats": 7,
            "transmission": "Automatic", "rating": 4.8, "reviews": 28,
            "available": True,
            "features": ["AC", "Captain Seats", "Rear AC", "Touchscreen"],
            "description": "Spacious 7-seater for family trips.",
            "created_at": datetime.now().isoformat()
        },
    ]
    for car in default_cars:
        cars_ref.add(car)
    print("Seeded default cars to Firebase")

seed_cars()

# helper
def doc_to_car(doc):
    d = doc.to_dict()
    d["id"] = doc.id
    return d

# routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cars")
def get_cars():
    fuel  = request.args.get("fuel", "all")
    tx    = request.args.get("transmission", "all")
    avail = request.args.get("available", "false") == "true"
    query = db.collection("cars")
    if fuel != "all":
        query = query.where("fuel", "==", fuel)
    if tx != "all":
        query = query.where("transmission", "==", tx)
    if avail:
        query = query.where("available", "==", True)
    cars = [doc_to_car(d) for d in query.stream()]
    return jsonify(cars)

@app.route("/api/cars/<car_id>")
def get_car(car_id):
    doc = db.collection("cars").document(car_id).get()
    if not doc.exists:
        return jsonify({"error": "Not found"}), 404
    return jsonify(doc_to_car(doc))

@app.route("/api/book", methods=["POST"])
def book_car():
    d = request.json
    car_ref = db.collection("cars").document(d["car_id"])
    car_doc = car_ref.get()
    if not car_doc.exists:
        return jsonify({"error": "Car not found"}), 404
    car = car_doc.to_dict()
    if not car["available"]:
        return jsonify({"error": "Car is not available"}), 400
    booking_data = {
        "car_id": d["car_id"], "car_model": car["model"],
        "renter_name": d["renter_name"], "renter_phone": d["renter_phone"],
        "pickup_date": d["pickup_date"], "return_date": d["return_date"],
        "days": d["days"], "total": car["price_per_day"] * d["days"],
        "booked_at": datetime.now().isoformat()
    }
    _, booking_ref = db.collection("bookings").add(booking_data)
    booking_data["id"] = booking_ref.id
    car_ref.update({"available": False})
    return jsonify({"success": True, "booking": booking_data})

@app.route("/api/list-car", methods=["POST"])
def list_car():
    d = request.json
    new_car = {
        "owner": d["owner_name"], "owner_phone": d["owner_phone"],
        "model": d["model"], "year": int(d["year"]),
        "location": d["location"], "price_per_day": int(d["price_per_day"]),
        "fuel": d["fuel"], "seats": int(d["seats"]),
        "transmission": d["transmission"],
        "rating": 5.0, "reviews": 0, "available": True,
        "features": [f.strip() for f in d.get("features", "").split(",") if f.strip()],
        "description": d.get("description", ""),
        "created_at": datetime.now().isoformat()
    }
    _, doc_ref = db.collection("cars").add(new_car)
    new_car["id"] = doc_ref.id
    return jsonify({"success": True, "car": new_car})

@app.route("/api/stats")
def stats():
    all_cars     = list(db.collection("cars").stream())
    available    = list(db.collection("cars").where("available", "==", True).stream())
    all_bookings = list(db.collection("bookings").stream())
    owners       = set(d.to_dict().get("owner") for d in all_cars)
    return jsonify({
        "total": len(all_cars), "available": len(available),
        "bookings": len(all_bookings), "owners": len(owners),
    })

# chat using groq
@app.route("/api/chat", methods=["POST"])
def chat():
    d = request.json
    msg     = d.get("message", "")
    history = d.get("history", [])

    cars = [doc_to_car(doc) for doc in db.collection("cars").stream()]
    car_lines = []
    for c in cars:
        status = "available" if c["available"] else "booked"
        car_lines.append(
            f"- {c['model']} {c['year']}: Rs{c['price_per_day']}/day, "
            f"{c['fuel']}, {c['seats']} seats, {c['transmission']}, "
            f"{c['location']} [{status}]"
        )
    cars_text = "\n".join(car_lines)

    system_prompt = f"""You are DriveBot, a friendly AI assistant for PeerDrive, a peer-to-peer car rental platform in Delhi, India.
Help users find the right car. Use Rs for prices. Be friendly and concise. Plain text only, no asterisks or markdown.
Understand Indian travel context like Manali trips, office commute, family outings.

Current car listings:
{cars_text}"""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-4:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": msg})

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=300
        )
        reply = response.choices[0].message.content
        print(f"Groq reply: {reply[:80]}")
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Groq error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
