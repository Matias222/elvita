import uuid
import audioop
import numpy as np
from scipy.io import wavfile

from datetime import datetime, timedelta
from app import api_models
import pytz
from dotenv import load_dotenv

load_dotenv()

peru_tz=pytz.timezone("America/Lima")

def save_audio_from_chunks(ejecucion:api_models.Ejecucion):

    audio_data = b''.join(ejecucion.buffer_audio)
    
    pcm_audio = audioop.ulaw2lin(audio_data, 2)
    
    filename = f"./app/audios/{ejecucion.persona.nombre}_{ejecucion.iteracion_actual}.wav"
    wavfile.write(filename, 8000, np.frombuffer(pcm_audio, dtype=np.int16))
    
    print(f"Saved audio as: {filename}")
    return filename

def get_audio_duration_ms(chunks, sample_rate=8000):

    total_samples = len(b''.join(chunks))
    duration_ms = (total_samples / sample_rate) * 1000
    return round(duration_ms)

def datetime_peru():
    
    peru_time = datetime.now(peru_tz)

    return peru_time.isoformat()

def dia_semana(peru_time:str="Default"):

    if(peru_time=="Default"): peru_time = datetime.now(peru_tz)
    else:  peru_time=datetime.strptime(peru_time, "%Y-%m-%d").date()

    weekday_number = peru_time.weekday()

    days_in_spanish = {
        0: "Lunes",
        1: "Martes",
        2: "Miercoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sabado",
        6: "Domingo"
    }
    
    return days_in_spanish[weekday_number]