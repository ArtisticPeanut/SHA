from flask import Flask, render_template, request, jsonify
import os
import combination  # Import the combination module for handling chat logic

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    """
    Render the main page with information about SHA and the chat interface.
    """
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages sent by the user and return the bot's response.
    """
    user_message = request.json.get("message")  # Get the user's message from the request
    print(f"User message: {user_message}")  # For debugging

    # Get the bot's response using the combination module
    bot_response = combination.answer(user_message)
    return jsonify({'bot_response': bot_response})  # Return the bot's response as JSON

if __name__ == '__main__':
    app.run(debug=True)