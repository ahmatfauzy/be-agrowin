from dotenv import load_dotenv
load_dotenv()


from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from routes.plant_disease import plant_disease_bp
from routes.planting_recommendation import planting_bp
from routes.ecommerce import ecommerce_bp
from routes.education import education_bp
from routes.harvest_calculator import harvest_bp
from utils.middleware import login_required


app = Flask(__name__)
CORS(app)

# Public routes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(harvest_bp, url_prefix='/api/harvest')

# Protected routes
app.register_blueprint(plant_disease_bp, url_prefix='/api/plant')
app.register_blueprint(planting_bp, url_prefix='/api/planting')
app.register_blueprint(ecommerce_bp, url_prefix='/api/ecommerce')
app.register_blueprint(education_bp, url_prefix='/api/education')

@app.route('/')
def home():
    return jsonify({"message": "AGROWIN Backend Running"})

if __name__ == '__main__':
    app.run(debug=True)