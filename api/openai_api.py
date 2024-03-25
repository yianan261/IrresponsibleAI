from openai import OpenAI
from .taxonomies import Taxonomies
from .results import example_output
import api.prompt_factory as prompt_factory

class OpenaiAPI:
    def __init__(self, model="gpt-4-turbo-preview"):
        self.client = OpenAI()
        self.model = model
    
    def create_prompt(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0.2
        )
        return completion.choices[0].message.content
    
    def process_content(self,article_text,prompt_type):

        prompt = prompt_factory.get_prompt(article_text,prompt_type)
        messages = [{"role": "user", "content": prompt},
                    {"role": "system", "content":"You are a helpful university assistant designed to classify news articles to specific categories. Your output will be in JSON."}]

        response = self.create_prompt(messages)
        return response
