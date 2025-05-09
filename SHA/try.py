import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Official SHA website URL
SHA_WEBSITE_URL = "https://sha.go.ke/"

def preprocess_text(text):
    """Lowercase, remove punctuation, and stop words."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    return tokens

def fetch_and_extract_info(url):
    """Fetches content from a URL and extracts relevant text using CSS selectors."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # **ADJUST THESE CSS SELECTORS BASED ON THE ACTUAL WEBSITE STRUCTURE**
        css_selectors = [
            'main',             # Often contains the primary content
            '.entry-content',   # Common class for post content
            '.post-content',    # Another common class
            '.page-content',    # For page content
            'article',          # Semantic tag for main article
            'div.content',      # Example: div with class 'content'
            'div#main-content', # Example: div with ID 'main-content'
            'p'                 # As a fallback, get all paragraphs
        ]

        extracted_text = []
        for selector in css_selectors:
            elements = soup.select(selector)
            for element in elements:
                extracted_text.append(element.get_text(separator=' ', strip=True))

        # Join the extracted text with spaces
        return ' '.join(extracted_text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing content: {e}")
        return None

def retrieve_information_from_web(query):
    """Fetches information from the web and then performs keyword-based retrieval."""
    website_content = fetch_and_extract_info(SHA_WEBSITE_URL)

    if website_content:
        query_tokens = preprocess_text(query)
        content_tokens = preprocess_text(website_content)
        common_keywords = set(query_tokens) & set(content_tokens)

        if common_keywords:
            relevant_snippet = ""
            sentences = nltk.sent_tokenize(website_content)
            for sentence in sentences:
                if any(keyword in preprocess_text(sentence) for keyword in query_tokens):
                    relevant_snippet += sentence + " "
            return f"Based on information from the SHA website: {relevant_snippet[:500]}..."
        else:
            return "I found information on the website, but it doesn't seem directly related to your keywords."
    else:
        return "I was unable to retrieve information from the SHA website."

if __name__ == "__main__":
    while True:
        user_query = input("You: ")
        if user_query.lower() == 'exit':
            break
        response = retrieve_information_from_web(user_query)
        print(f"SHA Info Bot: {response}")