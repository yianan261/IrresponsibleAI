from openai import OpenAI


class OpenaiAPI:
    def __init__(self, model="gpt-3.5-turbo"):
        self.client = OpenAI()       
        self.model = model
    
    def create_prompt(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={ "type": "json_object"}
        )
        return completion.choices[0].message.content

    def process_content(self, article_text):
        
        prompt = f"""
        Please extract the following informaiton from the news article:
        - Country:
        - State:
        - City:
        - Continent:
        - Company city:
        - Affected population (e.g. Military, LGBTQ, Student, Facebook users, Black, Online Female population, EU travelers, Twitter users):
        - Number of people actually affected:
        - Number of people potentially affected:
        - Class of irresponsible AI use (e.g. Discrimination, Human Incompetence, Pseudoscience, Environmental Impact, Disinformation,Copyright Violation, Mental Health):
        - Subclasses (e.g. Discrimination->Data bias, Discrimination->Algorithmic bias,Human Incompetence->Administrative, Human Incompetence->Technical, Pseudoscience->Facial, Disinformation->Textual, Disinformation->Image, Disinformation->Video, Disinformation->Audio, Other):
        - Sub-subclass (e.g. Data bias->gender, Data bias->race, Data bias->sexual orientation,Data bias->economic, algorithmic bias->interaction, algorithmic bias -> feedback loop, algorithmic bias -> optimization function, algorithmic bias -> other)
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction)
        - Online (yes or no):
        

        Article Content:
        {article_text}

        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
            ]

        response = self.create_prompt(messages)
        return response