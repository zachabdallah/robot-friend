As of 3/21/25, you only have to run main.py, as it integrates the speech-to-text and text-to-speech functions into one place, along with allowing communication with whatever ollama model we're using

###################################################################

ON RASPBERRY PI OS

Step 1: create and activate venv

home_directory:~ $ python3 -m venv my_vosk

home_directory:~ $ source /home_directory/my_vosk/bin/activate

##

Step 2: install ollama and LLM

(my_vosk) home_directory:/ $ deactivate

home_directory:/ $ curl -fsSL https://ollama.com/install.sh | sh

home_directory:/ $ ollama pull deepseek-r1:1.5b

home_directory:/ $ ollama run deepseek-r1:1.5b

/set verbose

##

Step 3: update and install packages

sudo apt update

sudo apt install portaudio19-dev #required for pyaudio

pip install pyaudio

pip install vosk 

##

Step 4: download and extract vosk model

wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

unzip vosk-model-small-en-us-0.15.zip

mv vosk-model-small-en-us-0.15 vosk-model #rename it




###################################################################

ON MACOS M1 Sequoia 15.3.1

Step 1: Create and activate venv

brew install python@3.11 #3.13 not officially released

python3.11 -m venv robot_env

source robot_env/bin/activate

##

Step 2: install Ollama and LLM

brew install ollama

ollama serve //must start a local ollama process before running script. when i do that, it loads models into memory and make them available for queries, no internet required

brew services start ollama //OPTIONAL, can make it so ollama is always running in the background

ollama pull qwen:0.5b

##

Step 3: update and install packages

brew install portaudio

CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio

brew install espeak

##

Step 4: download and extract vosk model

pip install vosk

brew reinstall libunistring //was being annoying

brew reinstall wget //was also being annoying

wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

###################################################################
