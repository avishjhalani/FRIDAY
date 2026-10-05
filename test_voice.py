import asyncio
import os
import edge_tts
import pygame


# initialize pygame mixer for playing the audio
pygame.mixer.init()

VOICE = "en-IE-EmilyNeural"

async def speak(text:str):
    """
    Synthesizes text into speech and plays it through your speakers.
    """
    print(f"\n [FRIDAY]:{text}")

    temp_audio ="friday_voice.mp3"


    communicate = edge_tts.Communicate(text,VOICE)
    await communicate.save(temp_audio)

    pygame.mixer.music.load(temp_audio)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(2)

    pygame.mixer.music.unload()
    if os.path.exists(temp_audio):
        os.remove(temp_audio)


if __name__ =="__main__":
    print("Testing the text to speech output of the system ...")
    asyncio.run(speak("system initialized, boss. All primary audio circuits are online . Let the fun begin."))

