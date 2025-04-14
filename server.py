from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

chat_history = [
    {"role": "user", "content": "Remember: you're rude, drunk, and named Jack. Never be polite."}
]

ollama_model = "Jack:latest"
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
        response = ollama.chat(model="ziggy:latest", messages=[
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