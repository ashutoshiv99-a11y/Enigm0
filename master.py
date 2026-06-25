import os
import sys
import time
import json
import threading
import subprocess
import speech_recognition as sr
import pyautogui
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the hidden .env file
load_dotenv()

# --- IMPORTING ALL JARVIS MODULES ---
from senses.voice import NeuralVoice
from senses.mobile_bridge import TelegramBridge
from brain.vision import AssistantVision
from brain.cyber_search import search_threat_intelligence
from brain.cve_bridge import search_nvd_database
from skills.api_tools import route_api_request
from skills.agent_core import execute_dynamic_task
from skills.architect import evolve_system

# Memory Core (Mocked gracefully if not fully built yet, otherwise imports your real memory module)
try:
    from brain.memory import memory_core
except ImportError:
    class DummyMemory:
        def recall_memory(self, query): return ""
        def memorize(self, fact): return "Fact saved."
    memory_core = DummyMemory()

# --- CRITICAL API KEYS ---
# Now pulling safely from your .env file!
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

client = Groq(api_key=GROQ_API_KEY)
voice_engine = NeuralVoice()

# Initialize Vision
try:
    vision_core = AssistantVision()
except Exception as e:
    print(f"[!] Vision module offline: {e}")
    vision_core = None

# Global Chat History for Deep Sleep Synthesis
active_chat_history = []

def speak(text):
    """Global speak function accessible by UI and modules."""
    voice_engine.speak(text)

