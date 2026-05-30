import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def upload_to_temp_host(file_path: str) -> str:
    """Uploads a file to a temporary public host so Twilio can access it."""
    url = "https://tmpfiles.org/api/v1/upload"
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, files={'file': f})
        if response.status_code == 200:
            data = response.json()
            # Convert the standard URL to a direct download URL
            public_url = data['data']['url'].replace('tmpfiles.org/', 'tmpfiles.org/dl/')
            return public_url
    except Exception as e:
        print(f"Error uploading to temp host: {e}")
    return ""

def send_for_review(video_path: str, title: str):
    """Sends the generated video to WhatsApp via Twilio."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_number = os.getenv("YOUR_WHATSAPP_NUMBER")

    # Twilio requires the "whatsapp:" prefix for WhatsApp messages
    if from_number and not from_number.startswith("whatsapp:"):
        from_number = f"whatsapp:{from_number}"
    if to_number and not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"

    if not all([account_sid, auth_token, from_number, to_number]) or "your_twilio" in account_sid:
        print("⚠️ Twilio credentials not configured in .env. Skipping WhatsApp message.")
        return False

    print("Uploading video to a temporary public link for WhatsApp...")
    media_url = upload_to_temp_host(video_path)

    client = Client(account_sid, auth_token)
    message_body = f"🎬 *New YouTube Short Ready!*\n\n*Title*: {title}\n\nPlease review the video attached. If it fails to load, download it here: {media_url}"

    try:
        print("Sending WhatsApp message...")
        kwargs = {"body": message_body, "from_": from_number, "to": to_number}
        
        if media_url:
            kwargs["media_url"] = [media_url]
            
        message = client.messages.create(**kwargs)
        print(f"✅ WhatsApp message sent! (SID: {message.sid})")
        return True
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")
        return False