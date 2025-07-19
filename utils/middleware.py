from functools import wraps
from flask import request, jsonify
from utils.auth import verify_token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split(" ")[1]
        decoded = verify_token(token)
        if not decoded:
            return jsonify({"error": "Invalid token"}), 401
        request.user = decoded
        return f(*args, **kwargs)
    return decorated