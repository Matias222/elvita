from datetime import datetime, timedelta
import os

from anthropic import AsyncAnthropic
from app import api_models

from dotenv import load_dotenv
import litellm

load_dotenv()

litellm.success_callback=["helicone"]

HELICONE_LLAVE=os.environ.get("HELICONE_API_KEY")

client = AsyncAnthropic(
  base_url="https://anthropic.helicone.ai",
  default_headers={
    "Helicone-Auth": f"Bearer {HELICONE_LLAVE}",
  },
)

async def call_open(messages,formato_respuesta,modelo="openai/gpt-4o-mini",temperatura=0):


    response = await litellm.acompletion(
        model=modelo,
        messages=messages,
        temperature=temperatura,
        response_format=formato_respuesta
    )

    return response