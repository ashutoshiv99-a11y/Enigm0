import time
import threading
import pygetwindow as gw
import pyperclip
from datetime import datetime

class OmniLogger:
    def __init__(self):
        self.is_logging = True
        self.current_window = ""
        self.last_clipboard = ""
        self.context_log = [] # Holds recent background activity

    def _monitor_loop(self):
        """Silently watches the active window and clipboard."""
        while self.is_logging:
            try:
                # 1. Track the Active Window (What is the user looking at?)
                active_window = gw.getActiveWindow()
                if active_window is not None:
                    title = active_window.title
                    if title and title != self.current_window:
                        self.current_window = title
                        timestamp = datetime.now().strftime("%I:%M %p")
                        log_entry = f"[{timestamp}] User switched to application/tab: {self.current_window}"
                        self.context_log.append(log_entry)
                        print(f"\n[Omni-Logger] {log_entry}")

                # 2. Track the Clipboard (What did the user just copy?)
                clipboard_content = pyperclip.paste()
                if clipboard_content and clipboard_content != self.last_clipboard:
                    self.last_clipboard = clipboard_content
                    # Only log short snippets so we don't overload his memory if you copy an entire book
                    snippet = clipboard_content[:150] + "..." if len(clipboard_content) > 150 else clipboard_content
                    timestamp = datetime.now().strftime("%I:%M %p")
                    log_entry = f"[{timestamp}] User copied text to clipboard: '{snippet}'"
                    self.context_log.append(log_entry)
                    print(f"\n[Omni-Logger] {log_entry}")

                # Keep only the last 30 events so his RAM stays lightning fast
                if len(self.context_log) > 30:
                    self.context_log.pop(0)

            except Exception:
                pass # Fail silently so it never crashes the main AI
            
            # Check the system every 1.5 seconds
            time.sleep(1.5)

    def start(self):
        """Launches the logger in a hidden background thread."""
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        thread.start()
        print("[*] Omni-Logger initialized. J.A.R.V.I.S. is now passively observing your digital environment.")

    def get_recent_context(self):
        """Returns the recent context so the Master Brain can read it before answering questions."""
        if not self.context_log:
            return "No recent computer activity detected."
        return "\n".join(self.context_log)