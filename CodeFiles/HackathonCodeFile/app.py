from flask import Flask, jsonify, request
from typing import Optional
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import random
import string

app = Flask(__name__)
CORS(app)

# ── MongoDB Connection ──────────────────────────────────────────────────────────
MONGO_URI = "mongodb://localhost:27017/"  # Change if using Atlas
client = MongoClient(MONGO_URI)
db = client["smart_waste"]
bins_collection = db["bins"]

# ── Helper ──────────────────────────────────────────────────────────────────────
# Base coordinates — IIT Madras area (Chennai)
BASE_LAT = 12.9916
BASE_LNG = 80.2336

def make_bin_doc(bin_id: str, level: int, location: str,
                 lat: Optional[float] = None, lng: Optional[float] = None) -> dict:
    return {
        "binId": bin_id,
        "level": level,
        "location": location,
        "status": "Full" if level >= 80 else ("Medium" if level >= 50 else "Normal"),
        "lat": lat if lat is not None else float(round(BASE_LAT + random.uniform(-0.02, 0.02), 6)),
        "lng": lng if lng is not None else float(round(BASE_LNG + random.uniform(-0.02, 0.02), 6)),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


# ── Endpoints ───────────────────────────────────────────────────────────────────

@app.route("/data", methods=["POST"])
def receive_data():
    """Accept a bin reading and persist it to MongoDB."""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON body required"}), 400

    bin_id   = payload.get("binId")
    level    = payload.get("level")
    location = payload.get("location", "Unknown")

    # Validation
    if not bin_id:
        return jsonify({"error": "binId is required"}), 400
    if level is None or not isinstance(level, (int, float)):
        return jsonify({"error": "level must be a number"}), 400
    if not (0 <= level <= 100):
        return jsonify({"error": "level must be between 0 and 100"}), 400

    doc = make_bin_doc(str(bin_id), int(level), str(location))
    result = bins_collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    return jsonify({"message": "Data stored successfully", "data": doc}), 201


@app.route("/data", methods=["GET"])
def get_data():
    """Return the latest reading per bin (sorted by level desc)."""
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {
            "$group": {
                "_id": "$binId",
                "binId":    {"$first": "$binId"},
                "level":    {"$first": "$level"},
                "location": {"$first": "$location"},
                "status":   {"$first": "$status"},
                "lat":      {"$first": "$lat"},
                "lng":      {"$first": "$lng"},
                "timestamp":{"$first": "$timestamp"},
            }
        },
        {"$sort": {"level": -1}},
    ]
    docs = list(bins_collection.aggregate(pipeline))
    for d in docs:
        d.pop("_id", None)

    return jsonify({"count": len(docs), "bins": docs}), 200


@app.route("/simulate", methods=["GET"])
def simulate():
    """Generate random readings for demo bins and store them."""
    locations = [
        "Block A - Main Entrance",
        "Block B - Cafeteria",
        "Block C - Parking Lot",
        "Block D - Library",
        "Block E - Sports Complex",
        "Block F - Admin Office",
        "Block G - Hostel",
        "Block H - Labs",
    ]

    inserted = []
    for i, location in enumerate(locations, start=1):
        bin_id = f"BIN-{i:03d}"
        level  = random.randint(0, 100)
        doc    = make_bin_doc(bin_id, level, location)
        bins_collection.insert_one(doc)
        doc.pop("_id", None)
        inserted.append(doc)

    return jsonify({
        "message": f"{len(inserted)} bins simulated",
        "bins": sorted(inserted, key=lambda x: x["level"], reverse=True),
    }), 200


@app.route("/clear", methods=["DELETE"])
def clear_data():
    """Utility: wipe all records (dev/demo use only)."""
    result = bins_collection.delete_many({})
    return jsonify({"message": f"Deleted {result.deleted_count} records"}), 200


# ── Entry Point ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
