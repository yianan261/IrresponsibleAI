from openai import OpenAI
import api.prompt_factory as prompt_factory
from .results import *
from .search_request import *
import json


class OpenaiAPI:
    def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model

    def create_prompt(self, messages):
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
                                "description": "The question for the search engine to search for the city and state of the company. It should be a question, specifically ask which state and which city",
                            },
                        },
                        "required": ["query"],
                    },
                },
            }
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=messages,
            temperature=0.3,
            tools=tools,
            tool_choice="auto",
        )
        response_message = completion.choices[0].message
        print("====/////RESPONSE MESSAGE///====", response_message)
        tool_calls = response_message.tool_calls
        print("=====TOOL CALLS=====", tool_calls)
        if tool_calls:
            available_functions = {"get_location": get_location}
            messages.append(available_functions)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                print("FUNCTION TO CALL", function_to_call)
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(query=function_args.get("query"))
                print("FUNCTION RESPONSE ==========", function_response)
        print("COMPLETION", completion.choices[0])
        return completion.choices[0].message.content

    def process_content(self, article_text, prompt_type):

        prompt = prompt_factory.get_prompt(article_text, prompt_type)

        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        message_multi_turn = [
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
             Follow the previous steps 1. provide classification and reasoning 2. check your facts: check if the city, state, country of the company involved is correct, you may use function calling. give your final classification results in JSON format
             """,
            },
        ]
        response = self.create_prompt(message_multi_turn)
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
        print("====TEXT RESPONSE======", text_response)
        if text_response.lower() in set(
            ["yes", "true", "indeed", "correct", "affirmative"]
        ):
            return True
        else:
            return False
