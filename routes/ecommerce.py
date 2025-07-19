from flask import Blueprint, request, jsonify
from utils.db import supabase
from utils.middleware import login_required

ecommerce_bp = Blueprint('ecommerce', __name__)

@ecommerce_bp.route('/products', methods=['GET'])
def list_products():
    res = supabase.table("products").select("*").execute()
    return jsonify(res.data)

@ecommerce_bp.route('/sell', methods=['POST'])
@login_required
def add_product():
    data = request.json
    supabase.table("products").insert({
        "user_id": request.user["user_id"],
        "name": data["name"],
        "price": data["price"],
        "description": data["description"],
        "image_url": data["image_url"]
    }).execute()
    return jsonify({"message": "Product added"})