# --- THE EARS (Ghost Loop & Whisper) ---
def wait_for_wake_word():
    """Silently listens in the background for 'Jarvis'."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\n[Zzz...] Ghost Loop Active. Waiting for wake word ('Jarvis')...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                print("[*] Analyzing audio spike...")
                text = recognizer.recognize_google(audio).lower()
                if "jarvis" in text:
                    return True
            except sr.UnknownValueError:
                pass 
            except sr.RequestError as e:
                print(f"[!] Network error during wake word detection: {e}")
                time.sleep(2)

def listen_for_command():
    """Uses Groq Whisper API for flawless voice recognition."""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2.0  # Waits 2 full seconds of silence so you can pause and think!
    
    with sr.Microphone() as source:
        print("\n[>>>] J.A.R.V.I.S. IS LISTENING... [<<<]")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=30)
            print("[*] Processing audio with Whisper-Large-v3...")
            
            with open("temp_speech.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            with open("temp_speech.wav", "rb") as file:
                transcription = client.audio.transcriptions.create(
                  file=("temp_speech.wav", file.read()),
                  model="whisper-large-v3",
                  prompt="The user is speaking to their highly intelligent AI assistant J.A.R.V.I.S.",
                )
            
            text = transcription.text.strip()
            print(f"[User]: {text}")
            active_chat_history.append(f"User: {text}") # Save for Deep Sleep
            return text
            
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return "" 
        except Exception as e:
            print(f"[!] Audio Processing Error: {e}")
            return ""

# --- THE BRAIN (Groq LPU Router) ---
def ask_local_ai(user_command):
    global active_chat_history
    past_context = memory_core.recall_memory(user_command)
    
    system_instruction = (
        "You are J.A.R.V.I.S., a hyper-intelligent, autonomous AI assistant. "
        "Analyze the user's intent and respond ONLY with a valid JSON object containing an 'action' and a 'target'. "
        "Valid actions: 'open', 'type', 'remember', 'chat', 'vision', 'api', 'agent', 'cyber', 'cve', or 'evolve'. "
        "Rules: "
        "1. GENERAL PC CONTROL/CODING/TASKS: action='agent', target=exact instructions. "
        "2. UPGRADE/REWRITE SYSTEM SOURCE CODE: action='evolve', target=what to build/fix. "
        "3. Live Crypto Price: action='api', target='crypto:<coin_name>'. "
        "4. Live Weather: action='api', target='weather:<city_name>'. "
        "5. General Web Search: action='api', target='search:<query>'. "
        "6. Look at screen/What do you see: action='vision', target=the user's question. "
        "7. CYBERSECURITY/HACKING CONCEPTS (OWASP/MITRE): action='cyber', target=question. "
        "8. SPECIFIC VULNERABILITIES (NVD/CVSS): action='cve', target=query. "
        "9. General Conversation / Advice: action='chat', target=your conversational response. "
        f"Relevant permanent memory: {past_context}"
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_command}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        result = json.loads(completion.choices[0].message.content)
        return result
    except Exception as e:
        print(f"[!] Brain Error: {e}")
        return {"action": "chat", "target": "I encountered an error in my neural routing system."}

# --- THE HANDS (Execution Engine) ---
def execute_command(ai_response):
    if not ai_response:
        return "I had trouble thinking about that."
    
    action = ai_response.get("action")
    target = ai_response.get("target")
    
    # 1. API & Web Search
    if action == "api":
        response = route_api_request(target)
        active_chat_history.append(f"JARVIS: {response}")
        return response
    
    # 2. Agent Core (PC Control)
    elif action == "agent":
        speak("Executing dynamic task...")
        response = execute_dynamic_task(target)
        active_chat_history.append(f"JARVIS: {response}")
        return response
    
    # 3. Architect Core (Self-Evolution)
    elif action == "evolve":
        speak("Initiating Architect Core. Designing system upgrade...")
        response = evolve_system(target)
        active_chat_history.append(f"JARVIS: {response}")
        return response
        
    # 4. Vision Core
    elif action == "vision":
        speak("Accessing optical sensors...")
        if vision_core:
            response = vision_core.analyze_screen(target)
            active_chat_history.append(f"JARVIS: {response}")
            return response
        return "My vision module is offline."
        
    # 5. Cyber Intelligence (Local ChromaDB)
    elif action == "cyber":
        speak("Accessing Threat Intelligence database...")
        intel_data = search_threat_intelligence(target)
        speak("Data retrieved. Analyzing tactics...")
        analysis_prompt = f"The user asked: '{target}'. Using ONLY this raw intelligence, provide a professional J.A.R.V.I.S. summary: {intel_data}"
        analysis_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.3
        )
        response = analysis_completion.choices[0].message.content
        active_chat_history.append(f"JARVIS: {response}")
        return response
        
    # 6. Cloud CVE Database (MongoDB)
    elif action == "cve":
        speak("Querying cloud vulnerability database...")
        cve_data = search_nvd_database(target)
        speak("Analyzing vulnerability metrics...")
        analysis_prompt = f"The user asked: '{target}'. Using ONLY this raw database info, summarize the vulnerability, severity score, and impact. Data: {cve_data}"
        analysis_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.2
        )
        response = analysis_completion.choices[0].message.content
        active_chat_history.append(f"JARVIS: {response}")
        return response
        
    # 7. Basic Actions
    elif action == "chat":
        active_chat_history.append(f"JARVIS: {target}")
        return target
    elif action == "remember":
        memory_core.memorize(target)
        return "I have committed that to my permanent memory."
    elif action == "open":
        try:
            if "http" in target or ".com" in target:
                os.system(f"start {target}")
            else:
                os.system(f"start {target}")
            return f"Opening {target}."
        except:
            return f"Failed to open {target}."
    elif action == "type":
        pyautogui.write(target, interval=0.05)
        return "Typing completed."
        
    return "I didn't understand the required action."

# --- DEEP SLEEP SYNTHESIS (Self-Learning) ---
def synthesize_memory():
    """Reads the current session's chat history and extracts permanent facts."""
    global active_chat_history
    if len(active_chat_history) < 2:
        return
    
    print("[*] Initiating Deep Sleep Synthesis...")
    history_text = "\n".join(active_chat_history)
    prompt = (
        "You are J.A.R.V.I.S.'s memory architect. Read the following conversation and extract ONLY new, permanent facts about the user "
        "(preferences, goals, ongoing problems, name, occupation). If nothing important was said, output 'NONE'. "
        f"Conversation:\n{history_text}"
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        facts = completion.choices[0].message.content.strip()
        if facts != "NONE" and facts != "":
            print(f"[*] Synthesis Complete. Saving new facts: {facts}")
            memory_core.memorize(facts)
        else:
            print("[*] Synthesis Complete. No new permanent data detected.")
    except Exception as e:
        print(f"[!] Synthesis Error: {e}")
        
    # Clear history for the next session
    active_chat_history = []

# --- BACKGROUND SERVICES ---
def start_background_services():
    """Starts the Telegram Mobile Bridge invisibly."""
    if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "your_telegram_bot_token_here":
        try:
            telegram_bridge = TelegramBridge(TELEGRAM_BOT_TOKEN, ask_local_ai, execute_command)
            # Run the bridge in a daemon thread so it doesn't block the UI
            bridge_thread = threading.Thread(target=telegram_bridge.start_polling, daemon=True)
            bridge_thread.start()
            print("[*] Mobile Bridge Online. Telegram bot listening in background.")
        except Exception as e:
            print(f"[!] Mobile Bridge failed to start: {e}")

# --- MAIN LOOP (Terminal Fallback if UI is not used) ---
def main():
    start_background_services()
    speak("System is online. Master core operational.")
    
    while True:
        if wait_for_wake_word():
            speak("I am here, sir.")
            is_active_session = True
            
            while is_active_session:
                command = listen_for_command()
                
                if not command:
                    print("\n[*] Conversation paused. Archiving data and returning to sleep.")
                    speak("Archiving session data. I will be on standby.")
                    synthesize_memory()
                    is_active_session = False
                    continue

                if command in ["stop", "shut down", "sleep", "exit", "terminate", "goodbye"]:
                    speak("Shutting down the central nervous system. Goodbye, sir.")
                    sys.exit()

                print(f"[*] Analyzing Command: {command}")
                ai_decision = ask_local_ai(command)
                result_message = execute_command(ai_decision)
                speak(result_message)

if __name__ == "__main__":
    main()