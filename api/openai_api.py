from openai import OpenAI
import api.prompt_factory as prompt_factory
from .results import *
from .search_request import *
import json
from .param_data import *
import datetime


class OpenaiAPI:
    def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model
        self.available_functions = {"get_location": get_location}

    def get_data(self, prompt_type, article_text):
        """
        returns messages, tool, and prompts for chat completions API arguments
        """
        prompt = prompt_factory.get_prompt(article_text, prompt_type)
        messages = get_messages(prompt, article_text, "multi")
        tools = get_tools()
        return messages, tools, prompt

    def handle_tool_calls(self, tool_calls):
        location_candidates = []
        available_functions = self.available_functions
        i = 0
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        location_directory = (
            f"{os.path.abspath(os.path.dirname(__file__))}/location_{current_time}"
        )
        os.makedirs(location_directory, exist_ok=True)
        for tool_call in tool_calls:
            i += 1
            with open(f"{location_directory}/{i}.txt", "w") as location_file:
                location_file.write(f"{location_candidates}")
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            print("FUNCTION TO CALL", function_to_call)
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(query=function_args.get("query"))
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
        return location_candidates

    def process_content(self, article_text, prompt_type):
        """
        function that calls chat completions API from OpenAI in get_data() and external search function
        to search company location
        :param article_text: type string article text to pass to get data
        :param prompt_type: type string prompt type to get prompt
        :return: response from LLM and prompt
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

    def check_result(self, article_text, result):

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
