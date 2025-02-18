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

async def call_claude(sistema,messages,tools,modelo,temperatura,tipo_funciones="auto"):
  
  response_claude = await client.messages.create(
      model=modelo,
      system=sistema,
      messages=messages,
      tools=tools,
      tool_choice={"type": tipo_funciones,"disable_parallel_tool_use":True},
      temperature=temperatura,
      max_tokens=8000
  )

  return response_claude