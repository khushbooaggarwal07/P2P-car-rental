from flask import Flask, render_template, request, jsonify
import json, anthropic
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='.')
client = anthropic.Anthropic()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
            "description": "Well-maintained Swift, perfect for city drives. Always kept spotless.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Priya Kapoor", "owner_phone": "98100-22222",
            "model": "Hyundai Creta", "year": 2023, "location": "Hauz Khas, Delhi",
            "price_per_day": 2200, "fuel": "Diesel", "seats": 5,
            "transmission": "Automatic", "rating": 4.9, "reviews": 17,
            "available": True,
            "features": ["AC", "Sunroof", "360 Camera", "Android Auto", "Cruise Control"],
            "description": "Premium SUV with all comforts. Great for highway trips and family outings.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Amit Verma", "owner_phone": "98100-33333",
            "model": "Tata Nexon EV", "year": 2023, "location": "Dwarka, Delhi",
            "price_per_day": 1800, "fuel": "Electric", "seats": 5,
            "transmission": "Automatic", "rating": 4.7, "reviews": 31,
            "available": True,
            "features": ["AC", "Fast Charging", "Apple CarPlay", "ADAS", "Ventilated Seats"],
            "description": "Eco-friendly EV with 312km range. Save on fuel, enjoy a modern drive.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Sneha Gupta", "owner_phone": "98100-44444",
            "model": "Honda City", "year": 2021, "location": "Lajpat Nagar, Delhi",
            "price_per_day": 1500, "fuel": "Petrol", "seats": 5,
            "transmission": "Manual", "rating": 4.6, "reviews": 42,
            "available": False,
            "features": ["AC", "Sunroof", "Touchscreen", "Rear Camera"],
            "description": "Reliable sedan with great mileage. Ideal for city and long drives.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Vikram Singh", "owner_phone": "98100-55555",
            "model": "Mahindra Thar", "year": 2022, "location": "Rohini, Delhi",
            "price_per_day": 3500, "fuel": "Diesel", "seats": 4,
            "transmission": "Manual", "rating": 4.9, "reviews": 12,
            "available": True,
            "features": ["4WD", "Convertible Top", "Off-road Tyres", "Adventure Ready"],
            "description": "The ultimate adventure vehicle. Perfect for Manali trips and off-road fun.",
            "created_at": datetime.now().isoformat()
        },
        {
            "owner": "Neha Joshi", "owner_phone": "98100-66666",
            "model": "Toyota Innova Crysta", "year": 2022, "location": "Saket, Delhi",
            "price_per_day": 2800, "fuel": "Diesel", "seats": 7,
            "transmission": "Automatic", "rating": 4.8, "reviews": 28,
            "available": True,
            "features": ["AC", "Captain Seats", "Rear AC", "Touchscreen", "USB All Rows"],
            "description": "Spacious 7-seater, perfect for family trips or group outings.",
            "created_at": datetime.now().isoformat()
        },
    ]
    for car in default_cars:
        cars_ref.add(car)
    print("Seeded default cars to Firebase")

seed_cars()

def doc_to_car(doc):
    d = doc.to_dict()
    d["id"] = doc.id
    return d

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

@app.route("/api/chat", methods=["POST"])
def chat():
    d = request.json
    msg     = d.get("message", "")
    history = d.get("history", [])
    cars = [doc_to_car(doc) for doc in db.collection("cars").stream()]
    cars_data = json.dumps([{
        "id": c["id"], "model": c["model"], "year": c["year"],
        "location": c["location"], "price_per_day": c["price_per_day"],
        "fuel": c["fuel"], "seats": c["seats"], "transmission": c["transmission"],
        "available": c["available"], "features": c["features"],
        "description": c["description"], "rating": c["rating"]
    } for c in cars], indent=2)
    system = f"""You are DriveBot, a friendly AI assistant for PeerDrive — a peer-to-peer car rental platform in Delhi, India.
Help users find the right car based on budget, trip type, group size, fuel preference.
Live listings from Firebase:
{cars_data}
Rules: Be friendly and concise. Always use Rs for prices. Suggest alternatives if a car is unavailable. Understand Indian travel context."""
    messages = history + [{"role": "user", "content": msg}]
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600, system=system, messages=messages
    )
    return jsonify({"reply": resp.content[0].text})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
