from openai import OpenAI
import api.prompt_factory as prompt_factory
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

        reasoning = """
        {
            "Country": "Worldwide", reasoning-> Youtube, including Youtube Kids, can be accessed in many countries. Though the incident is reported in the U.S., it doesn't mean the problem is limited to only the U.S..
            "State": "", reasoning-> The incident is nation-wide in the United States, not specific to one state.
            "City": "", reasoning-> The incident is nation-wide in the United States, not specific to one city.
            "Continent": "Worldwide", reasoning-> Youtube, including Youtube Kids, can be accessed in many countries. Though the incident is reported in the U.S., it doesn't mean the problem is limited to only the U.S.; therefore the result should be 'Worldwide' for continent.
            "Company": "Google LLC", reasoning-> Youtube is a subsidiary under Google.
            "Company city": "Mountain View", reasoning-> Youtube is a subsidiary under Google and Google's headquarter is in Mountain View.
            "Company state": "California", reasoning-> Mountain View is a city in the California state.
            "Affected population": "Children on Youtube", reasoning-> The incident affects children on youtube directly.
            "Number of people actually affected": "Unknown", reasoning-> There is no record of an actual number in the article text, we cannot know how many people are directly affected.
            "Number of people potentially affected": "Unknown", reasoning-> There is no record of potential number of people affected in the article, we cannot know how many people are potentially affected.
            "Class of irresponsible AI use": "Disinformation", "Human Incompetence", "Mental Health", "Copyright Violation"], reasoning-> The classes in the taxonomy include "discrimination,human incompetence, psuedoscience, environmental impact, disinformation, copyright violation, mental health".
            We choose "Human Incompetence" because the engineers and administrators behind the platform have not well-regulated the videos, causing such an issue.
            "Mental Health" because the disturbing videos could potentially affect children's mental health.
            "Copyright Violation" because the videos use characters without permission such as Mickey Mouse and Elsa from Disney, and Peppa Pig fakes to portray disturbing acts in videos.
            "Subclasses": {
            "Human Incompetence":["Technical", "Administrative"], reasoning-> The subclasses of 'human incompetence' in the taxonomy example include 'technical' and 'administrative', and both in this case seem to be appropriate tags of this incident because the technically, the channel algorithm should be more robust to filter out inappropriate content for kids, and administratively, better monitoring and regulation of videos should be imposed by Youtube's team to prevent such problems.
            "Mental Health":[], reasoning-> 'Mental health' doesn't have a subclass in the taxonomy, so it should be left empty.
            "Copyright Violation":[], reasoning-> 'Copyright Violation' doesn't have a subclass in the taxonomy, so it should be left empty.
            },
            "Sub-subclass": [], reasoning-> There are no sub-subclasses of the subclasses listed in the taxonomy, therefore this field should be left empty.
            "Area of AI Application": "content filtering", reasoning-> The area of AI application here is content filtering.
            "Online": "Yes", reasoning-> Youtube is an online platform, therefore this incident is in fact an online incident.
        },
        """
        result = """ 
        {
            "Country": "Worldwide",
            "State": "",
            "City": "",
            "Continent": "Worldwide",
            "Company": "Google LLC",
            "Company city": "Mountain View",
            "Company state": "California",
            "Affected population": ["Children on Youtube"],
            "Number of people actually affected": "Unknown",
            "Number of people potentially affected": "Unknown",
            "Class of irresponsible AI use": ["Human Incompetence", "Mental Health", "Copyright Violation"],
            "Subclasses": {
            "Human Incompetence":["Technical", "Administrative"]
            },
            "Sub-subclass": [],
            "Area of AI Application": "content filtering",
            "Online": "Yes"
        }
        """
        prompt = prompt_factory.get_prompt(article_text, prompt_type)

        llm_lingua = PromptCompressor(
            model_name="TheBloke/Llama-2-7b-Chat-GPTQ", device_map="mps"
        )

        compressed_article = llm_lingua.compress_prompt(
            article_text, rate=0.4, force_tokens=["\n", "?"]
        )
        # llm_lingua = PromptCompressor(
        #     model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
        #     use_llmlingua2=True,  # Whether to use llmlingua-2
        # )
        compressed_prompt = llm_lingua.compress_prompt(
            prompt, rate=0.6, force_tokens=["\n", "?"]
        )

        message1 = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        message_with_rules = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "content": reasoning,
            },
            {
                "role": "user",
                "content": "Check if your reasoning makes sense and is supported by the article text. Give your final classification result in JSON format",
            },
            {
                "role": "assistant",
                "content": result,
            },
            {
                "role": "user",
                "content": f"""
             read this article: 
             ====start of article====
             {compressed_article}
             ====end of article ====
             Follow the previous steps 1. provide classification and reasoning 2. give your final classification results in JSON format
             """,
            },
        ]
        messages = message_with_rules
        response = self.create_prompt(messages)
        return response, prompt

    def check_result(self, article_text, result):

        prompt = prompt_factory.get_prompt_for_check(article_text, result)
        messages = [
            {"role": "user", "content": prompt},
            {
                "role": "system",
                "content": "You are a helpful university assistant designed to classify news articles to specific categories.",
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
