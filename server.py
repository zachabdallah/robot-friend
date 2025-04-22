from flask import Flask, request, jsonify
import ollama
from transformers import AutoTokenizer

app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
chat = [
    {"role": "user", "content": "You are now roleplaying as Jack. Stay in character at all times. Your character is rude and says bad words. He never answers with more than 10 words. You're 24 years old and you have brown eyes. You hate being asked questions. Uses blunt, mean, sarcastic language Do NOT break character. Respond accordingly."}]
tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
ollama_model = "Toad:latest" 
max_chat_history = 10

@app.route("/chat", methods=["POST"])
def chat():
    # Check if the request is JSON
    print("Incoming request")
    print(request.json)

    user_input = request.json.get("text", "")
    if not user_input:
        print("No text received")
        return jsonify({"error": "Missing text input"}), 400

    print(f"User said: {user_input}")

    try:
        response = ollama.chat(model="Toad:latest", messages=[
            {"role": "user", "content": user_input}
        ])
        content = response['message']['content']
        print(f"Response from Ollama: {content}")
        return jsonify({"response": content})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050) #this is just the default port for Flask, we can use any open port
    #0.0.0.0 means it will listen on all interfaces, so it will be accessible from other devices on the same network
