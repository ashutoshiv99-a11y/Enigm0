# Enigm0/skills/routines.py
import webbrowser
import subprocess
import time
import os

def activate_trading_protocol():
    """Sets up the environment for technical analysis and strategy building."""
    print("[*] Initiating Trading Protocol...")
    
    # Open exchanges and charting
    webbrowser.open("https://www.delta.exchange")
    time.sleep(1)
    webbrowser.open("https://www.tradingview.com")
    
    # Open the local directory where you keep your code (Update this path to your actual folder)
    # subprocess.Popen(r'explorer /select,"C:\Users\ashut\Documents\LRX-PRO_Script"')
    
    return "Trading environment initialized. Delta Exchange and TradingView are online. Ready to analyze the volume profile."

def activate_gaming_protocol():
    """Optimizes the system for gaming."""
    print("[*] Initiating Gaming Protocol...")
    
    # In a fully fleshed-out system, you would add code here to kill background processes like Chrome to free up RAM
    # os.system("taskkill /f /im chrome.exe") 
    
    # Launch your game (Update the path to your actual game executable or emulator)
    # subprocess.Popen([r"C:\Riot Games\Riot Client\RiotClientServices.exe"]) 
    
    return "System optimized. Launching gaming environment."

def activate_editing_protocol():
    """Sets up the video editing workflow."""
    print("[*] Initiating Editing Protocol...")
    
    # Open your video editing software and AI generation web tools
    # subprocess.Popen([r"C:\Program Files\YourEditor\editor.exe"])
    webbrowser.open("https://runwayml.com") # Example AI video tool
    
    return "Editing workflow deployed. AI tools are standing by."

def route_protocol(target):
    """Routes the AI's target to the correct complex function."""
    if target == "trading":
        return activate_trading_protocol()
    elif target == "gaming":
        return activate_gaming_protocol()
    elif target == "editing":
        return activate_editing_protocol()
    else:
        return f"Protocol '{target}' does not exist in my system."