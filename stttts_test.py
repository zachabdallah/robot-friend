#!/usr/bin/env python3
import os
import subprocess
import json
import wave
import pyaudio
from vosk import Model, KaldiRecognizer

# Function for STT (from stt_test.py)
def run_stt():
    model_path = "/home/vinso/vosk-model"
    if not os.path.exists(model_path):
        print("Model not found")
        exit(1)

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    stream.start_stream()

    print("STT Mode: Listening... (Press Ctrl+C to stop)")
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print(result["text"])
    except KeyboardInterrupt:
        print("\nStopping STT...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("STT Mode finished.")

# Function for TTS (from tts_test.py)
def run_tts():
    print("TTS Mode: Type something for me to say (type 'exit' to stop)")
    while True:
        user_input = input("Type: ").strip()
        if user_input.lower() == "exit":
            break
        print(f"TTS Mode will say: {user_input}")
        subprocess.run(["espeak", "-v", "en", "-s", "150", "-a", "200", user_input])
    print("TTS Mode stopped.")

# Main program start
print("Welcome to STT-TTS Test!")
print("Type 'a' for STT (speech-to-text) or 'b' for TTS (text-to-speech):")
choice = input("Your choice (a/b): ").strip().lower()

if choice == 'a':
    run_stt()
elif choice == 'b':
    run_tts()
else:
    print("Invalid choice. Please type 'a' or 'b'. Exiting.")
