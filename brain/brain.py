import requests
import json

def ask_local_ai(prompt):
    url = "http://localhost:11434/api/generate"
    
    # We pass the prompt and enforce a JSON response structure
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # Parse the response text into a dictionary
            result = json.loads(response.text)
            return result.get("response")
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# System prompt giving the AI a role
system_instruction = (
    "You are a system automation router. The user will give a command. "
    "Respond ONLY with a JSON object containing an 'action' and a 'target'. "
    "Example: If user says 'open youtube', respond with {'action': 'open', 'target': 'youtube'}."
)

user_command = "Hey assistant, open up youtube"
full_prompt = f"{system_instruction}\nUser command: {user_command}"

print("Sending command to local AI...")
ai_response = ask_local_ai(full_prompt)
print("\nAI Response:")
print(ai_response)