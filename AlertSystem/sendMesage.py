import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API token and sender info from .env
API_TOKEN = os.getenv("AFROMESSAGE_API_TOKEN")
SENDER_ID = "AAU-CVMA"  # Optional short code
SENDER_NAME = os.getenv("AFROMESSAGE_SENDER_NAME", "Cowsville")  # Optional sender name

# Development mode - don't require API token
if not API_TOKEN:
    logging.warning("⚠️ Development mode: AFROMESSAGE_API_TOKEN not set. SMS sending is disabled.")
    API_TOKEN = "development_token"

# API Details
BASE_URL = "https://api.afromessage.com/api/send"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Create a session object
session = requests.Session()


def send_alert(phone_number, message):
    """
    Sends an SMS alert to the specified phone number.

    :param phone_number: The recipient's phone number (e.g., +251912345678).
    :param message: The message content to send.
    :return: API response or error message.
    """
    # In development mode, just log the message instead of sending it
    if API_TOKEN == "development_token":
        logging.info(f"📱 [DEV MODE] Would send SMS to {phone_number}: {message}")
        return {"status": "success", "response": {"acknowledge": "success", "message": "Development mode - no actual SMS sent"}}

    try:
        # Construct the request URL with proper sender info
        params = { # Sender name (e.g., "Cowsville")
            "sender": SENDER_ID,  # Short code/sender ID if you have one
            "to": phone_number,
            "message": message,
            "callback": "",  # Optional callback URL
        }

        response = session.get(BASE_URL, headers=HEADERS, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("acknowledge") == "success":
                logging.info(f"✅ SMS sent successfully to {phone_number}")
                return {"status": "success", "response": json_response}
            else:
                logging.error(f"❌ API error: {json_response}")
                return {"status": "error", "response": json_response}
        else:
            logging.error(
                f"❌ HTTP error: Code {response.status_code}, Message: {response.text}"
            )
            return {
                "status": "http_error",
                "code": response.status_code,
                "message": response.text,
            }

    except requests.RequestException as e:
        logging.error(f"❌ Network error: {str(e)}")
        return {"status": "network_error", "message": str(e)}
