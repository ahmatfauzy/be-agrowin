from flask import Blueprint, request, jsonify
from utils.middleware import login_required
import requests
import os

planting_bp = Blueprint('planting', __name__)
OPENWEATHER_API = os.getenv("OPENWEATHER_API")

@planting_bp.route('/recommend', methods=['GET'])
@login_required
def recommend():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API}&units=metric"
    res = requests.get(url).json()

    # Rule-based logic
    recommendations = []
    for item in res['list']:
        if item['main']['temp'] > 20 and item['weather'][0]['main'] != 'Rain':
            recommendations.append(item)

    return jsonify({"recommendations": recommendations})