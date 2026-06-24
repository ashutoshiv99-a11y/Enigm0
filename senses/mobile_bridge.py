import telebot
import threading

class TelegramBridge:
    def __init__(self, bot_token, brain_function, execute_function):
        self.bot = telebot.TeleBot(bot_token)
        self.brain_function = brain_function
        self.execute_function = execute_function
        
        # Security: We will lock this down to ONLY your phone later
        self.authorized_chat_id = None 

        print("[*] Mobile Bridge Initialized. Connecting to Telegram servers...")

        # Define how the bot reacts when it gets a message from your phone
        @self.bot.message_handler(func=lambda message: True)
        def handle_remote_command(message):
            chat_id = message.chat.id
            user_text = message.text
            
            # Security check: lock the bot to the first person who messages it!
            if self.authorized_chat_id is None:
                self.authorized_chat_id = chat_id
                self.bot.reply_to(message, "J.A.R.V.I.S. Mobile Bridge connected securely. Awaiting your commands, sir.")
                print(f"[+] Security Lock: Mobile Bridge locked to Chat ID {chat_id}")
            
            if chat_id != self.authorized_chat_id:
                print(f"[!] Unauthorized access attempt from Chat ID {chat_id}")
                return

            print(f"\n[📱 Phone]: {user_text}")
            
            # Send a "typing..." action to your phone so you know he is thinking
            self.bot.send_chat_action(chat_id, 'typing')
            
            try:
                # 1. Send the text to the Groq Brain
                ai_decision = self.brain_function(user_text)
                
                # 2. Execute the action on the PC
                result_message = self.execute_function(ai_decision)
                
                # 3. Send the result back to your phone!
                self.bot.reply_to(message, result_message)
                print(f"[🤖 J.A.R.V.I.S.]: Sent result to phone.")
                
            except Exception as e:
                self.bot.reply_to(message, f"System Error during remote execution: {e}")

    def start_listening(self):
        """Starts the Telegram polling loop in a background thread."""
        # non_stop=True ensures it doesn't crash if your internet drops for a second
        self.bot.polling(non_stop=True)

    def run_in_background(self):
        """Spawns a separate thread so it doesn't block the PC microphone."""
        thread = threading.Thread(target=self.start_listening)
        thread.daemon = True
        thread.start()
        print("[*] Mobile Bridge is now actively listening in the background.")

# Note: We don't run a test block here because it needs your master functions!