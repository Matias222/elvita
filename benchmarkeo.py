from deepgram import DeepgramClient, PrerecordedOptions
from app import ai_calls

import time, os, asyncio, httpx

DEEPGRAM_API_KEY = 'BENCH'

deepgram = DeepgramClient(DEEPGRAM_API_KEY)

async def deep_trans(file_path):
    
    with open(file_path, 'rb') as buffer_data:
    
        # STEP 1 Create a Deepgram client using the DEEPGRAM_API_KEY from environment variables
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        # STEP 2 Call the transcribe_url method on the prerecorded class
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            language="es-419",
            keywords=["Lima:3"]
        )

        payload = { 'buffer': buffer_data }

        response = deepgram.listen.rest.v("1").transcribe_file(
            payload, options#, timeout=httpx.Timeout(300.0, connect=10.0)
        )

        transcripcion=response["results"]["channels"][0]["alternatives"][0]["transcript"]

        print(transcripcion)

        return transcripcion
    
async def main():

    folder_path = "audios_variados/abuela"

    for filename in os.listdir(folder_path):
        
        print("*"*50)

        file_path = os.path.join(folder_path, filename)

        st=time.time()

        await deep_trans(file_path)

        print("Deepgram",time.time()-st)

        st=time.time()

        A=await ai_calls.transcript(file_path)

        print("Whisper",time.time()-st)

        print("*"*50)
