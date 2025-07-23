from flask import Blueprint, request, jsonify
from utils.middleware import login_required
from utils.db import supabase
from utils.cloudinary import upload_to_cloudinary  # jika ingin simpan foto
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import requests
import io

plant_disease_bp = Blueprint('plant_disease', __name__)

USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"

LOCAL_MODEL = os.getenv("LOCAL_MODEL", "plant_disease_model.h5")

CLOUD_MODEL_URL = os.getenv("MODEL_URL")  # URL Supabase / CDN

model = None
if not USE_MOCK:
    if os.path.exists(LOCAL_MODEL):
        model = tf.keras.models.load_model(LOCAL_MODEL)
    elif CLOUD_MODEL_URL:
        try:
            print("Downloading model …")
            r = requests.get(CLOUD_MODEL_URL)
            r.raise_for_status()
            model = tf.keras.models.load_model(io.BytesIO(r.content))
            # simpan lokal agar tidak download ulang
            with open(LOCAL_MODEL, "wb") as f:
                f.write(r.content)
            print("Model ready")
        except Exception as e:
            print("Model download failed:", e)
            USE_MOCK = True
    else:
        print("Model URL tidak di-set, fallback ke mock")
        USE_MOCK = True

@plant_disease_bp.route('/detect', methods=['POST'])
@login_required
def detect():
    if USE_MOCK:
        return jsonify({
            "disease_class": "mock_early_blight",
            "confidence": 0.87,
            "note": "Model belum di-upload / mock mode"
        }), 200

    file = request.files.get('image')
    if not file:
        return jsonify({"error": "image required"}), 400

    try:
        img = Image.open(file).convert('RGB').resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        preds = model.predict(img_array)
        class_idx = int(np.argmax(preds))
        confidence = float(np.max(preds))

        # simpan log
        supabase.table("disease_logs").insert({
            "user_id": request.user["user_id"],
            "prediction": str(class_idx),
            "confidence": confidence
        }).execute()

        return jsonify({
            "disease_class": str(class_idx),
            "confidence": confidence
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500