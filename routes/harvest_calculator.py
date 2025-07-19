from flask import Blueprint, request, jsonify

harvest_bp = Blueprint('harvest', __name__)

# Data spesifik tiap tanaman
CROP_DATA = {
    # Sayuran
    "tomat":     {"yield_per_m2": 0.8, "price_per_kg": 5000, "days": 75},
    "cabai":     {"yield_per_m2": 0.6, "price_per_kg": 12000, "days": 90},
    "selada":    {"yield_per_m2": 1.2, "price_per_kg": 3000, "days": 45},
    "wortel":    {"yield_per_m2": 1.0, "price_per_kg": 4000, "days": 60},
    "bayam":     {"yield_per_m2": 1.5, "price_per_kg": 2500, "days": 30},
    "bawang-merah": {"yield_per_m2": 1.1, "price_per_kg": 14000, "days": 100},
    "bawang-putih": {"yield_per_m2": 0.9, "price_per_kg": 30000, "days": 120},
    "kentang":   {"yield_per_m2": 2.5, "price_per_kg": 6000, "days": 90},
    "terong":    {"yield_per_m2": 0.7, "price_per_kg": 4500, "days": 70},
    "mentimun":  {"yield_per_m2": 1.3, "price_per_kg": 3500, "days": 45},
    "kangkung":  {"yield_per_m2": 2.0, "price_per_kg": 2000, "days": 25},
    "sawi":      {"yield_per_m2": 1.8, "price_per_kg": 2200, "days": 30},

    # Buah
    "semangka":  {"yield_per_m2": 4.0, "price_per_kg": 4000, "days": 80},
    "melon":     {"yield_per_m2": 3.5, "price_per_kg": 5000, "days": 75},
    "jeruk":     {"yield_per_m2": 1.5, "price_per_kg": 8000, "days": 365},  # tahunan
    "mangga":    {"yield_per_m2": 2.0, "price_per_kg": 12000, "days": 365},

    # Padi & palawija
    "padi":      {"yield_per_m2": 0.5, "price_per_kg": 7000, "days": 120},
    "jagung":    {"yield_per_m2": 0.7, "price_per_kg": 4000, "days": 90},
    "kedelai":   {"yield_per_m2": 0.4, "price_per_kg": 10000, "days": 85},
}

@harvest_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    crop = data.get("crop_type", "").lower()
    area = float(data.get("area", 0))

    if crop not in CROP_DATA:
        return jsonify({"error": "crop_type tidak dikenal"}), 400

    info = CROP_DATA[crop]
    estimated_yield = area * info["yield_per_m2"]
    estimated_income = estimated_yield * info["price_per_kg"]
    harvest_time = f"{info['days']} days"

    return jsonify({
        "crop_type": crop,
        "area": area,
        "estimated_yield": round(estimated_yield, 2),
        "estimated_income": int(estimated_income),
        "harvest_time": harvest_time
    })