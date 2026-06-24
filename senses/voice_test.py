import pyttsx3
import speech_recognition as sr

# --- THE VOICE (Speaking) ---
# Initialize the offline text-to-speech engine
engine = pyttsx3.init()

# Optional: Speed up or slow down the speaking rate
engine.setProperty('rate', 170) 

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# --- THE EARS (Listening) ---
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[*] Calibrating microphone... please stay quiet for a second.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[*] Listening! Go ahead and speak...")
        
        # Capture the audio
        audio = recognizer.listen(source)
        
    try:
        print("[*] Processing speech...")
        # Note: We are using the default online recognizer just to verify your hardware works. 
        # We can swap this to a 100% offline Whisper model later if you want strict privacy.
        text = recognizer.recognize_google(audio)
        print(f"You said: '{text}'")
        return text
        
    except sr.UnknownValueError:
        print("[!] Sorry, I couldn't catch that. Could be background noise.")
        return None
    except sr.RequestError as e:
        print(f"[!] Network error: {e}")
        return None

# --- TEST THE LOOP ---
if __name__ == "__main__":
    speak("System initialized. I am listening. Say a test phrase.")
    
    # Trigger the microphone
    user_input = listen()
    
    # Repeat back what was heard
    if user_input:
        speak(f"I heard you say: {user_input}")
    else:
        speak("I didn't receive any clear audio.")