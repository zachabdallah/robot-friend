
Step 1: create and activate venv
home_directory:~ $ python3 -m venv my_vosk
home_directory:~ $ source /home/zcabdallah/my_vosk/bin/activate

Step 2: install and run ollama
(my_vosk) home_directory:/ $ deactivate
home_directory:/ $ curl -fsSL https://ollama.com/install.sh | sh
home_directory:/ $ ollama pull deepseek-r1:1.5b
home_directory:/ $ ollama run deepseek-r1:1.5b
/set verbose

Step 3: update and install packages
sudo apt update
sudo apt install portaudio19-dev #required for pyaudio
pip install pyaudio
pip install vosk 

Step 4:
download and extract vosk model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 vosk-model #rename it
