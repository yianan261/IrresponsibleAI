from .results import *
import json


def get_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_location",
                "description": "Get the company city and company state location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The question for the search engine to search for the city and state of the company. It should be a question, for example where is the headquarters of so-and-so company?",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    ]
    return tools


def get_messages(article_text, prompt="", message_type="one"):
    """
    Constructs a message list for chat completions API based on provided parameters.

    This function also invokes the `get_location()` method from the Google Custom Search API

    Parameters:
        prompt (str): The initial user prompt for the language model (LLM).
        article_text (str): The text of the article involved in the incident.
        message_type (str): Determines the structure of the conversation.
                            "one" for a single interaction, "multi" for a multi-step interaction.

    Returns:
        list[dict]: A list of message dictionaries. Each dictionary represents a step in the conversation,
                    containing 'role' (either 'system' or 'user') and 'content' (text of the message).
    """
    message = []
    if message_type == "one":
        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    elif message_type == "multi":
        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"""
            Read this article and do the following: 
            ====start of article====
            {article_text}
            ====end of article ====
            What is the name of the company that caused the problem according to the article? Think about it and note it down.
            Now, find the city and state of the company that caused the problem. You may use function calling to find the company location.
            Return JSON response.
            If there are multiple companies involved, skip this step and return empty JSON.
            """,
            },
        ]
    return message


def update_messages_with_location(
    prompt, message_type="one", article_text="", location_candidates=[]
):
    """Updates and returns a message list for the chat completions API that includes steps
    Parameters:
        article_text (str): The text of the article involved in the incident.
        prompt (str): The initial prompt for the language model to start the conversation.
        location_candidates (list): A list of location results from Google Custom Search API, which are potential
                                    locations of the company mentioned in the article text.

    Returns:
        list[dict]: An extended list of message dictionaries structured for a multi-turn conversation for chat completions API
    """
    message = []
    if message_type == "multi":
        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "content": example_output_explanation_id_1,
            },
            {
                "role": "user",
                "content": "Check if your reasoning makes sense and is supported by the article text. Give your final classification result in JSON format",
            },
            {
                "role": "assistant",
                "content": example_output_id_1,
            },
            {
                "role": "user",
                "content": f"""
            now, please read this article and keep this article in mind: 
            ====start of article====
            {article_text}
            ====end of article ====
            please do the following:
            request 1. Follow the previous example steps for this article, provide classification and reasoning. Construct your final classification results in JSON format.
            request 2. From this list of location candidates from Google Search API that returns search results on the city and state of the company, 
            ```location candidates = {location_candidates}```
            determine which candidate most-likely has the correct location of company in question in the article and note the city and state of the company of the chosen candidate.
            Compare the `company city` and `company state` field results with your result from request 1; determine which `company city` and `company state` are the correct answers and update if necessary. Provide your final full classification result in JSON.
            If the location candidates list is empty, you may just return the classification results in JSON format.
            """,
            },
        ]
    elif message_type == "one":
        message = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You must return results in JSON format",
            },
            {"role": "user", "content": prompt},
        ]
    return message
