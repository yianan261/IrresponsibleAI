from newspaper import Article
import json
from api.openai_api import OpenaiAPI
from dotenv import load_dotenv
import logging
import datetime

load_dotenv()
openai_client = OpenaiAPI()

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
    result = openai_client.process_content(content)
    json_result = json.loads(result)
    processed_results[id] = json_result

logging.info("LLM processing completed. Saving results to file...")

current_time = datetime.datetime.now().strftime("%Y_%m-_%d_%H_%M")
with open(f"processed_results_{current_time}.json","w") as json_file:
    json.dump(processed_results,json_file, indent=4)

logging.info("Results saved to JSON file. Script completed successfully.")