import os
from dotenv import load_dotenv
import requests
import re


def clean_filename(filename):
    """Cleans a string to make it safe for use as a filename by removing special characters.

    Parameters:
        filename (str): The original filename string to be sanitized.

    Returns:
        str: A cleaned string safe for use as a filename.
    """
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # remove special characters
    return filename


def build_payload(query: str, start=1, num=10, **params):
    """
    Constructs a dictionary payload for making a Google Search API request.

    Parameters:
        query (str): The search term for the API request.
        start (int): The starting index of the search results (default is 1).
        num (int): The number of search results to return (default is 10).
        **params: Additional parameters to customize the API request.

    Returns:
        dict: A dictionary containing the parameters for the API request.
    """
    load_dotenv()
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    payload = {"key": SEARCH_API_KEY, "q": query, "cx": SEARCH_ENGINE_ID, "num": num}

    payload.update(params)
    return payload


def make_request(payload):
    """
    Sends a GET request to the Google Search API using the provided payload and handles errors.

    Parameters:
        payload (dict): A dictionary containing the parameters for the API request.

    Returns:
        dict: The JSON response from the API.

    Raises:
        Exception: If the request to the API fails.
    """
    response = requests.get(
        "https://customsearch.googleapis.com/customsearch/v1", params=payload
    )
    if response.status_code != 200:
        raise Exception("Request failed")
    return response.json()


def get_location(query):
    payload = build_payload(query)
    response = make_request(payload)
    return response
