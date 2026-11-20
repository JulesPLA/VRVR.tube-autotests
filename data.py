import os

from dotenv import load_dotenv


load_dotenv()

login_body = {
    "username": os.getenv("VRVR_USERNAME", ""),
    "password": os.getenv("VRVR_PASSWORD", ""),
}

channel_body = {
    "title": "Autotest channel"
}
