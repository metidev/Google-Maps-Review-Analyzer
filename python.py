import os
import re
import time
import warnings
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transformers import pipeline
from tqdm.auto import tqdm

# --- Suppress all unnecessary logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

import logging
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)
logging.getLogger("transformers.configuration_utils").setLevel(logging.ERROR)

# --- Browser setup
options = Options()
options.add_argument('--log-level=3')
# options.add_argument('--headless')  # Enable this if you don't want the browser to open

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# --- Target Google Maps URL
location_url = "https://www.google.com/maps/place/Shamsipour+Technical+and+Vocational+College/@35.7039419,51.4501719,17z/data=!3m1!4b1!4m6!3m5!1s0x3f8e0248182b1fdf:0x41b23deefbb9c666!8m2!3d35.7039376!4d51.4527468!16s%2Fm%2F0j3fgbb!5m1!1e2"
print("🌐 Loading Google Maps page ...")
driver.get(location_url)
time.sleep(4)

# --- Click the Reviews button
try:
    print("🔍 Attempting to open the reviews section ...")
    reviews_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.hh2c6[aria-label*='Reviews']")))
    reviews_button.click()
    time.sleep(3)
    print("✅ Reviews section opened.")
except:
    print("❌ Reviews button not found or not clickable.")

# --- Scroll to load all reviews
print("📥 Collecting reviews...")
try:
    scrollable = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m6QErb")))
    prev_count = 0
    retries = 0
    print("⏳ Scrolling through the reviews...")

    with tqdm(total=300, desc="Scrolling", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} reviews') as progress:
        while True:
            reviews_elements = driver.find_elements(By.CLASS_NAME, "wiI7pd")
            current_count = len(reviews_elements)
            progress.n = current_count
            progress.refresh()

            if current_count == prev_count:
                retries += 1
                if retries >= 5:
                    break
            else:
                retries = 0
                prev_count = current_count

            if reviews_elements:
                driver.execute_script("arguments[0].scrollIntoView(true);", reviews_elements[-1])
            time.sleep(2)

except:
    print("❌ Failed to scroll the review section.")

# --- Extract translated English reviews
print("🧾 Extracting review texts...")
all_spans = driver.find_elements(By.CSS_SELECTOR, ".m6QErb span")
reviews = [el.text for el in all_spans if len(el.text.strip()) > 30 and not re.search(r'[\u0600-\u06FF]', el.text)]
driver.quit()
print(f"✅ Total reviews collected: {len(reviews)}\n")

# --- Sentiment Analysis and Named Entity Recognition
print("🤖 Running sentiment and entity analysis...")
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)
person_sentiment = defaultdict(list)

for review in tqdm(reviews, desc="Analyzing", unit="review", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} processed'):
    sentiment = sentiment_model(review)[0]
    entities = ner_model(review)
    for entity in entities:
        if entity["entity_group"] == "PER":
            name = entity["word"]
            person_sentiment[name].append((sentiment["label"], sentiment["score"]))

# --- Final Results
print("\n📊 Final Analysis: Mentioned people and positivity rate\n")
for person, entries in person_sentiment.items():
    count = len(entries)
    positives = [s for s, _ in entries if s == "POSITIVE"]
    percent_pos = round(len(positives) / count * 100, 1)
    if count >= 2:
        print(f"👤 {person}: Mentioned {count} times - {percent_pos}% positive reviews")

print("\n✅ Analysis completed successfully.")
