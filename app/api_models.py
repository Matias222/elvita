from collections import deque
from datetime import datetime, time, date
from typing import Literal
from fastapi import WebSocket, BackgroundTasks
from pydantic import BaseModel, Field
from enum import Enum

class Chat(BaseModel):
    persona: str
    ia: str|None=None

class Persona(BaseModel):

    chat: list[Chat]=[]
    nombre: str

class Ejecucion(BaseModel):

    buffer_audio: list=[]
    threshold: float=2
    contador_silencio: int=0
    contador_habla: int=0
    bandera_silencio: bool=False
    stream_sid: str=""
    persona: Persona
    espacio_blanco: float=0
    iteracion_actual: int=0

class Respuesta(BaseModel):

    respuesta: str