# Import twilio Client API and required modules
from twilio.rest import Client
from src.config import RECIPIENT_PHONE_NUMBER, TWILIO_PHONE_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


# Send SMS to configured recipient
def send_text_message(message):
    try:
        client = Client(
            TWILIO_ACCOUNT_SID, 
            TWILIO_AUTH_TOKEN
        )
        client.messages.create(
            to = RECIPIENT_PHONE_NUMBER,
            from_ = TWILIO_PHONE_NUMBER,
            body = message
        )
        print("Sent Successfully!")
    except Exception as e:
        print(f"Failed to Send Message: {e}")