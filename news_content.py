from newspaper import Article
import json
from api.openai_api import OpenaiAPI
from dotenv import load_dotenv
import logging
import datetime
from format_checker import FormatChecker
import os
from incident_data import IncidentData
import concurrent.futures
import random
from check_urls import process_urls
import re
import argparse


class NewsContent:

    TAXONOMY_STRING_FORMATTED = "taxonomy_string_formatted"
    TAXONOMY_STRING = "taxonomy_string"
    ZERO_SHOT = "zero_shot"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    FEW_SHOTS_COT = "few_shots_cot_prompt"
    FEW_SHOTS = "few_shots"
    FEW_SHOTS_COT_STEPS = "few_shots_cot_steps"
    TREE_OF_THOUGHTS_COT = "tot_cot"
    COT_USER_PROMPT = "cot_user_prompt"
    TOT_MULTI_TURN = "tot_cot_multi_turn"
    TOT_COT_2 = "tot_cot_2"

    def __init__(self):
        self.aggregated_content = {}
        self.base = os.path.abspath(os.path.dirname(__file__))
        self.openai_client = OpenaiAPI()
        self.processed_results = {}
        self.issues = dict()

    def _scrape_article(self, url) -> str:
        """
        Attempts to download and parse an article from a given URL using the Newspaper3k library.
        Logs a message if the article cannot be accessed.

        Args:
            url (str): The URL from which to scrape the article.

        Returns:
            str: The text content of the article, or an empty string if an error occurs.
        """
        article = None
        try:
            article = Article(url)
            article.download()
            article.parse()
        except Exception as e:
            logging.info(f"the URL {url} cannot be accessed: {e}")
            return ""
        return article.text

    def _fill_article_content(self, write=False):
        """
        Retrieves URLs to scrape, downloads articles, aggregates content, and optionally writes to files.

        Args:
            write (bool): If True, writes the aggregated article content to local files.

        Returns:
            None
        """
        urls_dict = process_urls()

        logging.info("Successfully loaded JSON data, starting to scrape articles...")

        aggregated_content = self.aggregated_content
        for id, urls in urls_dict.items():
            if len(urls) > 2:
                urls = random.sample(urls, 2)
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                article_texts = list(executor.map(self._scrape_article, urls))
            concated = ". ".join(article_texts)
            aggregated_content[id] = concated
            # write to file
            if write:
                file_path = os.path.join(self.base, "article_texts", f"{id}.txt")
                try:
                    with open(file_path, "w") as f:
                        f.write(concated)
                except IOError as e:
                    logging.error(f"Failed to write to file {file_path}: {e}")

        logging.info("Article scraping completed. Processing with LLM...")
        return

    def _read_article_from_file(self, id_set):
        """
        Reads article content from local files for a given set of IDs.

        Args:
            id_set (set): A set of article IDs to read from local files.

        Returns:
            None

        Raises:
            FileNotFoundError: If a file for an ID does not exist.
        """
        aggregated_content = self.aggregated_content
        for i in id_set:
            try:
                file_path = os.path.join(self.base, "article_texts", f"{i}.txt")
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()

                cleaned_content = re.sub(r"\n+", "\n", file_content)
                aggregated_content[str(i)] = cleaned_content
            except FileNotFoundError:
                logging.error(f"File for ID {i} does not exist, skipping...")
                continue

        return

    def _process_aggregate_results(self, prompt_type, check_prompt):
        """
        Processes scraped articles through OpenAI API, classifies content, and saves results.

        Args:
            prompt_type (str): The type of prompt to use for OpenAI classification.
            check_prompt (str): The prompt to use if re-checking is needed.

        Returns:
            None
        """
        processed_results = self.processed_results
        aggregated_content = self.aggregated_content
        openai_client = self.openai_client
        format_checker = FormatChecker()
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        results_directory = f"{self.base}/processed_output_individual/{prompt_type}/results_{current_time}"
        os.makedirs(results_directory, exist_ok=True)
        prompt = ""

        for id, content in aggregated_content.items():
            try:
                result, prompt = openai_client.process_content(content, prompt_type)
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
                self.issues[id] = f"{e}"
                continue
            except IOError as e:
                logging.exception(f"File I/O error for ID {id}: {e}")
                self.issues[id] = f"{e}"
                continue
            except Exception as e:
                logging.exception(f"An error occurred for ID {id}: {e}")
                self.issues[id] = f"{e}"
                continue
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
        print("FILES WITH ISSUES", self.issues)
        return

    def _get_double_check(self, prompt_type, check_prompt):
        """
        Rechecks processed results with OpenAI API to ensure accuracy and updates results.

        Args:
            prompt_type (str): The type of prompt to use for initial checks.
            check_prompt (str): The prompt to use for rechecking.

        Returns:
            None
        """
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
        with open(
            f"./processed_output/{prompt_type}/processed_results_{current_time}_checked.json",
            "w",
        ) as json_file:
            json.dump(processed_results, json_file, indent=4)

        logging.info("Check completed. Results saved to JSON file.")
        return

    def main(
        self,
        scrape_articles=False,
        double_check=False,
        start=0,
        end=10,
        prompt_type="ToT_CoT_Multi_turn",
    ):
        load_dotenv()

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.info("Starting the script...")
        logging.info("Loading JSON data from file...")

        allowed_prompt_types = [
            NewsContent.TAXONOMY_STRING_FORMATTED,
            NewsContent.TAXONOMY_STRING,
            NewsContent.ZERO_SHOT,
            NewsContent.TREE_OF_THOUGHTS,
            NewsContent.FEW_SHOTS_COT,
            NewsContent.FEW_SHOTS,
            NewsContent.FEW_SHOTS_COT_STEPS,
            NewsContent.TREE_OF_THOUGHTS_COT,
            NewsContent.COT_USER_PROMPT,
            NewsContent.TOT_MULTI_TURN,
            NewsContent.TOT_COT_2,
        ]

        if prompt_type.lower() not in allowed_prompt_types:
            raise ValueError(
                f"Invalid prompt_type provided: {prompt_type}. Allowed values: {', '.join(allowed_prompt_types)}"
            )

        data = IncidentData()
        if scrape_articles:
            self._fill_article_content()
        else:
            # id_set = data.get_incidents_2023()
            id_remove = data.get_empty_data()
            id_set = data.get_handpicked_id_set(start, end)
            logging.info(f"Requested IDs to process {id_set}")
            ids_to_process = id_set - id_remove
            to_process = sorted(ids_to_process)
            logging.info(f"Processing IDs {to_process}")
            self._read_article_from_file(ids_to_process)

        self._process_aggregate_results(prompt_type, NewsContent.ZERO_SHOT)

        if double_check == True:
            self._get_double_check(prompt_type, NewsContent.ZERO_SHOT)

        logging.info("Script completed successfully.")

        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process news articles and analyze with LLM."
    )
    parser.add_argument(
        "--scrape_articles", action="store_true", help="Scrape articles from URLs"
    )
    parser.add_argument(
        "--double_check", action="store_true", help="Double-check the processed results"
    )
    parser.add_argument(
        "--start", type=int, default=0, help="Start of handpicked ID range"
    )
    parser.add_argument(
        "--end", type=int, default=10, help="End of handpicked ID range"
    )
    parser.add_argument(
        "--prompt_type",
        type=str,
        default="tot_cot_multi_turn",
        help="Type of prompt to use",
    )

    args = parser.parse_args()

    incident_results = NewsContent()
    incident_results.main(
        scrape_articles=args.scrape_articles,
        double_check=args.double_check,
        start=args.start,
        end=args.end,
        prompt_type=args.prompt_type,
    )
