from dotenv import load_dotenv
from twilio.rest import Client
from httpx import AsyncClient, Response, Timeout
from elevenlabs.client import AsyncElevenLabs

import os, asyncio, uuid

load_dotenv()

LEMONFOX=os.environ.get("LEMONFOX")
ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

eleven_client = AsyncElevenLabs(
  api_key=ELEVENLABS_API_KEY,
  timeout=600
)

async def generar_voz(texto:str):

  abuela="eBthAb30UYbt2nojGXeA"
  jorge="HAsl3FenyWHYwECSP6Hl"
  cristina="CaJslL1xziwefCeTNzHv"

  results = eleven_client.text_to_speech.convert_as_stream(
    voice_id=cristina,
    output_format="ulaw_8000",
    text=texto,
    model_id="eleven_flash_v2_5")

  out = b''

  arreglo_binarios=[]

  async for value in results: arreglo_binarios.append(value)
  
  return arreglo_binarios

async def transcript(path:str):

  url = "https://api.lemonfox.ai/v1/audio/transcriptions"
  headers = {
    "Authorization": f"Bearer {LEMONFOX}"
  }

  data = {
  "language": "spanish",
  "response_format": "json",
  "prompt": "El audio ha escuchar es recolectado en tiempo real de una llamada telefónica. En caso no detectas nada, devuelve una cadena vacia."
  }

  async with AsyncClient(timeout=60) as client:
      
      response = await client.post(url, headers=headers, data=data, files={"file": open(path, "rb")})
      print(response.json())
  
  texto=response.json()["text"]

  return texto