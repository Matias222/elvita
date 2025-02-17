from dotenv import load_dotenv
from twilio.rest import Client
from httpx import AsyncClient, Response, Timeout
from elevenlabs.client import AsyncElevenLabs

import os, asyncio, uuid

load_dotenv()

LEMONFOX=os.environ.get("LEMONFOX")
ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

eleven_client = AsyncElevenLabs(
  api_key=ELEVENLABS_API_KEY
)

async def generar_voz(texto:str):

  voz="eBthAb30UYbt2nojGXeA"

  results = eleven_client.text_to_speech.convert(
    voice_id=voz,
    output_format="ulaw_8000",
    text=texto,
    model_id="eleven_multilingual_v2")

  out = b''

  async for value in results: out += value

  return out

async def transcript(path:str):

  url = "https://api.lemonfox.ai/v1/audio/transcriptions"
  headers = {
    "Authorization": f"Bearer {LEMONFOX}"
  }

  data = {
  "language": "spanish",
  "response_format": "json",
  "prompt": "La transcripción es de una persona mayor peruana, presta atención a regionalismos y peruanismos."
  }

  async with AsyncClient(timeout=60) as client:
      
      response = await client.post(url, headers=headers, data=data, files={"file": open(path, "rb")})
      print(response.json())
  
  texto=response.json()["text"]

  return texto