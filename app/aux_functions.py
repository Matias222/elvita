import uuid
import audioop
import numpy as np
from scipy.io import wavfile

def save_audio_from_chunks(chunks):
    # Combine all audio chunks
    audio_data = b''.join(chunks)
    
    # Properly convert μ-law to 16-bit linear PCM using audioop.ulaw2lin
    pcm_audio = audioop.ulaw2lin(audio_data, 2)
    
    # Save the decoded PCM audio to a .wav file
    filename = f"./app/audios/{uuid.uuid4()}.wav"
    wavfile.write(filename, 8000, np.frombuffer(pcm_audio, dtype=np.int16))
    
    print(f"Saved audio as: {filename}")
    return filename
