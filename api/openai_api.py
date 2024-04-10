from openai import OpenAI
import api.prompt_factory as prompt_factory
from .results import *
from llmlingua import PromptCompressor


class OpenaiAPI:
    def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model

    def create_prompt(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=messages,
            temperature=0.3,
        )
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
             Follow the previous steps 1. provide classification and reasoning 2. check your facts if the city, state, country of the company involved is correct 3. give your final classification results in JSON format
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
