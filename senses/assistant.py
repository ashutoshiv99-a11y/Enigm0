import requests
import json
import webbrowser
import subprocess
import pyautogui
import time

# --- THE BRAIN ---
def ask_local_ai(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = json.loads(response.text)
            return json.loads(result.get("response")) # Parse the JSON string into a Python dictionary
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection Error: {str(e)}")
        return None

# --- THE HANDS ---
def execute_command(ai_response):
    if not ai_response:
        return
    
    action = ai_response.get("action")
    target = ai_response.get("target")
    
    print(f"\n[*] Attempting to execute -> Action: '{action}', Target: '{target}'")
    
    # 1. Handling 'Open' commands
    if action == "open":
        if target == "youtube":
            print("[*] Launching web browser...")
            webbrowser.open("https://www.youtube.com")
        
        elif target == "notepad":
            print("[*] Launching Notepad...")
            subprocess.Popen(["notepad.exe"])
            
        else:
            print(f"[!] I don't know how to open '{target}' yet. You need to program this target.")
            
    # 2. Handling 'Type' commands (Using PyAutoGUI)
    elif action == "type":
        print(f"[*] Typing: {target}")
        pyautogui.write(target, interval=0.05)
        
    else:
        print(f"[!] Unknown action: '{action}'")

# --- THE LOOP ---
system_instruction = (
    "You are a system automation router. The user will give a command. "
    "Respond ONLY with a JSON object containing an 'action' (must be 'open' or 'type') and a 'target'. "
    "Examples: "
    "User says 'open up youtube' -> {'action': 'open', 'target': 'youtube'}. "
    "User says 'start notepad' -> {'action': 'open', 'target': 'notepad'}. "
    "User says 'type hello world' -> {'action': 'type', 'target': 'hello world'}."
)

# Test Command 1: Opening a web page
user_command = "Hey assistant, can you open up youtube for me?"
print(f"User: {user_command}")

full_prompt = f"{system_instruction}\nUser command: {user_command}"
response_dict = ask_local_ai(full_prompt)

# Pass the AI's decision to the Hands
execute_command(response_dict)