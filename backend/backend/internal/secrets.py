import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_CX = os.getenv("GOOGLE_CX")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MONGODB_URI = os.getenv("MONGODB_URI")

SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")