import os
import subprocess
import json
import pyaudio
import threading
import ollama
import psutil
from vosk import Model, KaldiRecognizer

# ===== Global constants =====
RECOGNIZER_RATE = 16000
FRAMES = 4000
CHANNELS = 1
cpu_alert_threshold = 60
max_chat_history = 10

# ===== Global objects =====
model = None
recognizer = None
pyaudio_instance = None
stream = None
chat_history = [{"role": "system", "content": "hi there"}]
ollama_model = "ziggy:latest"

# ===== Commands =====
shutdown_commands = ["turn off"]
wake_words = ["hey billy", "hey robot", "check"]

# ===== Initialization Functions =====
def init_vosk():
    global model
    model_path = "/Users/zachabdallah/Downloads/vscode/robot-friend-main/vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print("Model not found")
        exit(1)
    model = Model(model_path)

def init_ollama():
    print("Warming up Ollama...")
    try:
        _ = ollama.chat(model=ollama_model, messages=chat_history + [{"role": "user", "content": "hey"}])
    except Exception as e:
        print("Error communicating with Ollama during warmup:", e)
        exit(1)

def init_audio():
    global recognizer, pyaudio_instance, stream
    try:
        recognizer = KaldiRecognizer(model, RECOGNIZER_RATE)
        pyaudio_instance = pyaudio.PyAudio()
        stream = pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=RECOGNIZER_RATE,
            input=True,
            frames_per_buffer=FRAMES
        )
    except Exception as e:
        print("Audio system initialization error:", e)
        exit(1)
# ====== other functions ======
def show_chat_history():
    print("\n=== Chat History ===")
    for message in chat_history:
        role = message["role"]
        content = message["content"]
        print(f"{role.upper()}: {content}")
    print("====================\n")

# ====== Ollama Chat ======
def ask_ollama(input_text):
    try:
        response = ollama.chat(model=ollama_model, messages=chat_history)
        content = response['message']['content']
        chat_history.append({"role": "user", "content": input_text})
        chat_history.append({"role": "assistant", "content": content})
        if len(chat_history) > max_chat_history + 1:
            chat_history[:] = [chat_history[0]] + chat_history[-max_chat_history:]
        return content
    except Exception as e:
        return f"Error communicating with Ollama in ask_ollama(): {e}"

# ====== CPU Monitor ======
def monitor_cpu(threshold=cpu_alert_threshold):
    def check_loop():
        print("[monitor_cpu] CPU monitoring started")  # debug print
        while True:
            try:
                cpu_usage = psutil.cpu_percent(interval=5)
                print(f"[monitor_cpu] CPU usage: {cpu_usage}%") 
                if cpu_usage > threshold:
                    print(f"CPU usage is {cpu_usage}%")
                    subprocess.run(["espeak", "-v", "en", "-s", "150", "-a", "200", "the CPU is getting hot"])
            except Exception as e:
                print("CPU monitoring error:", e)
    thread = threading.Thread(target=check_loop, daemon=True)
    thread.start()

# ====== Text-to-Speech ======
def speak_aloud(text):
    subprocess.run(["espeak-ng", "-v", "en+f2", "-s", "200", "-a", "200", "-p", "50", text])

# ====== Talk Loop ======
def talk(): 
    stream.start_stream()
    print("I'm listening, press Ctrl+C to stop)")
    speak_aloud("I'm listening")
    try:
        while True:
            data = stream.read(FRAMES, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result["text"]
                if text:
                    print(f"Heard: {text}")
                    print("Sending to Ollama...")
                    response = ask_ollama(text)
                    print(f"Ollama Response: {response}")
                    speak_aloud(response)
                    show_chat_history()
    except KeyboardInterrupt:
        print("Goodbye.")
        subprocess.run(["espeak-ng", "-v", "en+f2", "-s", "200", "-a", "200", "-p", "50", "Goodbye"])
        stream.stop_stream()
        stream.close()
        pyaudio_instance.terminate()

# ====== Main ======
if __name__ == "__main__":
    init_vosk()
    init_ollama()
    init_audio()
    monitor_cpu() 
    talk()

