
import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import emoji
import time
import matplotlib.pyplot as plt 


nltk.download('vader_lexicon')


def preprocess_text(text):
    return emoji.demojize(text)


def sentiment_vader(text):
    sid = SentimentIntensityAnalyzer()
    polarity_scores = sid.polarity_scores(text)
    if polarity_scores['compound'] >= 0.05:
        return "positive"
    elif polarity_scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"


def generate_single_suggestion(sentiment):
    suggestions = {
        'positive': 'Highly recommended! This product seems to have great feedback.',
        'negative': 'Some customers had issues with this product. Consider reading the negative reviews before making a decision.',
        'neutral': 'Opinions on this product vary. You may want to explore further to make an informed choice.'
    }
    return suggestions.get(sentiment, 'No suggestion')



def scrape_reviews(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    reviews_container = soup.find('div', {'class': '_1YokD2 _3Mn1Gg col-9-12'})
    if reviews_container is None:
        return []
    review_divs = reviews_container.find_all('div', {'class': 't-ZTKy'})
    if not review_divs:
        return []
    reviews = []
    for review_div in review_divs:
        review_text = review_div.get_text().strip()
        preprocessed_text = preprocess_text(review_text)
        reviews.append(preprocessed_text)
    return reviews


def scrape_flipkart_reviews(product_url, num_pages):
    all_reviews = []
    for page in range(1, num_pages + 1):
        url = f"{product_url}&page={page}"
        reviews = scrape_reviews(url)
        if not reviews:
            break
        all_reviews.extend(reviews) 
        time.sleep(1)  
    return all_reviews


product_url = 'https://www.flipkart.com/boult-crown-1-95-screen-bt-calling-working-crown-zinc-alloy-frame-900-nits-spo2-smartwatch/product-reviews/itme4d41a7681606?pid=SMWGPHT4WMGGHGGC&lid=LSTSMWGPHT4WMGGHGGC7NH1PB&marketplace=FLIPKART'
num_pages = 10


all_reviews = scrape_flipkart_reviews(product_url, num_pages)

if not all_reviews:
    print("Error: No reviews found.")
    exit()


data = pd.DataFrame({'review': all_reviews})


data['polarity'] = data['review'].apply(lambda review: sentiment_vader(review))


overall_sentiment = data['polarity'].value_counts().idxmax()


suggestion = generate_single_suggestion(overall_sentiment)


plt.figure(figsize=(8, 6))
data['polarity'].value_counts().plot(kind='bar', color=['green', 'red', 'blue'], alpha=0.7)
plt.title('Sentiment Distribution of Reviews')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.ylim(0, len(data))
plt.text(0, len(data) * 0.9, f'Suggestion: {suggestion}', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
plt.tight_layout()
plt.show()