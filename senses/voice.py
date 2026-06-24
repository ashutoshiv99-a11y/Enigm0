import edge_tts
import asyncio
import pygame
import os
import time

class NeuralVoice:
    def __init__(self):
        # We use a British Male voice to mimic J.A.R.V.I.S.
        # Other options: "en-US-ChristopherNeural" (US Male), "en-US-AriaNeural" (US Female)
        self.voice_model = "en-GB-RyanNeural" 
        self.temp_audio_file = "./senses/temp_speech.mp3"
        print("[*] Neural Voice Engine (Cloud TTS) Initialized.")

    async def _generate_audio(self, text):
        """Asynchronously contacts the cloud to generate the audio file."""
        communicate = edge_tts.Communicate(text, self.voice_model, rate="+10%")
        await communicate.save(self.temp_audio_file)

    def speak(self, text):
        """Generates and plays realistic speech."""
        print(f"\nEnigm0: {text}")
        
        # 1. Contact the cloud and generate the audio
        asyncio.run(self._generate_audio(text))
        
        # 2. Play the audio using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(self.temp_audio_file)
        pygame.mixer.music.play()
        
        # 3. Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # 4. Cleanup and delete the temporary file
        pygame.mixer.quit()
        time.sleep(0.1) # Brief pause to let Windows release the file
        try:
            os.remove(self.temp_audio_file)
        except Exception as e:
            pass

# Quick test block
if __name__ == "__main__":
    voice = NeuralVoice()
    voice.speak("Good evening, sir. My neural voice engine is online and fully operational.")