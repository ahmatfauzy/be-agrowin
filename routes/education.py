from flask import Blueprint, jsonify
from utils.db import supabase
from utils.middleware import login_required

education_bp = Blueprint('education', __name__)

@education_bp.route('/articles', methods=['GET'])
@login_required
def get_articles():
    res = supabase.table("articles").select("*").execute()
    return jsonify(res.data)

@education_bp.route('/videos', methods=['GET'])
@login_required
def get_videos():
    res = supabase.table("videos").select("*").execute()
    return jsonify(res.data)