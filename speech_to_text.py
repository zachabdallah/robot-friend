import os
import json#vosk outputs stuff in JSON format
import wave
import pyaudio#lets us handle real-time audio 
from vosk import Model, KaldiRecognizer #allow us to load a model, Kaldi handles audio recognition from microphone

#configure vosk
model_path = "vosk-model"
if not os.path.exists(model_path):
    print("Model not found")
    exit(1)

model = Model(model_path)
rec = KaldiRecognizer(model, 16000) #current sample rate is 16kHz

#configure PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

print("Listening... (Press Ctrl+C to stop)")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False) #read a chunk of 4000 frames from mic
        if rec.AcceptWaveform(data):#basically, only execute this statement if speech is recognized (white noise protection)
            result = json.loads(rec.Result())#convert JSON text outpit to a dictionary
            print(result["text"])

except KeyboardInterrupt:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finished listening.")
