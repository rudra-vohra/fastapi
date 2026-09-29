from dotenv import load_dotenv
load_dotenv()

import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

ALLOWED_EXTENSIONS = {".pdf", ".txt"}
ALLOWED_SIZE = 50  # 50 MB

UPLOAD_DIR = "uploads"