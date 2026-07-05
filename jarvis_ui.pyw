import customtkinter as ctk
import threading
import sys
import os
import time

# --- IMPORT YOUR JARVIS MASTER CORE ---
import master

class RedirectText(object):
    """Intercepts terminal print() statements and sends them to the UI matrix."""
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        # We use 'after' to ensure thread safety when updating the Tkinter GUI
        self.output.after(0, self._write_to_widget, string)

    def _write_to_widget(self, string):
        self.output.insert("end", string)
        self.output.see("end") # Auto-scroll to the bottom

    def flush(self):
        pass

class JarvisUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("J.A.R.V.I.S. Nexus Command Center")
        self.geometry("950x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- UI LAYOUT ---
        # 1. Header Frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=15)

        self.title_label = ctk.CTkLabel(self.header_frame, text="ENIGM0 / J.A.R.V.I.S.", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(side="left")

        self.status_label = ctk.CTkLabel(self.header_frame, text="Status: INITIALIZING...", font=ctk.CTkFont(size=16, weight="bold"), text_color="yellow")
        self.status_label.pack(side="right")

        # 2. Main Console Output (The Brain's Terminal)
        self.console = ctk.CTkTextbox(self, width=900, height=480, font=ctk.CTkFont(family="Consolas", size=14))
        self.console.pack(padx=20, pady=5, fill="both", expand=True)
        
        # Redirect all terminal output to this console
        sys.stdout = RedirectText(self.console)
        sys.stderr = RedirectText(self.console)

        # 3. Manual Override Bar (Bottom)
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=20, pady=15)

        self.input_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Enter manual override command...", width=650, height=40, font=ctk.CTkFont(size=14))
        self.input_entry.pack(side="left", padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_manual_command)

        self.send_button = ctk.CTkButton(self.bottom_frame, text="Execute", command=self.send_manual_command, width=120, height=40, font=ctk.CTkFont(weight="bold"))
        self.send_button.pack(side="left")

        self.power_button = ctk.CTkButton(self.bottom_frame, text="SYSTEM SHUTDOWN", fg_color="#8B0000", hover_color="#FF0000", command=self.shutdown_system, width=120, height=40, font=ctk.CTkFont(weight="bold"))
        self.power_button.pack(side="right")

        # --- START BACKGROUND AI THREAD ---
        self.ai_thread = threading.Thread(target=self.run_jarvis_backend, daemon=True)
        self.ai_thread.start()

    def update_status(self, text, color):
        """Changes the UI status indicator dynamically."""
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def send_manual_command(self, event=None):
        """Allows you to type commands if you don't want to speak."""
        command = self.input_entry.get()
        if command:
            print(f"\n[MANUAL OVERRIDE]: {command}")
            self.input_entry.delete(0, 'end')
            
            # Run the AI logic in a quick sub-thread so it doesn't freeze the UI
            threading.Thread(target=self.process_text_command, args=(command,), daemon=True).start()

    def process_text_command(self, command):
        """Processes typed text identically to spoken text."""
        self.update_status("PROCESSING DATA...", "cyan")
        try:
            # We must save the user's manual text to history so Deep Sleep remembers it!
            master.active_chat_history.append(f"User: {command}")
            
            ai_decision = master.ask_local_ai(command)
            result_message = master.execute_command(ai_decision)
            
            self.update_status("SPEAKING...", "yellow")
            master.speak(result_message)
        except Exception as e:
            print(f"[!] Error processing manual command: {e}")
        finally:
            self.update_status("GHOST LOOP (SLEEPING)", "gray")

    def run_jarvis_backend(self):
        """This runs the exact logic from your master.py, but connected to the UI."""
        print("=== J.A.R.V.I.S. BOOT SEQUENCE INITIATED ===")
        
        # --- START BACKGROUND SERVICES (Telegram Bridge) ---
        master.start_background_services()
        
        time.sleep(1)
        master.speak("Command Center Interface Online. All subsystems operational.")
        
        while True:
            self.update_status("GHOST LOOP (Awaiting Wake Word)", "gray")
            
            # 1. Wait for wake word
            if master.wait_for_wake_word():
                self.update_status("AWAKE (Listening...)", "green")
                master.speak("I am here, sir.")
                
                is_active_session = True
                
                while is_active_session:
                    self.update_status("LISTENING...", "green")
                    command = master.listen_for_command()
                    
                    if not command:
                        print("\n[*] Conversation paused. Archiving data and returning to sleep.")
                        self.update_status("SYNTHESIZING MEMORY...", "orange")
                        master.speak("Archiving session data. I will be on standby.")
                        master.synthesize_memory()
                        is_active_session = False
                        continue

                    if command in ["stop", "shut down", "sleep", "exit", "terminate", "goodbye", "that's all"]:
                        self.shutdown_system()

                    print(f"[*] Analyzing Command: {command}")
                    self.update_status("PROCESSING DATA...", "cyan")
                    
                    try:
                        ai_decision = master.ask_local_ai(command)
                        result_message = master.execute_command(ai_decision)
                        
                        self.update_status("SPEAKING...", "yellow")
                        master.speak(result_message)
                    except Exception as e:
                        print(f"[!] AI Engine Error: {e}")
                        master.speak("I encountered an error processing that request.")

    def shutdown_system(self):
        """Forces an absolute kill of the UI, Telegram bots, and Microphone threads."""
        self.update_status("SHUTTING DOWN", "red")
        print("\n[!!!] INITIATING CRITICAL SHUTDOWN [!!!]")
        master.speak("Shutting down the central nervous system. Goodbye, sir.")
        self.destroy() # Closes the UI window
        
        # os._exit(0) guarantees ALL background daemon threads are killed instantly.
        os._exit(0)

if __name__ == "__main__":
    app = JarvisUI()
    app.mainloop()