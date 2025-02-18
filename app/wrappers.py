from app import aux_functions, api_models, ai_calls, emma
import time
import math

async def pipeline(ejecucion:api_models.Ejecucion):

    audio_guardado=aux_functions.save_audio_from_chunks(ejecucion)

    st=time.time()

    texto=await ai_calls.transcript(audio_guardado)

    print("Transcripcion ->",texto)

    ejecucion.persona.chat.append(api_models.Chat(persona=texto))

    respuesta=await emma.conversa(ejecucion)

    print("IA ->",respuesta)

    ejecucion.persona.chat[-1].ia=respuesta

    voz=await ai_calls.generar_voz(respuesta)

    tiempo_total=time.time()-st

    ejecucion.frames_respuesta=math.floor((aux_functions.get_audio_duration_ms(voz)*1.0/len(voz))/20.)

    ejecucion.espacio_blanco=tiempo_total*1.1*50+ejecucion.iteracion_actual#+aux_functions.get_audio_duration_ms(voz)/20

    print("Tiempo total demorado ->",tiempo_total,"Frames por respuesta ->",ejecucion.frames_respuesta)

    return voz