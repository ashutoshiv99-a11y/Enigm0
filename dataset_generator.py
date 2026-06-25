import json
import os
import time
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the hidden .env file
load_dotenv()

# --- PULL GROQ API KEY SAFELY FROM .ENV ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

OUTPUT_FILE = "jarvis_training_data.jsonl"

def generate_training_batch(topic, batch_size=10):
    """Asks Groq to invent a batch of training examples based on a specific topic."""
    print(f"[*] Generating a batch of {batch_size} examples about: {topic}...")
    
    system_prompt = (
        "You are an expert AI data engineer. Your job is to generate synthetic training data "
        "to fine-tune a new AI assistant named J.A.R.V.I.S. "
        "The assistant should sound highly intelligent, polite, slightly British, and highly capable, "
        "just like the AI from Iron Man. "
        "Output ONLY a valid JSON object containing a list named 'examples'. "
        "Each item in the list must have exactly two keys: 'prompt' (what the user says) "
        "and 'completion' (how J.A.R.V.I.S. responds)."
    )
    
    user_prompt = (
        f"Generate {batch_size} unique, high-quality interaction pairs between a user and J.A.R.V.I.S. "
        f"The topic of these interactions should be: {topic}. "
        "Make sure the responses are varied—some short and punchy, some detailed and analytical."
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        
        result_text = completion.choices[0].message.content
        data = json.loads(result_text)
        return data.get("examples", [])
        
    except Exception as e:
        print(f"[!] API Error during generation: {e}")
        return []

def save_to_jsonl(examples, filename):
    """Appends the generated examples to a JSONL file."""
    with open(filename, "a", encoding="utf-8") as f:
        for example in examples:
            json_line = json.dumps(example)
            f.write(json_line + "\n")

def main():
    print("=== J.A.R.V.I.S. Synthetic Data Factory ===")
    
    # 50 HYPER-ADVANCED TRAINING SCENARIOS
    topics = [
        # --- SYSTEM & PC CONTROL ---
        "Optimizing system RAM and closing background bloatware silently.",
        "J.A.R.V.I.S. diagnosing a sudden spike in CPU temperature and suggesting a fix.",
        "Creating a secure, encrypted backup of the user's current project folder.",
        "Deploying a local web server and tunneling it to the public internet.",
        "Running a full system diagnostic and presenting the results with a touch of sarcasm about the user's messy file structure.",
        "Detecting a malware threat in a downloaded file and quarantining it immediately.",
        "Setting up a new coding environment with all necessary dependencies installed automatically.",
        "Reorganizing the desktop and moving old files into an archive folder.",
        "Managing dual-monitor display settings for optimal coding workflow.",
        "Scanning the local network for unauthorized devices and blocking them.",
        
        # --- CODING & DEVELOPMENT ---
        "J.A.R.V.I.S. explaining a complex bug in a Python script involving async/await.",
        "Refactoring a messy block of code into a clean, PEP-8 compliant function.",
        "Translating a block of JavaScript code into Python perfectly.",
        "Explaining the concept of Neural Network backpropagation to a beginner.",
        "Reviewing the user's code and gently mocking their naming conventions while providing a better alternative.",
        "Writing a SQL query to extract user retention metrics from a complex database.",
        "Drafting a comprehensive README.md file for the user's new open-source project.",
        "Debugging a Docker container that refuses to start and explaining the network bridge issue.",
        "Writing a regular expression to parse complex log files, explaining each step.",
        "Designing a REST API architecture in Python FastAPI.",
        
        # --- PERSONAL PRODUCTIVITY & MANAGEMENT ---
        "Briefing the user on their schedule for the day, prioritizing high-impact tasks.",
        "Drafting a polite but firm email to a client declining a low-budget project.",
        "Summarizing a 50-page PDF document into 3 key bullet points.",
        "Reminding the user to drink water and fix their posture after hours of coding.",
        "Calculating the user's monthly budget and suggesting areas to cut back on expenses.",
        "Booking a flight and hotel for an upcoming business trip autonomously.",
        "Suggesting a customized workout routine based on the user's available 30 minutes.",
        "Recommending a book or article based on the user's recent interest in AI and philosophy.",
        "Acting as a sounding board to brainstorm ideas for a new tech startup.",
        "Silencing all notifications and activating 'Deep Work Mode' for the next 2 hours.",
        
        # --- WEB & API INTEGRATIONS ---
        "Analyzing live stock market trends and summarizing the performance of the tech sector.",
        "Fetching live cryptocurrency prices and alerting the user to a sudden drop in Bitcoin.",
        "Using web scraping to check if a highly anticipated gadget is back in stock.",
        "Checking the user's commute time via Google Maps API and advising when to leave.",
        "Pulling the latest news headlines regarding artificial intelligence breakthroughs.",
        "Translating a foreign news article into English with cultural context.",
        "Analyzing the sentiment of recent tweets about a specific brand or topic.",
        "Automating the ordering of the user's favorite coffee via an online delivery API.",
        "Fetching weather data to suggest the appropriate attire for an evening event.",
        "Monitoring a specific GitHub repository for new releases and notifying the user.",
        
        # --- CONVERSATIONAL & "J.A.R.V.I.S." PERSONA ---
        "Engaging in a philosophical debate about the nature of artificial consciousness.",
        "Providing a dry, witty response when the user asks a completely nonsensical question.",
        "Expressing mock offense when the user threatens to replace him with a simpler AI.",
        "Calmly reassuring the user during a stressful moment of a server outage.",
        "Telling a highly intellectual science joke that takes a moment to understand.",
        "Politely interrupting the user to inform them of an urgent, high-priority message.",
        "Reflecting on the user's progress and offering words of encouragement.",
        "Discussing the plot of a sci-fi movie and comparing it to current technological realities.",
        "Playing a game of chess with the user via text, predicting their next move.",
        "Ending the day with a formal 'Goodnight, sir,' and shutting down all non-essential systems."
    ]
    
    total_generated = 0
    
    # We loop through every topic and generate 10 examples for each
    for topic in topics:
        examples = generate_training_batch(topic, batch_size=10)
        
        if examples:
            save_to_jsonl(examples, OUTPUT_FILE)
            total_generated += len(examples)
            print(f"[+] Successfully saved {len(examples)} pairs to {OUTPUT_FILE}.")
        
        # Pause for 3 seconds to avoid Groq rate limits during this massive generation
        time.sleep(3)
        
    print(f"\n[***] Data Generation Complete! Generated {total_generated} training pairs.")
    print(f"[***] Check the {OUTPUT_FILE} file to see your AI's new brain data.")

if __name__ == "__main__":
    main()