from flask import Blueprint, request, jsonify
from utils.db import supabase
from utils.middleware import login_required
from utils.cloudinary import upload_to_cloudinary

education_bp = Blueprint('education', __name__)

@education_bp.route('/articles', methods=['GET'])
@login_required
def get_articles():
    res = supabase.table("articles").select("*").order("created_at", desc=True).execute()
    return jsonify(res.data), 200

@education_bp.route('/videos', methods=['GET'])
@login_required
def get_videos():
    res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    return jsonify(res.data), 200

@education_bp.route('/articles/upload', methods=['POST'])
@login_required
def upload_article():
    title   = request.form.get("title")
    content = request.form.get("content")
    image   = request.files.get("image")

    if not title or not content:
        return jsonify({"error": "title & content required"}), 400

    # upload thumbnail ke Cloudinary (jika ada)
    image_url = None
    if image:
        try:
            result = upload_to_cloudinary(image, folder="education/articles")
            image_url = result["url"]
        except Exception as e:
            return jsonify({"error": f"upload failed: {e}"}), 500

    # simpan ke Supabase
    row = {
        "title": title,
        "content": content,
        "image_url": image_url
    }
    supabase.table("articles").insert(row).execute()
    return jsonify({"message": "Article created", "image_url": image_url}), 201


@education_bp.route('/videos/upload', methods=['POST'])
@login_required
def upload_video():
    title       = request.form.get("title")
    description = request.form.get("description")
    video       = request.files.get("video")

    if not title or not video:
        return jsonify({"error": "title & video required"}), 400

    try:
        result = upload_to_cloudinary(video, folder="education/videos", resource_type="video")
    except Exception as e:
        return jsonify({"error": f"upload failed: {e}"}), 500

    row = {
        "title": title,
        "description": description,
        "video_url": result["url"]
    }
    supabase.table("videos").insert(row).execute()
    return jsonify({"message": "Video created", "video_url": result["url"]}), 201