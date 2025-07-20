from flask import Blueprint, request, jsonify
from utils.db import supabase
from utils.middleware import login_required
from utils.cloudinary import upload_to_cloudinary

ecommerce_bp = Blueprint('ecommerce', __name__)

@ecommerce_bp.route('/products', methods=['GET'])
def list_products():
    res = supabase.table("products").select("*").execute()
    return jsonify(res.data)

@ecommerce_bp.route('/sell', methods=['POST'])
@login_required
def add_product():
    # 1. upload gambar ke Cloudinary
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "image required"}), 400
    upload_res = upload_to_cloudinary(file, folder="products")

    # 2. simpan URL ke Supabase
    data = request.form.to_dict()
    supabase.table("products").insert({
        "user_id": request.user["user_id"],
        "name": data["name"],
        "price": int(data["price"]),
        "description": data["description"],
        "image_url": upload_res["url"]
    }).execute()

    return jsonify({"message": "Product added", "image_url": upload_res["url"]}), 201