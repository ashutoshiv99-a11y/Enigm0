import subprocess
import json
import base64
import os
import threading
import time
import pyautogui
from PIL import ImageGrab, ImageDraw
import requests

class AssistantVision:
    def __init__(self):
        # We need a temporary location to save the screenshot before sending it to the AI
        self.screenshot_path = "./brain/current_view.png"
        self.latest_frame = None
        self.is_watching = True
        
        print("[*] Vision Core Initialized. Starting Continuous Optical Stream...")
        # --- NEW: Start the continuous optical stream in the background ---
        self.vision_thread = threading.Thread(target=self._optical_stream, daemon=True)
        self.vision_thread.start()

    def _optical_stream(self):
        """Continuously captures the screen into a buffer so J.A.R.V.I.S. always has a live feed."""
        while self.is_watching:
            try:
                # Grab the screen instantly
                frame = ImageGrab.grab()
                
                # Get the exact X, Y coordinates of your mouse cursor
                mx, my = pyautogui.position()
                
                # Draw a bright red targeting circle around the mouse cursor
                # so the AI knows exactly what you are pointing at!
                draw = ImageDraw.Draw(frame)
                radius = 40
                draw.ellipse((mx - radius, my - radius, mx + radius, my + radius), outline="red", width=6)
                
                # Update the live buffer
                self.latest_frame = frame
                
                # Run the stream at roughly 10 frames per second
                time.sleep(0.1) 
            except Exception as e:
                time.sleep(1)

    def encode_image(self):
        """Converts the image into a base64 string that the local LLM can understand."""
        with open(self.screenshot_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_screen(self, query):
        """Analyzes the LIVE frame from the background optical stream."""
        if not self.latest_frame:
            return "My optical sensors are still booting up. Please wait a moment."

        print("[*] Locking onto target...")
        
        # Save the exact millisecond frame from the live stream
        self.latest_frame.save(self.screenshot_path)
        base64_image = self.encode_image()
        
        url = "http://localhost:11434/api/generate"
        
        # --- NEW: We inject a secret prompt telling the AI to look at the red circle ---
        enhanced_query = f"{query} (Note: The user's mouse cursor is highlighted by the red circle. Focus heavily on what is inside or near the red circle.)"
        
        payload = {
            "model": "llava", 
            "prompt": enhanced_query,
            "images": [base64_image],
            "stream": False
        }

        print("[*] Processing visual data through LLaVA...")
        try:
            # We increase the timeout slightly because LLaVA can take a moment to "think" about images
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                result = json.loads(response.text)
                return result.get("response")
            else:
                return "My vision processing failed to return a result."
        except Exception as e:
            return f"Vision Core Error: {str(e)}"

# Quick test block
if __name__ == "__main__":
    vision = AssistantVision()
    time.sleep(1) # Wait 1 second for the optical stream to grab the first frame
    print("Taking a screenshot and asking the AI what it sees...")
    result = vision.analyze_screen("Describe what I am pointing at right now.")
    print(f"\nAI Vision Analysis:\n{result}")