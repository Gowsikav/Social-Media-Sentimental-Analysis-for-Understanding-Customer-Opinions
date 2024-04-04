import requests
from bs4 import BeautifulSoup

# Function to scrape reviews from a single page
def scrape_reviews(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    review_divs = soup.find_all('div', {'class': 'Jwxk6d'})
    reviews = []
    for review_div in review_divs:
        review_text = review_div.find('span', {'jsname': 'h3YV2d'}).text.strip()
        reviews.append(review_text)
    return reviews

# Function to scrape reviews from multiple pages
def scrape_google_play_reviews(app_id, num_pages):
    base_url = f"https://play.google.com/store/getreviews?id={app_id}&hl=en&reviewSortOrder=2&reviewType=1&pageNumber="
    all_reviews = []
    for page in range(1, num_pages + 1):
        url = base_url + str(page)
        reviews = scrape_reviews(url)
        if not reviews:
            break
        all_reviews.extend(reviews)
    return all_reviews

# App ID and number of pages to scrape
app_id = 'com.whatsapp'
num_pages = 3

# Scrape reviews from Google Play Store
all_reviews = scrape_google_play_reviews(app_id, num_pages)

# Print the scraped reviews
for i, review in enumerate(all_reviews):
    print(f"Review {i+1}: {review}")
