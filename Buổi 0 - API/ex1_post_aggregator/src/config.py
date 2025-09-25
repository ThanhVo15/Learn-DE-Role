import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # loads from .env if exists

BASE_DIR = Path.cwd()
OUTPUT_DIR = BASE_DIR / "output_ex1"
OUTPUT_DIR.mkdir(exist_ok=True)

POSTS_API = "https://jsonplaceholder.typicode.com/posts"
CACHE_TTL_SECONDS = 60
RETRY_LIMIT = 3
RETRY_BASE_DELAY = 0.5

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)
EMAIL_TO = [e.strip() for e in os.getenv("EMAIL_TO", "").split(",") if e.strip()]