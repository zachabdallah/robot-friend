import os
import subprocess
import json
import pyaudio
import ollama
from vosk import Model, KaldiRecognizer

#initialize vosk
model_path = "/Users/zachabdallah/Downloads/vscode/robot-friend-main/vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print("Model not found")
    exit(1)
model = Model(model_path)
#initialize ollama
ollama_model = "deepseek-r1:1.5b"
print("Warming up Ollama...")
_ = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": "Hey"}])
#initalize pyaudio
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
#prompt the LLM
def ask_ollama(input_text):
    try:
        response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": input_text}])
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

def run_stt_tts(): 
    stream.start_stream()
    print("I'm listening, press Ctrl+C to stop)")
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result["text"]
                if text:  #only speak if text is recognized
                    print(f"Heard: {text}")
                    print("Sending to ollama.....")
                    response = ask_ollama(text)
                    print(f"Ollama Response: {response}")
                    subprocess.run(["espeak", "-v", "en", "-s", "150", "-a", "200", response])#use espeak to read process aloud
    except KeyboardInterrupt:
        print("Wow, ok... later I guess....")
        stream.stop_stream()
        stream.close()
        p.terminate()

run_stt_tts()