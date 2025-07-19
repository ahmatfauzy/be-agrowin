from flask import Blueprint, request, jsonify
from utils.middleware import login_required
from utils.db import supabase
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import requests

plant_disease_bp = Blueprint('plant_disease', __name__)

# masih develop

# MODEL_URL = None ## set  nanti
# model = tf.keras.models.load_model(io.BytesIO(requests.get(MODEL_URL).content))

# # sementara
# @plant_disease_bp.route('/detect', methods=['POST'])
# @login_required
# def detect():
#     return jsonify({
#         "disease_class": "mock_early_blight",
#         "confidence": 0.87,
#         "note": "Model belum di-upload"
#     }), 200


# @plant_disease_bp.route('/detect', methods=['POST'])
# @login_required
# def detect():
#     file = request.files['image']
#     img = Image.open(file).resize((224, 224))
#     img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

#     prediction = model.predict(img_array)
#     class_idx = np.argmax(prediction)
#     confidence = float(np.max(prediction))

#     # Save to DB
#     supabase.table("disease_logs").insert({
#         "user_id": request.user["user_id"],
#         "prediction": str(class_idx),
#         "confidence": confidence
#     }).execute()

#     return jsonify({
#         "disease_class": str(class_idx),
#         "confidence": confidence
#     })