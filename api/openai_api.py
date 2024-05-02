from openai import OpenAI
import api.prompt_factory as prompt_factory
from .results import *
from .search_request import *
import json
from .param_data import *


class OpenaiAPI:
    """
    Initializes the OpenAI API client with a specific model.

    Parameters:
        model (str): The model identifier to be used with the OpenAI API.
    """

    def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model
        self.available_functions = {"get_location": get_location}

    def get_data(self, prompt_type, article_text):
        """
        Retrieves messages, tools, and prompts necessary for the chat completions API based on the given prompt type and article text.

        Parameters:
            prompt_type (str): The type of prompt to generate.
            article_text (str): The article text to process.

        Returns:
            tuple: A tuple containing the list of messages, tools configuration, and the prompt string.
        """
        prompt = prompt_factory.get_prompt(article_text, prompt_type)
        messages = get_messages(prompt, article_text, "multi")
        tools = get_tools()
        return messages, tools, prompt

    def handle_tool_calls(self, tool_calls):
        """
        Processes external function calls based on the tool calls suggested by the LLM, returning location candidates.

        Parameters:
            tool_calls (list): A list of tool call specifications received from the LLM.

        Returns:
            list: A list of location candidates extracted from the external function calls.
        """
        location_candidates = []
        available_functions = self.available_functions
        search = None
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # print("FUNCTION TO CALL", function_to_call)
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(query=function_args.get("query"))
            # print(">>>>>>FUNCTION RESPONSE>>>>>", function_response)
            search = function_response
        temp_snippet = []
        temp_metatag = []
        i = 0
        if search:
            for item in search["items"]:
                temp_snippet.append(item.get("snippet", "No snippet available"))
                pagemap = item.get("pagemap", {})
                metatags = pagemap.get("metatags", [{}])
                temp_metatag.append(metatags[0])
            for snippet, metatag in zip(temp_snippet, temp_metatag):
                location_candidates.append((i, snippet, metatag))
                i += 1
        # print("Location candidates====", location_candidates)
        return location_candidates

    def process_content(self, article_text, prompt_type):
        """
        Processes the article content by calling the chat completions API and handling external search functions to locate company information.

        Parameters:
            article_text (str): The article text to analyze.
            prompt_type (str): The type of prompt to generate for the completion.

        Returns:
            tuple: A tuple containing the response from the LLM and the generated prompt.
        """
        message, tools, prompt = self.get_data(prompt_type, article_text)

        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=message,
            temperature=0.3,
            tools=tools,
            tool_choice="auto",
        )
        response_message = completion.choices[0].message
        tool_calls = response_message.tool_calls
        print("=====TOOL CALLS=====", tool_calls)
        if tool_calls:
            location_candidates = self.handle_tool_calls(tool_calls)
            new_message = update_messages_with_location(
                article_text, prompt, location_candidates
            )
            completion = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=new_message,
                temperature=0.3,
            )
        response = completion.choices[0].message.content
        return response, prompt

    # optional
    def check_result(self, article_text, result):
        """
        Validates the result by asking a follow-up question and checking the response.

        Parameters:
            article_text (str): The text of the article associated with the result.
            result (str): The result to validate.

        Returns:
            bool: True if the response is affirmative, False otherwise.
        """
        prompt = prompt_factory.get_prompt_for_check(article_text, result)
        messages = [
            {"role": "user", "content": prompt},
            {
                "role": "system",
                "content": "You are a helpful assistant",
            },
        ]

        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.3, max_tokens=5
        )
        text_response = response.choices[0].message.content
        if text_response.lower() in set(
            ["yes", "true", "indeed", "correct", "affirmative"]
        ):
            return True
        else:
            return False
