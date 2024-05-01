import json
import requests
import concurrent.futures


def _is_url_accessible(url):
    """Check if the URL is accessible and returns HTML content.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is accessible and contains HTML content, else False
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.head(url, headers=headers, timeout=5)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            return "text/html" in content_type
        return False

    except requests.RequestException:
        return False


def _check_urls_concurrently(urls):
    """Check a list of URLs concurrently for accessibility and content type.

    Args:
        urls (list of str): A list of URLs to check.

    Returns:
        list of bool: A list of results corresponding to whether each URL is accessible and HTML.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(_is_url_accessible, urls))
    return results


def process_urls():
    """Process URLs from urls JSON file from AIID to check their accessibility.

    Reads URLs from a JSON file, checks each URL for accessibility and HTML content, and updates
    the dictionary with only URLs that meet the criteria.

    Returns:
        dict: A dictionary with IDs as keys and lists of accessible HTML URLs as values.
    """
    with open("newsUrls.json", "r") as file:
        urls_dict = json.load(file)
    updated_urls_dict = {}
    for id, urls in urls_dict.items():
        print(f"Checking URLs for ID: {id}")
        results = _check_urls_concurrently(urls)
        working_urls = [url for url, valid in zip(urls, results) if valid]
        updated_urls_dict[id] = working_urls
    return updated_urls_dict
