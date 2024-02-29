# Code template for Twilio 
# Source: https://medium.com/@thakuravnish2313/sending-sms-messages-with-twilio-and-python-e7a411c64e54
# TODO: Create Twilio account and get replace template with my credentials (stored in some venv tho)


from twilio.rest import Client

# Replace these with your actual Twilio credentials
TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number_here'
RECIPIENT_PHONE_NUMBER = 'recipient_phone_number_here'

def send_text_message(message):
    try:
        # Create a Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Send the SMS message
        client.messages.create(
            to=RECIPIENT_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )

        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send the message: {e}")

# Call the function to send the text message
message_to_send = "Hello, I am avnish"
send_text_message(message_to_send)