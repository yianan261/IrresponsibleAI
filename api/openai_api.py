from openai import OpenAI

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
        prompt = f"""
        Please extract the following information from the news article:
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

        This is the end of a text.

        """

        messages = [{"role": "user", "content":prompt},
                    {"role": "system", "content":"You are a helpful assistant designed to output JSON."}]

        response = self.create_prompt(messages)
        return response
