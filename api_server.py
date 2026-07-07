import uvicorn
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import master  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n[*] React UI connected to ENIGM0 via WebSockets!")
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_msg = payload.get("message", "")
            
            print(f"[Nexus UI]: Received command -> {user_msg}")
            
            await websocket.send_json({
                "role": "system",
                "text": "Command received. Accessing neural pathways..."
            })
            
            # Log the user's message to the central brain's history
            master.active_chat_history.append(f"User: {user_msg}")
            
            def process_ai():
                # Just ask the brain normally. The brain will handle the memory itself!
                ai_decision = master.ask_local_ai(user_msg)
                action = ai_decision.get("action", "chat")
                res = master.execute_command(ai_decision)
                return action, res
                
            action, result_message = await asyncio.to_thread(process_ai)
            
            await websocket.send_json({
                "role": "jarvis",
                "action": action,
                "text": result_message
            })
            
            asyncio.create_task(asyncio.to_thread(master.speak, result_message))
            
    except WebSocketDisconnect:
        print("\n[!] React UI Disconnected from WebSockets.")

if __name__ == "__main__":
    print("[*] J.A.R.V.I.S. API Bridge Online on Port 8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)