from app import aux_functions, api_models, ai_calls, emma
import time

async def pipeline(ejecucion:api_models.Ejecucion):

    audio_guardado=aux_functions.save_audio_from_chunks(ejecucion.buffer_audio)

    st=time.time()

    texto=await ai_calls.transcript(audio_guardado)

    print("Transcripcion ->",texto)

    ejecucion.persona.chat.append(api_models.Chat(persona=texto))

    respuesta=await emma.conversa(ejecucion)

    print("IA ->",respuesta)

    ejecucion.persona.chat[-1].ia=respuesta

    voz=await ai_calls.generar_voz(respuesta)

    ejecucion.espacio_blanco=int((time.time()-st)*1.15*50)+ejecucion.iteracion_actual

    return voz