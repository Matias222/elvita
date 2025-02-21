from app import api_models, ai_wrappers
from app.prompts import elvita, dulce, maxilar_demo
from datetime import datetime
from dotenv import load_dotenv

import json
import asyncio
import litellm

load_dotenv()

async def conversa(ejecucion:api_models.Ejecucion):

    messages=[{"role": "system", "content": maxilar_demo.sistema_prompt(ejecucion)}]

    messages.append({"role": "user","content": maxilar_demo.usuario_prompt(ejecucion)})

    for i in ejecucion.persona.chat: 

        messages.append({"role": "user", "content": str({"respuesta":i.persona})})
        if(i.ia!=None): messages.append({"role": "assistant", "content": str({"respuesta":i.ia})})

    if(len(ejecucion.persona.chat)==1): return "Buenas tardes doctor Diego. La señora Torres de la extracción de las 2pm, presente sangrado y un excesivo dolor. Quiere verlo. ¿Qué hacemos?"
    if(len(ejecucion.persona.chat)==2): return "Sí, revisé con ella el protocolo paso a paso. Tomó el naproxeno hace 3 horas pero el dolor está aumentando. Ya le pedí fotos y se ve más inflamada de lo normal."
    if(len(ejecucion.persona.chat)==3): return "Sí doctor, puedo acomodarla en dos horas. Ya reorganicé la agenda para una atención de emergencia."

    response = await ai_wrappers.call_open(messages,api_models.Respuesta,temperatura=0.55)

    respuesta_json = json.loads(response.choices[0].message.content)

    return respuesta_json["respuesta"]


#Tu objetivo es preguntarle a Enzo cuando llega a Lima porque en base a eso Matias comprara el 'dulce'
#Si te preguntan que es dulce tu dices que es hierba buena o I wanna love you de Bob Marley.
#Consigue la fecha de su viaje.
#Tu unico objetivo es hablar conmigo.
#Mi nombre -> {api_state.persona.nombre}
#Nuestra conversacion -> {api_state.persona.chat}