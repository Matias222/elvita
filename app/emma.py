from app import api_models, ai_wrappers
from app.prompts import elvita, dulce
from datetime import datetime
from dotenv import load_dotenv

import json
import asyncio
import litellm

load_dotenv()

async def conversa(ejecucion:api_models.Ejecucion):

    messages=[{"role": "system", "content": elvita.sistema_prompt(ejecucion)}]

    messages.append({"role": "user","content": elvita.usuario_prompt(ejecucion)})

    for i in ejecucion.persona.chat: 

        messages.append({"role": "user", "content": str({"respuesta":i.persona})})
        if(i.ia!=None): messages.append({"role": "assistant", "content": str({"respuesta":i.ia})})

    response = await ai_wrappers.call_open(messages,api_models.Respuesta,temperatura=0.55)

    respuesta_json = json.loads(response.choices[0].message.content)

    return respuesta_json["respuesta"]


#Tu objetivo es preguntarle a Enzo cuando llega a Lima porque en base a eso Matias comprara el 'dulce'
#Si te preguntan que es dulce tu dices que es hierba buena o I wanna love you de Bob Marley.
#Consigue la fecha de su viaje.
#Tu unico objetivo es hablar conmigo.
#Mi nombre -> {api_state.persona.nombre}
#Nuestra conversacion -> {api_state.persona.chat}