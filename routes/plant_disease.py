from flask import Blueprint, request, jsonify
from utils.middleware import login_required
from utils.db import supabase
from utils.cloudinary import upload_to_cloudinary  # jika ingin simpan foto
from PIL import Image
import numpy as np
import os
import io
import requests
import tensorflow as tf

plant_disease_bp = Blueprint('plant_disease', __name__)

USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "model.h5")
CLOUD_MODEL_URL = os.getenv("MODEL_URL", "")

MODEL_PATH = os.path.join(os.getcwd(), LOCAL_MODEL)

CLASS_NAMES = ["early_blight", "late_blight", "healthy"]

# Load model
model = None
if not USE_MOCK:
    try:
        if os.path.exists(MODEL_PATH):
            print(f"Loading model from local: {MODEL_PATH}")
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded from local.")
        elif CLOUD_MODEL_URL:
            print(f"Downloading model from {CLOUD_MODEL_URL}")
            r = requests.get(CLOUD_MODEL_URL)
            r.raise_for_status()
            model = tf.keras.models.load_model(io.BytesIO(r.content))
            with open(MODEL_PATH, "wb") as f:
                f.write(r.content)
            print("Model downloaded and saved.")
        else:
            print("Tidak ada model lokal atau URL, fallback ke mock.")
            USE_MOCK = True
    except Exception as e:
        print("Gagal load model:", str(e))
        USE_MOCK = True

@plant_disease_bp.route('/detect', methods=['POST'])
@login_required
def detect():
    if USE_MOCK or model is None:
        return jsonify({
            "disease_class": "mock_early_blight",
            "confidence": 0.87,
            "note": "Model belum tersedia (mock mode aktif)"
        }), 200

    file = request.files.get('image')
    if not file:
        return jsonify({"error": "Gambar (image) wajib diunggah"}), 400

    try:
        img = Image.open(file).convert('RGB').resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

        # Prediksi
        preds = model.predict(img_array)
        class_idx = int(np.argmax(preds))
        confidence = float(np.max(preds))
        class_label = CLASS_NAMES[class_idx]

        try:
            supabase.table("disease_logs").insert({
                "user_id": request.user["user_id"],
                "prediction": class_label,
                "confidence": confidence
            }).execute()
        except Exception as log_error:
            print("Gagal menyimpan log ke Supabase:", log_error)

        return jsonify({
            "disease_class": class_label,
            "confidence": confidence
        }), 200

    except Exception as e:
        print("Error saat proses deteksi:", e)
        return jsonify({"error": str(e)}), 500
