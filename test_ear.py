import os
import io
import wave
import asyncio
import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from groq import Groq
from test_voice import speak


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("No API Key for the LLM found")

client  = Groq(api_key = GROQ_API_KEY)

SAMPLE_RATE = 16000

def record_audio(duration_seconds: int =5)->bytes:
    """Records audio from your microphone and returns WAV bytes in memory."""
    print(f"\n[LISTENING] Speak into your mic now ({duration_seconds} seconds)...")


    audio_data = sd.rec(
        int(duration_seconds*SAMPLE_RATE),
        samplerate= SAMPLE_RATE,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    peak_volume = np.max(np.abs(audio_data))
    rms_volume = np.sqrt(np.mean(audio_data.astype(np.float32)**2))


    if peak_volume<500 or rms_volume<150:
        print(f"[SILENCE] No speech detected (Peak Volume: {peak_volume}). Ignoring.")
        return b""

    
    print("[PROCESSING] Audio captured. Transcribing with Wisper...")

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer,"wb")as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    wav_buffer.seek(0)
    return wav_buffer.read()


def transcribe(audio_bytes : bytes)-> str:
    """Sends recorded WAV bytes to Groq Whisper for sub-200ms transcription."""
    if not audio_bytes:
        return ""
    transcription =client.audio.transcriptions.create(
        file=("input.wav",audio_bytes),
        model = "whisper-large-v3",
        language="en"
    )

    return transcription.text.strip()


if __name__ == "__main__":
    input("Press [ENTER] when ready to speak...")
    
    # Capture & Transcribe
    audio = record_audio(duration_seconds=5)
    text = transcribe(audio)
    
    print(f"\n[YOU SAID]: \"{text}\"")
    
    # Friday responds verbally with what she heard
    if text:
        asyncio.run(speak(f"I heard you loud and clear, boss. You said: {text}"))
    else:
        asyncio.run(speak("I didn't catch that, boss. Microphone received silence."))