import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# API Keys & Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Email Configuration
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")

# Voice & Audio Configuration
# Kerry Condon / Irish female accent matching Friday from MCU
FRIDAY_VOICE = "en-IE-EmilyNeural"  
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# LLM Model Configuration
# High-speed versatile Llama 3.3 70B via Groq
LLM_MODEL = "llama-3.3-70b-versatile"
WHISPER_MODEL = "whisper-large-v3"
