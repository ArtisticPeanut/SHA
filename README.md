This project is a web-based virtual assistant designed to provide information and support related to mental health and Kenya's Social Health Authority (SHA). It features a chat interface powered by advanced language models and summarization pipelines, and includes user authentication (sign up/sign in).

## Features

- **24/7 Chat Support:** Interactive chatbot for SHA and mental health queries.
- **Summarization:** Uses NLP to summarize long responses for clarity.
- **Speech-to-Text:** Voice input supported in modern browsers.
- **User Authentication:** Sign up and sign in functionality.
- **Responsive UI:** Clean, modern interface with mobile support.

## Project Structure

```
SHA/
│
├── app.py                # Flask app entry point
├── combination.py        # Main chat logic (Gemini + summarization)
├── test.py               # Alternative chat logic/testing
├── testGEnai.py          # Direct Gemini API test
├── try.py                # Web scraping and info retrieval
├── templates/
│   ├── chat.html         # Main chat interface
│   ├── index.html        # Landing page
│   ├── signin.html       # Sign in page
│   └── signup.html       # Sign up page
├── static/
│   ├── styles.css        # Main stylesheet
│   ├── sha.jpeg          # SHA logo
│   ├── sha_back.jpeg     # Chat background
│   ├── relaxing.png      # Additional images
│   └── winking.mp4       # Video asset
├── instance/
│   └── users.db          # User database (SQLite)
├── __pycache__/          # Python cache files
├── txt                   # Stores Gemini API key
summarize.py              # Standalone summarization script
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <repository-url>
cd SHA
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

**Required packages include:**
- Flask
- transformers
- google-generativeai
- nltk
- beautifulsoup4
- requests

### 3. Set Up API Keys

- Place your Google Gemini API key in txt (or set as an environment variable).
- For security, do **not** commit your API key to version control.

### 4. Run the Application

```sh
cd SHA
python app.py
```

- The app will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Usage

- Visit the home page and sign up or sign in.
- Use the chat interface to ask questions about SHA or mental health.
- Use the microphone button for voice input (if supported by your browser).

## Security Notes

- **Do not expose your API keys.** Move them to environment variables or a secure config file for production.
- The included database is for demonstration only; use proper authentication and encryption for real deployments.

## License

This project is for educational purposes. See `LICENSE` for details (add a license file if needed).

---

**Maintainer:** Billy Paul  
**Contact:** paulsanova@gmail.com
