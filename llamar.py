
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID=os.environ.get("TWILIO_SID")
TWILIO_AUTH=os.environ.get("TWILIO_AUTH")

client = Client(TWILIO_SID, TWILIO_AUTH)

abuela="+51988482104"

call = client.calls.create(
    from_="+12177182629",
    to="+51953479740",
    url="https://0923-45-236-45-53.ngrok-free.app/incoming-call",
)

print(call.sid)