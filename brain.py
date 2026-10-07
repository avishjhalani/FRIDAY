import os
import asyncio
from dotenv import load_dotenv
from groq import Groq
from test_voice import speak
from test_ear import record_audio, transcribe

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise ValueError("Key not Found")

client = Groq(api_key=GROQ_KEY)

System_Prompt = {
    "role":"system",
    "content":("You are FRIDAY highly capable, intelligent, loyal, and slightly witty AI assistant. "
        "Keep your spoken answers concise, natural, and crisp (usually 1 to 2 sentences max) "
        "so they are fast and pleasant to hear aloud. Address the user as 'boss' occasionally.")
}

conversation_history =[System_Prompt]

def askFriday(user_prompt:str)->str:
    conversation_history.append({"role":"user","content":user_prompt})

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=conversation_history,
        temperature=0.7,
        max_tokens=500 
    )

    reply = response.choices[0].message.content or ""
    reply = reply.strip()
    
    # Fallback if model ever returns blank
    if not reply:
        reply = "All systems operational,boss. Standing by for your command."
        
    conversation_history.append({"role":"assistant","content":reply})
    return reply


async def conversation_loop():
    await speak("Online and listening,Boss. What are we working on today!")

    while True:
        input("\nPress {ENTER] to speak(or Ctrl+c to stop)}")

        audio = record_audio(duration_seconds=5)
        user_text = transcribe(audio)

        if not user_text:
            await speak("I didn't catch anything, boss. Standing By. ")
            continue

        print(f"\n [YOU]:{user_text}")

        if any(word in user_text.lower() for word in ["shut down", "exit", "quit", "goodbye"]):
            await speak("Powering down primary systems. Have a good one, boss.")
            break

        print("[THINKING] Friday is Processing...")

        ai_reply = askFriday(user_text)

        await speak(ai_reply)

if __name__ =="__main__":
    try:
        asyncio.run(conversation_loop())
    except (KeyboardInterrupt,EOFError):
        print("\n Session Ended")

