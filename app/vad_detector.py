import webrtcvad
import audioop
import numpy as np

vad = webrtcvad.Vad(3)

def is_speech_chunk(mulaw_chunk, sample_rate=8000):

    pcm_data = audioop.ulaw2lin(mulaw_chunk, 2)

    return vad.is_speech(pcm_data, sample_rate)

def process_audio_stream(audio_chunks):

    speech_detected = [is_speech_chunk(chunk) for chunk in audio_chunks]
    
    print(f"Speech detected in {sum(speech_detected)} out of {len(speech_detected)} chunks.")
    
    return speech_detected
