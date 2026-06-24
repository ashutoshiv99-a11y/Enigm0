import subprocess
import json
import base64
import os
from PIL import ImageGrab
import requests

class AssistantVision:
    def __init__(self):
        # We need a temporary location to save the screenshot before sending it to the AI
        self.screenshot_path = "./brain/current_view.png"
        print("[*] Vision Core Initialized.")

    def capture_screen(self):
        """Takes a silent screenshot of the primary monitor."""
        try:
            print("[*] Capturing screen...")
            screenshot = ImageGrab.grab()
            screenshot.save(self.screenshot_path)
            return True
        except Exception as e:
            print(f"[!] Failed to capture screen: {e}")
            return False

    def encode_image(self):
        """Converts the image into a base64 string that the local LLM can understand."""
        with open(self.screenshot_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_screen(self, query):
        """Captures the screen and asks the local vision model about it."""
        if not self.capture_screen():
            return "I am unable to see the screen right now."

        base64_image = self.encode_image()
        
        # We must use a vision-capable model. LLaVA is the standard for local vision.
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llava", 
            "prompt": query,
            "images": [base64_image],
            "stream": False
        }

        print("[*] Analyzing image data...")
        try:
            response = requests.post(url, json=payload)
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
    print("Taking a screenshot and asking the AI what it sees...")
    result = vision.analyze_screen("Describe what is on the screen right now.")
    print(f"\nAI Vision Analysis:\n{result}")