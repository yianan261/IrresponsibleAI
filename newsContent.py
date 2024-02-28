import requests
from newspaper import Article
import json
import openai
from dotenv import load_dotenv
import os
from collections import defaultdict
import logging


load_dotenv()
KEY = os.getenv("KEY")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting the script...")
logging.info("Loading JSON data from file...")

# function that uses Newspaper3k library to scrape article
def scrape_article(url):
    article = None
    try:
        article = Article(url)
        article.download()
        article.parse()
    except:
        logging.info(f"the URL {url} cannot be accessed")
        return ""
    return article.text


def process_content(text, api_key):
    api_url = "https://api.openai.com/v1/chat/completions"
    prompt = f"""
    Please extract the following informaiton from the news article:
    - Country:
    - State:
    - City:
    - Continent:
    - Company city:
    - Affected population (e.g. Military, LGBTQ, Student, Facebook users, Black, Online Female population, EU travelers, Twitter users):
    - Number of people actually affected:
    - Number of people potentially affected:
    - Class of irresponsible AI use (e.g. Discrimination, Human Incompetence, Pseudoscience, Environmental Impact, Disinformation,Copyright Violation, Mental Health):
    - Subclasses (e.g. Discrimination->Data bias, Discrimination->Algorithmic bias,Human Incompetence->Administrative, Human Incompetence->Technical, Pseudoscience->Facial, Disinformation->Textual, Disinformation->Image, Disinformation->Video, Disinformation->Audio, Other):
    - Sub-subclass (e.g. Data bias->gender, Data bias->race, Data bias->sexual orientation,Data bias->economic, algorithmic bias->interaction, algorithmic bias -> feedback loop, algorithmic bias -> optimization function, algorithmic bias -> other)
    - Area of AI Application (e.g. content filtering, surveillance, illness prediction)
    - Online (yes or no):
    

    Article Content:
    {text}

    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4-turbo-preview",
        "promp": prompt,
        "temperature":0.5,

    }

    response = requests.post(api_url, headers=headers,json=data)
    return response.json()

# import news URL json file and loop through 
with open("newsUrls.json","r") as file:
    urls_dict = json.load(file)

logging.info("Successfully loaded JSON data, starting to scrape articles...")

aggregated_content = {}

# TODO: remove counter (testing with the first 5 incidents)
count = 0
for id,urls in urls_dict.items():
    if count == 5:
        break
    count += 1
    aggregated_texts = []
    for url in urls:
        article_text = scrape_article(url)
        aggregated_texts.append(article_text)
    aggregated_content[id] = ". ".join(aggregated_texts)

logging.info("Article scraping completed. Processing with LLM...")

processed_results = {}
for id,content in aggregated_content.items():
    result = process_content(content,KEY)
    processed_results[id] = result

logging.info("LLM processing completed. Saving results to file...")

with open("processed_results.json","w") as json_file:
    json.dump(processed_results,json_file, indent=4)

logging.info("Results saved to JSON file. Script completed successfully.")