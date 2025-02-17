
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID=os.environ.get("TWILIO_SID")
TWILIO_AUTH=os.environ.get("TWILIO_AUTH")

client = Client(TWILIO_SID, TWILIO_AUTH)

call = client.calls.create(
    from_="+12177182629",
    to="+51950080044",
    url="https://c913-179-6-6-188.ngrok-free.app/incoming-call",
)

print(call.sid)