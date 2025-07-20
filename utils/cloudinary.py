import os
import cloudinary
from cloudinary.uploader import upload
from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_to_cloudinary(file, folder="agrowin"):
    try:
        result = upload(file, folder=folder, resource_type="auto")
        return {"url": result["secure_url"], "public_id": result["public_id"]}
    except Exception as e:
        raise e