from newspaper import Article
import json
from api.openai_api import OpenaiAPI
from dotenv import load_dotenv
import logging
import datetime
from format_checker import FormatChecker

load_dotenv()
openai_client = OpenaiAPI()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting the script...")
logging.info("Loading JSON data from file...")

TAXONOMY_STRING_FORMATTED = "taxonomy_string_formatted"
TAXONOMY_STRING = "taxonomy_string"
ZERO_SHOT = "zero_shot"
TREE_OF_THOUGHTS = "tree_of_thoughts"
FEW_SHOTS_COT = "few_shots_CoT_prompt"
FEW_SHOTS = "few_shots"
FEW_SHOTS_COT_STEPS = "few_shots_CoT_steps"
TREE_OF_THOUGHTS_COT = "ToT_CoT"
COT_USER_PROMPT = "COT_USER_PROMPT"
prompt_type = COT_USER_PROMPT

# get incident ids of 2023
path_to_file = "/Users/chenyian261/Documents/GitHub/IrresponsibleAI/ids_2023.json"

with open(path_to_file, "r") as file:
    ids_2023 = json.load(file)
set_ids_2023 = set(str(i) for i in ids_2023)
# id_set = set([0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 451, 382, 505, 167])
# scraped_set = (str(i) for i in id_set)

# # function that uses Newspaper3k library to scrape article
# def scrape_article(url):
#     article = None
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#     except:
#         logging.info(f"the URL {url} cannot be accessed")
#         return ""
#     return article.text


# # import news URL json file and loop through
# with open("newsUrls.json", "r") as file:
#     urls_dict = json.load(file)

# # logging.info("Successfully loaded JSON data, starting to scrape articles...")

aggregated_content = {}

# # TODO: remove counter (testing with the first 5 incidents)
# count = 0
# print("HEREEEEE")
# for id, urls in urls_dict.items():
#     if count == 15:
#         break
#     count += 1
#     aggregated_texts = []
#     for url in urls:
#         article_text = scrape_article(url)
#         aggregated_texts.append(article_text)
#         concated = ". ".join(aggregated_texts)
#     aggregated_content[id] = concated
#     # file_path = f"/Users/chenyian261/Documents/GitHub/IrresponsibleAI/article_texts/{id}.txt"
#     # with open(file_path, "w") as f:
#     #     f.write(concated)

for i in range(1, 2):
    file_path = (
        f"/Users/chenyian261/Documents/GitHub/IrresponsibleAI/article_texts/{i}.txt"
    )
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
    aggregated_content[str(i)] = file_content

logging.info("Article scraping completed. Processing with LLM...")

processed_results = {}
format_checker = FormatChecker()
for id, content in aggregated_content.items():
    result, prompt = openai_client.process_content(content, prompt_type)
    json_result = json.loads(result)
    check = format_checker.check_format(json_result)
    processed_results[id] = json_result
    # check if the first result has issues
    if not check:
        replace_result, _ = openai_client.process_content(
            aggregated_content[id], ZERO_SHOT
        )
        json_replace = json.loads(replace_result)
        processed_results[id] = json_replace
    # processed_results["prompt-"+id] = prompt

logging.info("LLM processing completed. Saving results to file...")

current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
with open(
    f"./processed_output/{prompt_type}/processed_results_{current_time}.json", "w"
) as json_file:
    json.dump(processed_results, json_file, indent=4)

logging.info("Results saved to JSON file. Script completed successfully.")

# logging.info("Starting result-checking...")

# double_check = set()
# for id,result in processed_results.items():
#     issues = openai_client.check_result(aggregated_content[id],result)
#     if issues:
#         double_check.add(id)
#         replace_result = openai_client.process_content(aggregated_content[id],ZERO_SHOT)
#         json_replace = json.loads(replace_result)
#         processed_results[id]=json_replace
# print("DOUBLE_CHECK",double_check)
# with open(f"./processed_output/{prompt_type}/processed_results_{current_time}_checked.json","w") as json_file:
#     json.dump(processed_results,json_file, indent=4)

# logging.info("Check completed. Results saved to JSON file. Script completed successfully.")
