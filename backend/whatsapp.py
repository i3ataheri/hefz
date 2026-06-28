"""
WhatsApp integration using Meta WhatsApp Cloud API.
100% free up to 1,000 conversations/month.
"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")
META_PHONE_NUMBER_ID = os.environ.get("META_PHONE_NUMBER_ID")
WHATSAPP_GROUP_ID = os.environ.get("WHATSAPP_GROUP_ID")

API_URL = f"https://graph.facebook.com/v22.0/{META_PHONE_NUMBER_ID}/messages"


def send_whatsapp(message_body: str) -> bool:
    if not all([META_ACCESS_TOKEN, META_PHONE_NUMBER_ID, WHATSAPP_GROUP_ID]):
        print("ERROR: Missing Meta Cloud API configuration. Check .env file.")
        return False

    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_GROUP_ID,
        "type": "text",
        "text": {"body": message_body},
    }

    try:
        with httpx.Client() as client:
            resp = client.post(API_URL, json=payload, headers=headers)
            if resp.status_code == 200:
                print(f"WhatsApp sent successfully. ID: {resp.json().get('messages', [{}])[0].get('id')}")
                return True
            else:
                print(f"ERROR {resp.status_code}: {resp.text}")
                return False
    except Exception as e:
        print(f"ERROR sending WhatsApp: {e}")
        return False
