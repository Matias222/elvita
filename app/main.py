from app import api_models, vad_detector, ai_calls, wrappers

from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream
from fastapi.responses import HTMLResponse, JSONResponse

import websockets, os, base64, json, base64, time

monolito = FastAPI(title="Elvita API")

monolito.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@monolito.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):

    form_data = await request.form()  # Get the incoming Twilio request data

    caller_number = form_data.get("To", "Unknown")  # Extract the caller's phone number

    response = VoiceResponse()
    
    host = request.url.hostname
    connect = Connect()
    
    connect.stream(
        url=f"wss://e3ca-2800-200-ea80-14e-7c14-a6c9-5d3c-88ce.ngrok-free.app/media-stream",
        parameter1_name="numero_celular",
        parameter1_value=caller_number
    )

    response.append(connect)

    return HTMLResponse(content=str(response), media_type="application/xml")

@monolito.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):

    ejecucion=api_models.Ejecucion(persona=api_models.Persona(nombre="Mercedes",nombre_asistente="Elvita"))

    print("Client connected")

    await websocket.accept()

    conectado=await websocket.receive_json()
    info_call=await websocket.receive_json()

    print(info_call)

    ejecucion.stream_sid=info_call['start']['streamSid']

    while(True):
        
        chunk_json=await websocket.receive_json()

        ejecucion.iteracion_actual=int(chunk_json["sequenceNumber"])

        if(ejecucion.iteracion_actual<ejecucion.espacio_blanco): continue

        ejecucion.buffer_audio.append(base64.b64decode(chunk_json["media"]["payload"]))

        if(vad_detector.is_speech_chunk(ejecucion.buffer_audio[-1])==False): ejecucion.contador_silencio+=1
        else: 
            ejecucion.contador_habla+=1
            if(ejecucion.contador_habla>=10 and ejecucion.bandera_silencio==True): ejecucion.contador_silencio=0

        if(ejecucion.contador_silencio>=ejecucion.threshold*50):
            
            if(ejecucion.bandera_silencio==False): 
                
                voz=await wrappers.pipeline(ejecucion)

                for fragmento in voz:

                    await websocket.send_json(
                        {
                            "event": "media",
                            "streamSid": ejecucion.stream_sid,
                            "media": {
                                "payload": base64.b64encode(fragmento).decode('utf-8')
                            }
                        }
                    )

                ejecucion.buffer_audio=ejecucion.buffer_audio[-1:]
                ejecucion.threshold=3.5
                ejecucion.contador_habla=0
            
            ejecucion.bandera_silencio=True

            print("Silencio")

        else:
            ejecucion.bandera_silencio=False
            print("Hablando")

        #acumular hasta cierto threshold luego vad filter, en base a eso openai clals
        #como hago para procesar mientras el bucket sigue? al final todas las calls se acumulan, no? igual todo puede ser asincrono? y espero al vacio y ahi lo mando?

        pass

    return

@monolito.get("/")
def hola():
    return "Hola a todos"
