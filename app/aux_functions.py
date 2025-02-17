import uuid
import audioop
import numpy as np
from scipy.io import wavfile

def save_audio_from_chunks(chunks):
    audio_data = b''.join(chunks)
    
    pcm_audio = audioop.ulaw2lin(audio_data, 2)
    
    filename = f"./app/audios/{uuid.uuid4()}.wav"
    wavfile.write(filename, 8000, np.frombuffer(pcm_audio, dtype=np.int16))
    
    print(f"Saved audio as: {filename}")
    return filename

def get_audio_duration_ms(chunks, sample_rate=8000):

    total_samples = len(b''.join(chunks))
    duration_ms = (total_samples / sample_rate) * 1000
    return round(duration_ms)
