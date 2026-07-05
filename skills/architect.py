import os
import re
from groq import Groq
from dotenv import load_dotenv

# --- SECURELY LOAD API KEYS ---
# This automatically reads your .env file so keys are never hardcoded!
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("[!] ERROR: GROQ_API_KEY is missing from your .env file!")

client = Groq(api_key=GROQ_API_KEY)

def evolve_system(upgrade_request):
    """Allows J.A.R.V.I.S. to write new permanent modules or edit his own source code."""
    print(f"\n[***] SYSTEM ARCHITECT ENGAGED [***]")
    print(f"[*] Analyzing Upgrade Request: '{upgrade_request}'")
    
    # Check if the user is asking to modify an existing file (e.g., master.py, agent_core.py)
    existing_code_context = ""
    target_file = None
    
    # Basic scan to see if a specific file was mentioned
    common_files = ["master.py", "agent_core.py", "api_tools.py", "routines.py", "mobile_bridge.py", "voice.py", "vision.py", "memory.py"]
    for file in common_files:
        if file in upgrade_request:
            target_file = file
            break
            
    if target_file:
        # Search for the file in the project directories to read its current brain
        search_dirs = ["./", "./skills/", "./brain/", "./senses/"]
        for d in search_dirs:
            potential_path = os.path.join(d, target_file)
            if os.path.exists(potential_path):
                with open(potential_path, "r", encoding="utf-8") as f:
                    existing_code_context = f.read()
                print(f"[*] Read existing source code from {target_file} for context.")
                break

    system_prompt = (
        "You are the System Architect of an advanced AI named J.A.R.V.I.S. "
        "The user wants you to upgrade your own system, add a new permanent feature, or fix a bug in your code. "
        "You must output exactly two things formatted with special tags: "
        "1. The filepath to save the code using <filepath>filename.py</filepath>. If it is a new skill, save it in ./skills/new_skill_name.py. "
        "2. The complete, fully functional Python code using <python> ... </python>. "
        "Do NOT output any other text or markdown outside of these tags."
    )
    
    if existing_code_context:
        system_prompt += f"\n\nNote: The user wants to modify {target_file}. Here is the current source code for it. Rewrite the ENTIRE file with the requested fix/upgrade:\n\n{existing_code_context}"

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": upgrade_request}
            ],
            temperature=0.1,
            max_tokens=6000 # Give him maximum memory to write huge files
        )
        
        response_text = completion.choices[0].message.content
        
        # Extract the filepath and the code
        filepath_match = re.search(r'<filepath>(.*?)</filepath>', response_text, re.IGNORECASE)
        code_match = re.search(r'<python>(.*?)</python>', response_text, re.IGNORECASE | re.DOTALL)
        
        if filepath_match and code_match:
            save_path = filepath_match.group(1).strip()
            new_code = code_match.group(1).strip()
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else ".", exist_ok=True)
            
            # Overwrite or create the file
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(new_code)
                
            return f"Upgrade complete. I have written the new system architecture to {save_path}."
        else:
            return "I failed to format the architecture upgrade correctly. Please check my output logs."
            
    except Exception as e:
        return f"A critical error occurred in the System Architect core: {e}"

# Quick Test
if __name__ == "__main__":
    print(evolve_system("Write a new skill module that can download a youtube video given a URL."))