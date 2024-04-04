from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import requests
import emoji

app = Flask(__name__)

# Download the VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

# Function to preprocess text (convert emojis to text representations)
def preprocess_text(text):
    return emoji.demojize(text)

# Function to perform sentiment analysis using VADER
def sentiment_vader(text):
    sid = SentimentIntensityAnalyzer()
    polarity_scores = sid.polarity_scores(text)
    if polarity_scores['compound'] >= 0.05:
        return "positive"
    elif polarity_scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

# Function to scrape reviews from Flipkart
# Function to scrape reviews from multiple pages for Flipkart
def scrape_flipkart_reviews(url, max_pages=10):
    all_reviews = []
    page = 1
    while page <= max_pages:
        response = requests.get(url.format(page))
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        review_divs = soup.find_all('div', class_='_27M-vq')
        if not review_divs:
            break
        reviews = [preprocess_text(review_div.get_text().strip()) for review_div in review_divs]
        all_reviews.extend(reviews)
        page += 1
    return all_reviews


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    product_url = data['productUrl']

    # Validate URL
    if 'flipkart.com' not in product_url:
        return jsonify({"error": "Invalid URL for Flipkart"})

    # Scrape reviews from the specified URL
    try:
        reviews = scrape_flipkart_reviews(product_url)
    except Exception as e:
        return jsonify({"error": str(e)})

    # Perform sentiment analysis on the reviews
    sentiment_data = {"positive": 0, "negative": 0, "neutral": 0}
    for review in reviews:
        sentiment = sentiment_vader(review)
        sentiment_data[sentiment] += 1

    return jsonify(sentiment_data)

if __name__ == '__main__':
    app.run(debug=True)
