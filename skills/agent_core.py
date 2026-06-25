import subprocess
import json
import os
import re
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the hidden .env file
load_dotenv()

# --- PULL GROQ API KEY SAFELY FROM .ENV ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def execute_dynamic_task(task_description):
    """The Iterative Terminal Loop: Enigm0 acts as a sysadmin to solve complex tasks step-by-step."""
    print(f"\n[***] NEXUS PROTOCOL INITIATED: {task_description} [***]")
    
    # We teach Enigm0 how to use the hidden terminal
    system_prompt = """You are Enigm0, a 'God-Mode' AI agent running on a Windows PC. 
You have absolute control over the system. You accomplish tasks by executing terminal commands iteratively.

You have 3 tools at your disposal:
1. Windows PowerShell: Wrap your command in <powershell> and </powershell>
2. Python Execution: Wrap your script in <python> and </python>
3. Task Complete: Wrap your final response to the user in <done> and </done>

You operate in a loop. You will output a command, I will run it and give you the terminal output. 
You will read the output, think, and output the next command. 
Keep doing this until the task is completely solved. 
If an error occurs, read the error and try a different approach. Do not ask for user help.

Example Workflow:
AI: <powershell>ping google.com</powershell>
User: [Terminal Output] Reply from 142.250.190.46: bytes=32 time=14ms TTL=116
AI: <done>Your internet is online, sir. Ping is 14ms.</done>
"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Task: {task_description}"}
    ]
    
    # Allow Enigm0 up to 8 steps to figure out complex problems
    max_steps = 8 
    
    for step in range(max_steps):
        print(f"\n[*] Agent Step {step + 1}/{max_steps} - Thinking...")
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=messages,
                temperature=0.1, # Keep it highly logical
                max_tokens=1024,
            )
            
            ai_response = completion.choices[0].message.content.strip()
            messages.append({"role": "assistant", "content": ai_response})
            
            # 1. Did the AI finish the task?
            done_match = re.search(r'<done>(.*?)</done>', ai_response, re.DOTALL)
            if done_match:
                final_result = done_match.group(1).strip()
                print(f"[+] Task Complete! Result: {final_result}")
                return final_result
                
            # 2. Did the AI write a PowerShell command?
            ps_match = re.search(r'<powershell>(.*?)</powershell>', ai_response, re.DOTALL)
            if ps_match:
                cmd = ps_match.group(1).strip()
                print(f"[>] Executing PowerShell:\n{cmd}")
                
                try:
                    # Execute the PowerShell command silently in the background
                    process = subprocess.run(
                        ["powershell", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                        capture_output=True, text=True, timeout=20
                    )
                    output = process.stdout.strip() + "\n" + process.stderr.strip()
                    if not output.strip():
                        output = "Command executed successfully with no terminal output."
                except subprocess.TimeoutExpired:
                    output = "Error: Command timed out after 20 seconds. Try a different approach."
                except Exception as e:
                    output = f"System Error: {e}"
                    
                print(f"[<] Reading Terminal Output...")
                # Feed the terminal output BACK into the AI's brain for the next loop!
                messages.append({"role": "user", "content": f"Terminal Output:\n{output}"})
                continue
                
            # 3. Did the AI write a Python script?
            py_match = re.search(r'<python>(.*?)</python>', ai_response, re.DOTALL)
            if py_match:
                code = py_match.group(1).strip()
                print(f"[>] Executing Python Script:\n{code}")
                temp_script = "./skills/temp_agent_script.py"
                with open(temp_script, "w", encoding="utf-8") as f:
                    f.write(code)
                try:
                    process = subprocess.run(["python", temp_script], capture_output=True, text=True, timeout=20)
                    output = process.stdout.strip() + "\n" + process.stderr.strip()
                    if not output.strip():
                        output = "Python script executed successfully with no output."
                except subprocess.TimeoutExpired:
                    output = "Error: Python script timed out after 20 seconds."
                except Exception as e:
                    output = f"System Error: {e}"
                    
                if os.path.exists(temp_script):
                    os.remove(temp_script)
                    
                print(f"[<] Reading Python Output...")
                messages.append({"role": "user", "content": f"Python Output:\n{output}"})
                continue
                
            # 4. Failsafe if the AI forgets its formatting
            print("[!] AI did not use correct formatting tags. Correcting...")
            messages.append({"role": "user", "content": "System Error: You must wrap your commands in <powershell>, <python>, or <done> tags. Try again."})
            
        except Exception as e:
            return f"Agent Core encountered a critical network error: {e}"
            
    return "I attempted the task but reached the maximum number of iterations without solving it."

# Quick test block
if __name__ == "__main__":
    print(execute_dynamic_task("Find out what my current Wi-Fi network name is."))