import pyttsx3

# Dictionary of voice lines for all colors including "Unknown"
lines = {
    "red.wav":   "Red object detected. Moving to bin A.",
    "green.wav": "Green object detected. Moving to bin B.",
    "blue.wav":  "Blue object detected. Moving to bin C.",
    "unknown.wav": "Unknown object detected. Please check the item."
}

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)   # Speed of speech
engine.setProperty("volume", 1.0) # Max volume

# Generate and save audio files
for fname, text in lines.items():
    engine.save_to_file(text, fname)
    print("Queued:", fname, "->", text)

engine.runAndWait()
print("✅ All audio files created successfully!")
