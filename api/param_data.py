from .results import *


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
                            "description": "The question for the search engine to search for the city and state of the company. It should be a question, for example where is the headquarter of so-and-so company?",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    ]
    return tools


def get_messages(prompt, article_text, message_type="one"):
    """
    :param prompt: prompt for the LLM
    :param article_text: incident article
    :message_type: if "one" selected only one prompt. If "multi" selected there will be a multi-role conversation
    :return: message list for chat completions API.
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
            Find the city and state of the company in question in the article. You may use function calling.
            Return JSON response.
            """,
            },
        ]
    return message


def update_messages_with_location(article_text, prompt, location_candidates):
    """
    :param article_text: incident article
    :param prompt: prompt for the LLM
    :param location_candidates: list of Google Custom Search API result for LLM to determine location of the company
    :return: message list for chat completions API
    """
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
            read this article: 
            ====start of article====
            {article_text}
            ====end of article ====
            please do the following:
            request 1. Follow the previous example steps, provide classification and reasoning. Construct your final classification results in JSON format.
            request 2. From this list of location candidates from Google Search API that returns search results on the city and state of the company, 
            ```location candidates = {location_candidates}```
            determine which candidate most-likely has the correct location of company in question in the article and note the city and state of the company of the chosen candidate.
            Compare the `company city` and `company state` field results with your result from request 1; determine which `company city` and `company state` are the correct answers and update if necessary. Provide your final full classification result in JSON.
            """,
        },
    ]
    return message
