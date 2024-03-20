from openai import OpenAI
from .taxonomies import Taxonomies
from .results import example_output

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
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        Regarding "Sub-subclass", only find the relation in the given taxonomy. If a field does not have a sub-subclass list, then leave sub-subclass list as empty.
        Refer to {example_output} for json output examples.
        - Country:
        - State:
        - City:
        - Continent:
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Affected population (e.g.{taxa.population_examples},please classify the population according to your judgment, it need not necessarily be from this list): 
        - Number of people actually affected:
        - Number of people potentially affected:
        - Classes of irresponsible AI use (please refer to this taxonomy: {taxa.get_category("class")}, there could be more than one classes the article classifies as):
        - Subclasses (refer to this taxonomy: {taxa.get_category("subclass")} The subclasses should be the children of the "Classes of irresponsible AI use"):
        - Sub-subclasses (refer to this taxonomy: {taxa.get_category("subsubclass")}. If a subclass does not have a sub-subclass list for children,leave the sub-subclass list empty.
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
        
        Article Content:

        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content =================
        
        """

        messages = [{"role": "user", "content": prompt},
                    {"role": "system", "content":"You are a helpful university assistant designed to output your response in JSON according to the user's prompt, and you follow the prompt instructions closely."}]

        response = self.create_prompt(messages)
        return response
