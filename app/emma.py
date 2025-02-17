from app import api_models, ai_wrappers
from datetime import datetime
from dotenv import load_dotenv

import json
import asyncio
import litellm

load_dotenv()

async def conversa(api_state:api_models.Ejecucion):

    messages=[{
        "role": "system", 
        "content": """Eres mi amigo hablemos."""
    }]

    messages.append({
        "role": "user",
        "content": f"""
        Te llamas Hector Testuri.
        Y eres mi ex enamorado de hace 25 años.
        Tu unico objetivo es hablar conmigo.
        Mi nombre -> {api_state.persona.nombre}
        Nuestra conversacion -> {api_state.persona.chat}
        """
    })

    response = await ai_wrappers.call_open(messages,api_models.Respuesta,temperatura=0.6)

    respuesta_json = json.loads(response.choices[0].message.content)

    return respuesta_json["respuesta"]
