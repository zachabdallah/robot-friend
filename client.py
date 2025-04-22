import os
import json
import pyaudio
import requests
import subprocess
from vosk import Model, KaldiRecognizer

RECOGNIZER_RATE = 16000
FRAMES = 4000
CHANNELS = 1
SERVER_URL = "http://172.16.29.23:5050/chat" #hardcoded IP address on my machine
#when running client.py on the pi5, get the macs IP address with the command "ipconfig getifaddr en0" in the mac terminal
#then, replace 127.0.0.1 with the IP address of the mac

# Initialize Vosk
model_path = "/Users/zachabdallah/Downloads/vscode/robot-friend-main/vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print("Vosk model not found")
    exit(1)
model = Model(model_path)
recognizer = KaldiRecognizer(model, RECOGNIZER_RATE)

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RECOGNIZER_RATE, input=True, frames_per_buffer=FRAMES)

def speak(text):
    stream.stop_stream()
    subprocess.run(["espeak-ng", "-v", "en+f2", "-s", "200", "-a", "200", "-p", "50", text])
    stream.start_stream()

def listen_and_respond():
    stream.start_stream()
    print("Listening (press Ctrl+C to stop)")
    speak("I'm listening")
    try:
        while True:
            data = stream.read(FRAMES, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(f"Heard: {text}")
                    print("Sending to server...")

                    try:
                        response = requests.post(SERVER_URL, json={"text": text})
                        if response.status_code == 200:
                            reply = response.json()["response"]
                            print(f"Response: {reply}")
                            speak(reply)
                        else:
                            print(f"Error from server: {response.text}")
                    except Exception as e:
                        print(f"Error contacting server: {e}")
    except KeyboardInterrupt:
        print("Exiting.")
        speak("Goodbye")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    listen_and_respond()
