import asyncio
import os
import edge_tts
import pygame


# initialize pygame mixer for playing the audio
pygame.mixer.init()

VOICE = "en-IE-EmilyNeural"

import asyncio
import io
import edge_tts
import pygame

pygame.mixer.init()
VOICE = "en-IE-EmilyNeural"

async def speak(text: str):
    temp_buffer = io.BytesIO()
    
    # 1. Stream audio chunks directly into RAM (Zero disk writes!)
    communicate = edge_tts.Communicate(text, VOICE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            temp_buffer.write(chunk["data"])
            
    temp_buffer.seek(0)
    
    # 2. Print right when playback actually starts
    print(f"\n[FRIDAY]: {text}")
    
    # 3. Play straight from RAM
    pygame.mixer.music.load(temp_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ =="__main__":
    print("Testing the text to speech output of the system ...")
    asyncio.run(speak("system initialized, boss. All primary audio circuits are online . Let the fun begin."))

