
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
    to="+51927144823",
    url="https://e3ca-2800-200-ea80-14e-7c14-a6c9-5d3c-88ce.ngrok-free.app/incoming-call",
)

print(call.sid)