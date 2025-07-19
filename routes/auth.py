from flask import Blueprint, request, jsonify
from utils.db import supabase
from utils.auth import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    print("Received payload:", data)

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"role": role}}
        })
        return jsonify({"message": "User registered", "user_id": res.user.id}), 201
    except Exception as e:
        print("Supabase error:", str(e))
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("Login payload:", data)
    try:
        res = supabase.auth.sign_in_with_password({
            "email": data.get('email'),
            "password": data.get('password')
        })
        token = generate_token(res.user.id)
        return jsonify({"token": token, "user": {"id": res.user.id, "email": res.user.email}})
    except Exception as e:
        print("Login error:", str(e))
        return jsonify({"error": str(e)}), 401