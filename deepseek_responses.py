#!/usr/bin/env python3
import os
import subprocess
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import ollama  # For local AI inference
import time

# Configuration
model_path = "/home/vinso/vosk-model"
if not os.path.exists(model_path):
    print("Model not found")
    exit(1)

# Initialize Vosk model and PyAudio
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,  # Default input (Card 3, mic)
    frames_per_buffer=4000
)
stream.start_stream()

# Silence detection settings
SILENCE_THRESHOLD = 2.0  # Wait 2 seconds of silence before finalizing input
last_speech_time = time.time()
accumulated_text = ""

# System instruction for concise responses
SYSTEM_PROMPT = "Respond concisely in one short sentence."

print("Listening and responding with DeepSeek-R1-Distill-Qwen-7B... (Press Ctrl+C to stop)")
try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        
        # Process audio chunk
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result["text"]
            if text:
                accumulated_text += " " + text
                last_speech_time = time.time()
        else:
            partial_result = json.loads(rec.PartialResult())
            partial_text = partial_result.get("partial", "")
            if partial_text:
                last_speech_time = time.time()

        # Check if silence has lasted long enough
        current_time = time.time()
        if accumulated_text and (current_time - last_speech_time) >= SILENCE_THRESHOLD:
            final_text = accumulated_text.strip()
            if len(final_text) > 2:  # Ignore short inputs
                print(f"Heard: {final_text}")
                # Combine system prompt with user input for concise response
                full_prompt = f"{SYSTEM_PROMPT} {final_text}"
                # Send to DeepSeek-R1-Distill-Qwen-7B
                ai_response = ollama.generate(model='deepseek-r1:7b-qwen-distill-q4_K_M', prompt=full_prompt, options={"num_ctx": 1024})['response']
                print(f"AI Response: {ai_response}")
                # Send AI response to TTS
                subprocess.run(["espeak", "-v", "en", "-s", "150", "-a", "200", ai_response])
            # Reset for next input
            accumulated_text = ""
            rec.Reset()

except KeyboardInterrupt:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Program stopped.")
