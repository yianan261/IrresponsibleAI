from newspaper import Article
import json
from api.openai_api import OpenaiAPI
from dotenv import load_dotenv
import logging
import datetime
from format_checker import FormatChecker
import os
from incident_data import IncidentData


class FileNotFoundError(Exception):
    pass


class NewsContent:
    def __init__(self):
        self.aggregated_content = {}
        self.base = os.path.abspath(os.path.dirname(__file__))
        self.openai_client = OpenaiAPI()
        self.processed_results = {}

    # using Newspaper3k library to scrape article
    def scrape_article(self, url):
        article = None
        try:
            article = Article(url)
            article.download()
            article.parse()
        except:
            logging.info(f"the URL {url} cannot be accessed")
            return ""
        return article.text

    def fill_article_content(self, write=False):
        # import news URL json file and loop through
        with open("newsUrls.json", "r") as file:
            urls_dict = json.load(file)

        logging.info("Successfully loaded JSON data, starting to scrape articles...")

        aggregated_content = self.aggregated_content

        # TODO: remove counter (testing with the first 5 incidents)
        count = 0
        for id, urls in urls_dict.items():
            if count == 15:
                break
            count += 1
            aggregated_texts = []
            for url in urls:
                article_text = self.scrape_article(url)
                aggregated_texts.append(article_text)
                concated = ". ".join(aggregated_texts)
            aggregated_content[id] = concated
            # write to file
            if write == True:
                file_path = f"{self.base}/article_texts/{id}.txt"
                with open(file_path, "w") as f:
                    f.write(concated)

        logging.info("Article scraping completed. Processing with LLM...")
        return

    # the directory article_texts already contains previously scraped articles. For articles already scraped there's no need to re-scrape
    def read_article_from_file(self, id_set):
        aggregated_content = self.aggregated_content
        for i in id_set:
            try:
                file_path = f"{self.base}/article_texts/{i}.txt"
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()
                aggregated_content[str(i)] = file_content
            except FileNotFoundError:
                raise FileNotFoundError(f"File for ID {i} does not exist")
        return

    def process_aggregate_results(self, prompt_type, check_prompt):
        processed_results = self.processed_results
        aggregated_content = self.aggregated_content
        openai_client = self.openai_client
        format_checker = FormatChecker()
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        results_directory = f"{self.base}/processed_output_individual/{prompt_type}/results_{current_time}"
        os.makedirs(results_directory, exist_ok=True)
        prompt = ""
        for id, content in aggregated_content.items():
            result, prompt = openai_client.process_content(content, prompt_type)
            try:
                individual_result = {}
                json_result = json.loads(result)
                check = format_checker.check_format(json_result)
                processed_results[id] = json_result
                individual_result[id] = json_result
                # check if the first result has format issues
                if not check:
                    replace_result, _ = openai_client.process_content(
                        aggregated_content[id], check_prompt
                    )
                    json_replace = json.loads(replace_result)
                    processed_results[id] = json_replace
                    individual_result[id] = json_replace
                # writing individual results
                with open(
                    f"{results_directory}/id_{id}_processed_results.json",
                    "w",
                ) as json_file:
                    json.dump(individual_result, json_file, indent=4)
            except json.JSONDecodeError as e:
                logging.error(
                    f"Error decoding JSON data from API response for ID {id}: {e}"
                )
                continue
            except Exception as e:
                logging.error(f"An error occurred for ID {id}: {e}")
                raise
        with open(f"{results_directory}/prompt.txt", "w") as prompt_file:
            prompt_file.write(prompt)

        logging.info("LLM processing completed. Saving aggregate results to file...")
        # writing aggregate results
        with open(
            f"./processed_output/{prompt_type}/processed_results_{current_time}.json",
            "w",
        ) as json_file:
            json.dump(processed_results, json_file, indent=4)

        logging.info("Aggregate results saved to JSON file...")
        return

    def get_double_check(self, prompt_type, check_prompt):
        processed_results = self.processed_results
        aggregated_content = self.aggregated_content
        openai_client = self.openai_client
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        logging.info("Starting result-checking...")
        double_check = set()
        for id, result in processed_results.items():
            issues = openai_client.check_result(aggregated_content[id], result)
            if issues:
                double_check.add(id)
                replace_result = openai_client.process_content(
                    aggregated_content[id], check_prompt
                )
                json_replace = json.loads(replace_result)
                processed_results[id] = json_replace
        print("DOUBLE_CHECK", double_check)
        with open(
            f"./processed_output/{prompt_type}/processed_results_{current_time}_checked.json",
            "w",
        ) as json_file:
            json.dump(processed_results, json_file, indent=4)

        logging.info("Check completed. Results saved to JSON file.")
        return

    def main(self, scrape_articles=False, double_check=False):
        load_dotenv()

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

        data = IncidentData()
        if scrape_articles == True:
            self.fill_article_content()
        else:
            id_set = data.get_handpicked_id_set()
            self.read_article_from_file(id_set)
            self.process_aggregate_results(prompt_type, ZERO_SHOT)

        if double_check == True:
            self.get_double_check(prompt_type, ZERO_SHOT)

        logging.info("Script completed successfully.")

        return


if __name__ == "__main__":
    incident_results = NewsContent()
    incident_results.main()
