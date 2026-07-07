import edge_tts
import asyncio
import pygame
import os
import time
import uuid

class NeuralVoice:
    def __init__(self):
        self.voice_model = "en-GB-RyanNeural" 
        print("[*] Neural Voice Engine (Cloud TTS) Initialized.")

    async def _generate_audio(self, text, filepath):
        """Asynchronously contacts the cloud to generate the audio file."""
        communicate = edge_tts.Communicate(text, self.voice_model, rate="+10%")
        await communicate.save(filepath)

    def speak(self, text):
        """Generates and plays realistic speech, handles both sync and async contexts."""
        print(f"\nEnigm0: {text}")
        
        unique_audio_file = f"./senses/temp_speech_{uuid.uuid4().hex[:6]}.mp3"
        
        # --- FIX: Properly handle existing event loops without RuntimeError ---
        try:
            loop = asyncio.get_running_loop()
            # If we are in an async loop (FastAPI), we schedule the coroutine 
            # and wait for the result without starting a new loop.
            future = asyncio.run_coroutine_threadsafe(self._generate_audio(text, unique_audio_file), loop)
            future.result() 
        except RuntimeError:
            # If no loop is running (normal terminal), use standard asyncio.run
            asyncio.run(self._generate_audio(text, unique_audio_file))
        
        # --- PLAYBACK ---
        pygame.mixer.init()
        pygame.mixer.music.load(unique_audio_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        time.sleep(0.1) 
        
        try:
            if os.path.exists(unique_audio_file):
                os.remove(unique_audio_file)
        except:
            pass

# Quick test block
if __name__ == "__main__":
    voice = NeuralVoice()
    voice.speak("System bridge diagnostic successful.")