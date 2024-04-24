import os
from dotenv import load_dotenv
import requests
import re


def clean_filename(filename):
    """
    function to clean up string to be used as filename
    :param filename: original string to be cleaned up
    :return: cleaned up string safe for use as a file name
    """
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  # remove special characters
    return filename


def build_payload(query: str, start=1, num=10, **params):
    """
    function to build payload for the Google Search API request
    :param query: search term
    :param start: index of the first result to return
    :param num: how many results returned
    :param params: additional parameters for the API request

    :return: Dictionary containing the API request parameters
    """
    load_dotenv()
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    payload = {"key": SEARCH_API_KEY, "q": query, "cx": SEARCH_ENGINE_ID, "num": num}

    payload.update(params)
    return payload


def make_request(payload):
    """
    function that sends GET request to Google Search API and handle potential errors
    :param payload: Dictionary containing API request parameters
    :return: JSON response from the API
    """
    response = requests.get(
        "https://customsearch.googleapis.com/customsearch/v1", params=payload
    )
    if response.status_code != 200:
        raise Exception("Request failed")
    print("SEARCH API RESPONSE=========", response.json())
    return response.json()


def get_location(query):
    print("CALLEDDDDDDD")
    payload = build_payload(query)
    response = make_request(payload)
    return response
