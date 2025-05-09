from transformers import pipeline
import google.generativeai as genai
import os
import warnings
from transformers import AutoTokenizer  # Import the tokenizer

warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages

# Load the summarization pipeline
summarizer = pipeline("summarization")
# Get the tokenizer associated with the summarization model
tokenizer = AutoTokenizer.from_pretrained(summarizer.model.name_or_path)
max_token_length = tokenizer.model_max_length  # Get the model's max input length

# Configure the generative model
genai.configure(api_key="AIzaSyAT8_moONkWrgdJ_G1jUBndNpes0t6dtJE") # Replace with your actual API key


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

def is_sha_related(user_input):
    """
    Checks if the user input is likely related to the Social Health Authority (SHA).
    This is a simple heuristic and can be improved with more sophisticated NLP.
    """
    keywords = ["sha", "social health authority", "shif", "health insurance kenya", "primary healthcare fund", "emergency fund"]
    user_input_lower = user_input.lower()
    for keyword in keywords:
        if keyword in user_input_lower:
            return True
    return False

def is_greeting(user_input):
    """
    Checks if the user input is a simple greeting.
    """
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    user_input_lower = user_input.lower()
    for greeting in greetings:
        if greeting in user_input_lower:
            return True
    return False

def get_sha_info(user_input):
    """
    Sends the user input to the Gemini model with a specific prompt
    to get information about the SHA.
    """
    prompt = f"Provide information about the Social Health Authority (SHA) in Kenya based on the following query: '{user_input}'. Be informative and helpful."
    response = convo.send_message(prompt)
    return response.text

def greet():
    """
    Returns a simple greeting.
    """
    return "Hello! How can I help you with information about the Social Health Authority (SHA) today?"

def handle_non_sha_related():
    """
    Returns a polite response for non-SHA related queries.
    """
    return "I can only provide information related to the Social Health Authority (SHA) in Kenya. Do you have any questions about that?"

def answer(user_input):
    if is_sha_related(user_input):
        bot_response = get_sha_info(user_input)

        # Truncate the response to the model's maximum sequence length
        truncated_response = tokenizer.decode(
            tokenizer.encode(bot_response, truncation=True, max_length=tokenizer.model_max_length),
            skip_special_tokens=True
        )

        # Dynamically adjust max_length and min_length
        input_length = len(truncated_response.split())
        max_length = min(150, input_length + 20)  # Ensure max_length is slightly longer than input
        min_length = max(10, min(input_length // 2, max_length - 1))  # Ensure min_length < max_length

        summary = summarizer(truncated_response, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    elif is_greeting(user_input):
        print("Greeting detected")
        bot_response = greet()
        return bot_response
    else:
        bot_response = handle_non_sha_related()

        # Truncate the response to the model's maximum sequence length
        truncated_response = tokenizer.decode(
            tokenizer.encode(bot_response, truncation=True, max_length=tokenizer.model_max_length),
            skip_special_tokens=True
        )

        # Dynamically adjust max_length and min_length
        input_length = len(truncated_response.split())
        max_length = min(150, input_length + 20)
        min_length = max(10, min(input_length // 2, max_length - 1))

        summary = summarizer(truncated_response, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

# Example usage (you'll likely integrate this with your Flask backend)
if __name__ == "__main__":
    while True:
        user_query = input("You: ") + '(NB:answers based on KENYA Social Health Authority question  )'
        if user_query.lower() == 'exit':
            break
        bot_answer = answer(user_query)
        print(f"SHA Info Bot: {bot_answer}")