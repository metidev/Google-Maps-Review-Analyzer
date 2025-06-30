حتماً Mehdi جان! اینم نسخه‌ی کامل و تمیز فایل `README.md` به زبان انگلیسی برای ریپازیتوری GitHub پروژه‌ت:

# 🗺️ Google Maps Review Analyzer with AI

A Python script that automatically collects user reviews from a specific Google Maps location and analyzes them using AI. It extracts names of mentioned individuals and performs sentiment analysis to determine how positively or negatively each person is discussed.

---

## 🚀 Features

- ✅ Automatically extract reviews from any Google Maps location
- 🧠 Named Entity Recognition (NER) to detect people mentioned in reviews
- 🤖 Sentiment analysis using state-of-the-art BERT model
- 📊 Console-based analysis report with progress bar
- 🧼 Clean output without cluttered system logs

---

## 🛠️ Requirements

- Python 3.8+
- Google Chrome installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your browser version

---

## 📦 Installation

Install the necessary packages using pip:

```bash
pip install selenium transformers tqdm
````


---


## ▶️ How to Run

1. Replace the `location_url` in the script with your desired Google Maps place URL:

   ```python
   location_url = "https://www.google.com/maps/place/Your+Location"
   ```

2. Run the script:

   ```bash
   python script.py
   ```

3. Output:
   You'll see something like:

   ```
   👤 Ali: Mentioned 5 times - 80.0% Positive
   👤 Sarah: Mentioned 3 times - 100.0% Positive
   ```

---

## 📋 How It Works

* Launches Chrome using Selenium and opens the provided Google Maps URL.
* Clicks the “Reviews” tab and scrolls until all reviews are loaded.
* Extracts all visible English-translated reviews (Google auto-translates them).
* Detects named entities (e.g., people) and analyzes the sentiment of each review.
* Aggregates sentiment scores for each person and prints a summary.

---

## ⚙️ Optional Settings

* To run the script **headless** (without opening a browser window), uncomment this line:

  ```python
  options.add_argument('--headless')
  ```

---

## 💡 Notes

* The script uses English translations from Google Maps (even if the original reviews were in another language).
* For large places with many reviews, make sure your internet connection is stable as the script scrolls to load all reviews.

---

## 📄 License

MIT © \Mehdi Anvari

---


