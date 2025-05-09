import google.generativeai as genai

# Configure the generative model
# It's best practice to load your API key from an environment variable or a secure configuration file.
# Hardcoding it directly in the script is not recommended for security reasons.
# For example:
# import os
# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
genai.configure(api_key="AIzaSyAT8_moONkWrgdJ_G1jUBndNpes0t6dtJE")  # Replace with your actual API key

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,

}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

# Initialize the generative model
model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                             generation_config=generation_config,
                             safety_settings=safety_settings)

# Start a conversation
convo = model.start_chat(history=[])

def respond(user_input):
    convo.send_message(user_input)
    print(convo.last.text)

    return convo.last.text  # Directly return the text

respond("my gal friend left me")