from openai import OpenAI
import api.prompt_factory as prompt_factory

class OpenaiAPI:
    def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model
    
    def create_prompt(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0.3,

        )
        return completion.choices[0].message.content
    
    def process_content(self,article_text,prompt_type):

        prompt = prompt_factory.get_prompt(article_text,prompt_type)
        messages = [{"role": "user", "content": prompt},
                    {"role": "system", "content":"You are a helpful university assistant designed to classify news articles to specific categories. Your output will be in JSON."}]

        response = self.create_prompt(messages)
        return response, prompt
    
    def check_result(self,article_text,result):

        prompt = prompt_factory.get_prompt_for_check(article_text,result)
        messages = [{"role": "user", "content": prompt},
                    {"role": "system", "content":"You are a helpful university assistant designed to classify news articles to specific categories."}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=5
        )
        text_response = response.choices[0].message.content
        print("====TEXT RESPONSE======",text_response)
        if text_response.lower() in set(["yes", "true", "indeed", "correct", "affirmative"]):
            return True
        else:
            return False
    
