from .taxonomies import Taxonomies
from .results import example_output

taxanomy = '''
{
                    "Discrimination": {
                        "Data bias": [
                        "Gender",
                        "Race",
                        "Sexual Orientation",
                        "Economic"
                        ],
                        "Algorithmic bias": [
                        "Interaction",
                        "Feedback loop",
                        "Optimization function",
                        "Other"
                        ]
                    },
                    "Human Incompetence": {
                        "Administrative": [],
                        "Technical": []
                    },
                    "Pseudoscience": {
                        "Facial": []
                    },
                    "Environmental Impact": {},
                    "Disinformation": {
                        "Textual": [],
                        "Image": [],
                        "Video": [],
                        "Audio": []
                    },
                    "Copyright Violation": {},
                    "Mental Health": {},
                    "Other": {}
                    }

'''
structure = "{ <class>: {<subclass>:{[<sub-subclass>]}} }"

def get_prompt(article_text,prompt_type):
    taxa = Taxonomies()
    if prompt_type == "zero_shot":
        return f"""
        Imagine a computer research institute trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State:
        - City:
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. Let's check if the company recently moved headquarters that is not stated in the article, if so provide the location of the new headquarter):
        - Affected population (let's think about who are the affected demographic and which people are affected): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may leave this blank):
        - Classes of irresponsible AI use (please refer to this taxonomy: {taxa.get_category("class")}, there could be more than one classes the article classifies as. DO NOT CREATE your own class, use the taxonomy list provided.):
        - Subclasses (refer to this taxonomy: {taxa.get_category("subclass")} for subclass. The subclasses should be the children of the "Classes of irresponsible AI use". DO NOT CREATE your own subclass field if it's not in the provided taxonomy list.):
        - Sub-subclass (refer to this taxonomy: {taxa.get_category("subs-subclass")} for the sub-subclass list that are under subclass. Only find the sub-subclass relation in the provided taxonomy. DO NOT ADD sub-subclass fields that are not in the provided taxonomy list.):
        - Area of AI Application:
        - Online (yes or no):
        
        Article Content:

        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content =================
        
        """
    elif prompt_type == "taxonomy_string_formatted":
        return f"""
        Imagine a computer research institute trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        Refer to {example_output} for json output examples.
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State:
        - City:
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected(let's check the article text to see if this information is provided or suggested, if not you may output 'Unknown'):
        - Classes of irresponsible AI use (please refer to this taxonomy: {taxa.get_category("class")}, there could be more than one classes the article classifies as. Let's consider which categories this article incident falls under. DO NOT create your own class, adhere strictly to the provided list.):
        - Subclasses  (refer to this taxonomy list: {taxa.get_category("subclass")} for subclass. DO NOT create your own subclass field if it's not in the provided taxonomy list.):
        - Sub-subclass (refer to this taxonomy list: {taxa.get_category("sub-subclass")} for the sub-subclass list that are under subclass. Only find the sub-subclass relation in the provided taxonomy. DO NOT ADD sub-subclass fields that are not in the provided taxonomy list. LEAVE THE FIELD EMPTY if it's not in the taxonomy example provided.):
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
        
        Article Content:

        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content =================
        """
    
    elif prompt_type == "taxonomy_string":
        return f"""
        Imagine a computer research institute trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        Refer to {example_output} for json output examples.
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State:
        - City:
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please refer to this taxonomy: {taxanomy}, the taxonony is defined as such: taxaonomy = {structure}. There could be more than one classes the article classifies as. DO NOT create your own class, adhere strictly to the provided list.):
        - Subclasses (refer to this taxonomy structure: {taxanomy}, the taxonony is defined as such: taxaonomy = {structure}. The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. DO NOT ADD subclass fields that are NOT in the provided taxonomy list.):
        - Sub-subclass (refer to this taxonomy structure: {taxanomy}, the taxonony is defined as such: taxaonomy = {structure}. Only find the sub-subclass relation in the provided taxonomy. DO NOT ADD sub-subclass fields that are not in the provided taxonomy list. LEAVE THE FIELD EMPTY if it's not in the taxonomy example provided.):
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
        
        Article Content:

        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content =================
        
        """
    elif prompt_type == "tree_of_thoughts":
        return f"""
        Imagine three expert academic researchers trying to categorize and classify a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, the three researchers will fill out the following classifications. Their responses are well-thought-out responses that are well-supported by the article text.
        The experts will share their reasoning for their taxonomy classificaiton of "Classes of irresponsible AI use", and its "subclasses" and sub-subclasses, and compare their results. 
        Each expert will share their thought process in detail, taking into account the previous thoughts of other and admitting any errors. 
        The experts will create a breadth-first search of the tree of probable classifications and will vote on which classification is the most promising and well-supported.
        Refer to {example_output} for json output examples.
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State:
        - City:
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected(let's check the article text to see if this information is provided or suggested, if not you may output 'Unknown'):
        - Classes of irresponsible AI use (Use this taxonomy list strictly: {taxa.get_category("class")}, there could be more than one classes the article classifies as. DO NOT CREATE your own class, use the provided list.):
        - Subclasses  (Use this taxonomy list strictly: {taxa.get_category("subclass")} for subclass. The subclasses should be the children of the "Classes of irresponsible AI use". DO NOT ADD OR CREATE subclass fields that are NOT in the provided taxonomy list.):
        - Sub-subclass (Use this taxonomy list strictly: {taxa.get_category("sub-subclass")} for the sub-subclass list that are under subclass. Only find the sub-subclass relation in the provided taxonomy. DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list.):
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
        
        Article Content:

        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content =================
        """