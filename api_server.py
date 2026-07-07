import uvicorn
import json
import asyncio
import threading
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Connects directly to your existing J.A.R.V.I.S. brain
import master  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE INVISIBLE BACKGROUND VOICE LOOP ---
def autonomous_voice_core():
    """Runs 24/7 in the background, listening for the wake word."""
    print("[*] Autonomous Voice Core Online. Awaiting 'Hey Jarvis'...")
    
    # Initialize sensors and background bridges (like Telegram)
    try:
        master.start_background_services()
    except Exception:
        pass
    
    time.sleep(2)
    # Give a brief audio confirmation that he has successfully booted in the background
    master.speak("System online. I am running in the background, sir.")
    
    while True:
        try:
            # 1. Wait silently for "Hey Jarvis"
            if master.wait_for_wake_word():
                master.speak("I am here, sir.")
                
                is_active_session = True
                while is_active_session:
                    # 2. Listen for your command
                    command = master.listen_for_command()
                    
                    if not command:
                        master.speak("Standing by.")
                        is_active_session = False
                        continue
                        
                    if command.lower() in ["stop", "shut down", "sleep", "exit", "goodbye"]:
                        master.speak("Returning to deep sleep.")
                        is_active_session = False
                        continue
                    
                    print(f"[*] Voice Command Received: {command}")
                    
                    # 3. Process the command using the Local Swarm Brain
                    ai_decision = master.ask_local_ai(command)
                    result_message = master.execute_command(ai_decision)
                    
                    # 4. Speak the final result out loud
                    master.speak(result_message)
                    
        except Exception as e:
            print(f"[!] Voice Engine Error: {e}")
            time.sleep(2)

# Start the invisible voice engine before the web server even boots up!
threading.Thread(target=autonomous_voice_core, daemon=True).start()


# --- THE WEBSOCKET PIPELINE (For the Optional React UI) ---
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n[*] React UI connected to ENIGM0 via WebSockets!")
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_msg = payload.get("message", "")
            
            await websocket.send_json({"role": "system", "text": "Command received. Accessing neural pathways..."})
            
            master.active_chat_history.append(f"User: {user_msg}")
            
            def process_ai():
                ai_decision = master.ask_local_ai(user_msg)
                action = ai_decision.get("action", "chat")
                
                if action == "chat":
                    recent_memory = "\n".join(master.active_chat_history[-6:])
                    memory_injected_query = f"Recent Conversation Context:\n{recent_memory}\n\nUser's Current Command: {user_msg}"
                    ai_decision["target"] = memory_injected_query
                
                res = master.execute_command(ai_decision)
                master.active_chat_history.append(f"J.A.R.V.I.S.: {res}")
                return action, res
                
            action, result_message = await asyncio.to_thread(process_ai)
            
            await websocket.send_json({"role": "jarvis", "action": action, "text": result_message})
            asyncio.create_task(asyncio.to_thread(master.speak, result_message))
            
    except WebSocketDisconnect:
        print("\n[!] React UI Disconnected from WebSockets.")

if __name__ == "__main__":
    print("[*] J.A.R.V.I.S. Nexus API Online (Port 8000)")
    uvicorn.run(app, host="127.0.0.1", port=8000)