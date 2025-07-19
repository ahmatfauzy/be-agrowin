from flask import Blueprint, request, jsonify

harvest_bp = Blueprint('harvest', __name__)

@harvest_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    area = data.get("area")
    crop_type = data.get("crop_type")
    # Dummy logic
    estimated_yield = area * 0.8  # tons
    estimated_income = estimated_yield * 5000  # IDR
    return jsonify({
        "estimated_yield": estimated_yield,
        "estimated_income": estimated_income,
        "harvest_time": "75 days"
    })