from openai import OpenAI
from taxonomies import Taxonomies

class OpenaiAPI:
    def __init__(self, model="gpt-4-turbo-preview"):
        self.client = OpenAI()
        self.model = model
    
    def create_prompt(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0.5
        )
        return completion.choices[0].message.content
    
    def process_content(self,article_text):
        taxa = Taxonomies()

        prompt = f"""
        Imagine a computer research institute trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles:
        - Country:
        - State:
        - City:
        - Continent:
        - Company city:
        - Affected population (e.g.{taxa.population_examples},please classify the population according to your judgment, it need not be from this list):
        - Number of people actually affected:
        - Number of people potentially affected:
        - Classes of irresponsible AI use (please refer to this list: {list(taxa.get_taxonomy_keys())}, there could be more than one classes the article classifies as):
        - Subclasses (e.g. {taxa.get_category("subclass")}, please classify the subclasses according to your judgment, it need not necessary be from this list, but it is a subclass from "Classes of irresponsible AI use"; there could be one or multiple subclasses):
        - Sub-subclasses (e.g.{taxa.get_category("subsubclass")},please classify the Sub-subclasses according to your judgment, it need not necessary be from this list, but it is a subclass from the "Subclasses"; there could be one or multiple sub-subclasses):
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction)
        - Online (yes or no):
        
        Article Content:
        {article_text}

        This is the end of a text.

        """

        messages = [{"role": "user", "content": prompt},
                    {"role": "system", "content":"You are a helpful university assistant designed to output your response in JSON according to the user's prompt."}]

        response = self.create_prompt(messages)
        return response
