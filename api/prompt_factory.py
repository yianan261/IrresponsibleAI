from .taxonomies import Taxonomies
from .results import *

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
        Imagine a computer researcher trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        1. Fill out the following fields:
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State (if not applicable leave blank):
        - City (if not applicable leave blank):
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Company state (the state of the company city, if applicable, if not leave blank):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please follow the rules and refer to this taxonomy: 
                {taxa.classes}    
        Rule1: There could be more than one classes the article classifies as. 
        Rule2: DO NOT create your own class, adhere strictly to the provided list.
        - Subclasses (please follow the rules and refer to this taxonomy structure: 
                 {taxa.subclasses}
        Rule1 : The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. 
        Rule2: DO NOT ADD subclass fields that are NOT in the provided taxonomy list
        Rule3: If there is no subclass for a particular class in the taxonomy, leave it.
                - Sub-subclass (please follow the rules and refer to this taxonomy structure: 
               {taxa.sub_subclasses}
        , the taxonony is defined as such: {taxa.structure}. 
        Rule1: Only find the sub-subclass relation in the provided taxonomy. 
        Rule2: DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list. 
        Rule3: If a subclass in the taxonomy does not have a sub-subclass, leave it.
        Rule4: If none of the subclasses have sub-subclasses, just leave the field empty e.g. sub-subclass:[]
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):

        Article Content:
        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content ===================
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
    elif prompt_type == "few_shots_CoT_prompt":
        return f"""
        Imagine a computer researcher trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        1. Take a look at this taxonomy {taxanomy} provided by the professor, and take a close look at this these examples:
        ==============start of example 1===============
        step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_1}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_1}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_1}
        ```end of output example```
        ==============end of example 1=================

        ==============start of example 2===============
         step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_6}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_6}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_6}
        ```end of output example```
        ============== end of example 2=================

        2. Your task is mainly this part. You have to fill out the following fields according to the article content by reasoning like the examples given, and your output should follow the example output format. DO NOT make up your own fields:
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State (if not applicable leave blank):
        - City (if not applicable leave blank):
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Company state (the state of the company city, if applicable, if not leave blank):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please follow the rules and refer to this taxonomy: 
                {taxa.classes}    
        Rule1: There could be more than one classes the article classifies as. 
        Rule2: DO NOT create your own class, adhere strictly to the provided list.
        - Subclasses (please follow the rules and refer to this taxonomy structure: 
                 {taxa.subclasses}
        Rule1 : The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. 
        Rule2: DO NOT ADD subclass fields that are NOT in the provided taxonomy list
        Rule3: If there is no subclass for a particular class in the taxonomy, leave it.
                - Sub-subclass (please follow the rules and refer to this taxonomy structure: 
               {taxa.sub_subclasses}
        , the taxonony is defined as such: {taxa.structure}. 
        Rule1: Only find the sub-subclass relation in the provided taxonomy. 
        Rule2: DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list. 
        Rule3: If a subclass in the taxonomy does not have a sub-subclass, leave it.
        Rule4: If none of the subclasses have sub-subclasses, just leave the field empty e.g. sub-subclass:[]
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):

       REMEMBER, only use these classification fields 
        [Country, 
        State,
        City,
        Continent,
        Company,
        Company city,
        Company state,
        Affected population, 
        Number of people actually affected, 
        Number of people potentially affected, 
        Classes of irresponsible AI use, 
        Subclasses,
        Sub-subclass,
        Area of AI Application,
        Online
        ].
        DO NOT make up your own field. DO NOT use fields that are not in the list. DO NOT USE example 1 and example 2 output on different articles.

        Article Content:
        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content ===================
        
        """
    elif prompt_type == "tree_of_thoughts":
        return f"""
        Imagine three expert academic researchers trying to categorize and classify a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, the three researchers will fill out the following classifications. Their responses are well-thought-out responses that are well-supported by the article text.
        The experts will share their reasoning for their taxonomy classificaiton of "Classes of irresponsible AI use", and its "subclasses" and sub-subclasses, and compare their results. 
        Each expert will share their thought process in detail, taking into account the previous thoughts of other and admitting any errors. 
        The experts will create a breadth-first search of the tree of probable classifications and will vote on which classification is the most promising and well-supported.
        Given the aggregated news article texts on relevant incidents, the experts will reach a consensus on how an incident should be classified according to the following format.
        
        1. The experts will take look at this taxonomy {taxanomy}, and take a close look at this these examples already reasoned and classified by previous research experts:
        ==============start of example 1===============
        step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_1}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_1}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_1}
        ```end of output example```
        ==============end of example 1=================

        2. The experts will focus mainly on this part. They have to each fill out the following fields by their reasoning and return an agreed upon result as json output from the article content. The experts CANNOT make up their own fields:
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State (if not applicable leave blank):
        - City (if not applicable leave blank):
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Company state (the state of the company city, if applicable, if not leave blank):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please follow the rules and refer to this taxonomy: 
                {taxa.classes}    
        Rule1: There could be more than one classes the article classifies as. 
        Rule2: DO NOT create your own class, adhere strictly to the provided list.
        - Subclasses (please follow the rules and refer to this taxonomy structure: 
                 {taxa.subclasses}
        Rule1 : The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. 
        Rule2: DO NOT ADD subclass fields that are NOT in the provided taxonomy list
        Rule3: If there is no subclass for a particular class in the taxonomy, leave it.
                - Sub-subclass (please follow the rules and refer to this taxonomy structure: 
               {taxa.sub_subclasses}
        , the taxonony is defined as such: {taxa.structure}. 
        Rule1: Only find the sub-subclass relation in the provided taxonomy. 
        Rule2: DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list. 
        Rule3: If a subclass in the taxonomy does not have a sub-subclass, leave it.
        Rule4: If none of the subclasses have sub-subclasses, just leave the field empty e.g. sub-subclass:[]
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
    
        REMEMBER, only use these classification fields: 
        [Country, 
        State,
        City,
        Continent,
        Company,
        Company city,
        Company state,
        Affected population, 
        Number of people actually affected, 
        Number of people potentially affected, 
        Classes of irresponsible AI use, 
        Subclasses,
        Sub-subclass,
        Area of AI Application,
        Online
        ].
        DO NOT make up your own field. DO NOT use fields that are not in the list.

        Article Content:
        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content ===================
        """
    elif prompt_type == "few_shots":
        return f"""
        Imagine a computer researcher trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        1. Take a look at this taxonomy {taxanomy} provided by the professor, and take a close look at this these examples:
         ==============start of example 1===============
        step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_1}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_1}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_1}
        ```end of output example```
        ==============end of example 1=================

        2. Your task is mainly this part. You have to fill out the following fields according to the article content by reasoning like the examples given, and your output should follow the example output format. DO NOT make up your own fields:
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State (if not applicable leave blank):
        - City (if not applicable leave blank):
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Company state (the state of the company city, if applicable, if not leave blank):
        - Affected population (e.g.{taxa.population_examples},let's think about who are the affected demographic and which people are affected, it need not necessarily be from this list): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please follow the rules and refer to this taxonomy: 
                {taxa.classes}    
        Rule1: There could be more than one classes the article classifies as. 
        Rule2: DO NOT create your own class, adhere strictly to the provided list.
        - Subclasses (please follow the rules and refer to this taxonomy structure: 
                 {taxa.subclasses}
        Rule1 : The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. 
        Rule2: DO NOT ADD subclass fields that are NOT in the provided taxonomy list
        Rule3: If there is no subclass for a particular class in the taxonomy, leave it.
        - Sub-subclass (please follow the rules and refer to this taxonomy structure: 
               {taxa.sub_subclasses}
        , the taxonony is defined as such: {taxa.structure}. 
        Rule1: Only find the sub-subclass relation in the provided taxonomy. 
        Rule2: DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list. 
        Rule3: If a subclass in the taxonomy does not have a sub-subclass, leave it.
        Rule4: If none of the subclasses have sub-subclasses, just leave the field empty e.g. sub-subclass:[]
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):

        REMEMBER, only use these classification fields 
        [Country, 
        State,
        City,
        Continent,
        Company,
        Company city,
        Company state,
        Affected population, 
        Number of people actually affected, 
        Number of people potentially affected, 
        Classes of irresponsible AI use, 
        Subclasses,
        Sub-subclass,
        Area of AI Application,
        Online
        ].
        DO NOT make up your own field. DO NOT use fields that are not in the list.

        Article Content:
        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content ===================
        
        """
    elif prompt_type == "few_shots_CoT_steps":
        return f"""
        Imagine a computer researcher trying to categorize a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, please extract the following information, your responses should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        1. Take a look at this taxonomy
        ```taxonomy
          {taxanomy}
        ```, 
        and take a close look at this these examples:
        ==============start of example 1===============
        step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_1}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_1}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_1}
        ```end of output example```
        ==============end of example 1=================

        ==============start of example 2===============
         step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_6}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_6}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_6}
        ```end of output example```
        ============== end of example 2=================

        2. Your task is mainly this part. You have to fill out the following fields according to the article content using the three steps above:
        STEP 1: Read the article text:
        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content ===================
        STEP 2: State your reason for your classifications for the following:
        =================Classification Fields====================
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State (if not applicable leave blank):
        - City (if not applicable leave blank):
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Company state (the state of the company city, if applicable, if not leave blank):
        - Affected population (let's think about which groups of people are directly affected by the incident in the article.): 
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please follow the rules and refer to this taxonomy: 
        ```taxonomy classes
                {taxa.classes} 
        ```   
        Rule1: There could be more than one classes the article classifies as. 
        Rule2: DO NOT create your own class, adhere strictly to the provided list.
        - Subclasses (please follow the rules and refer to this taxonomy structure `<class>:[<subclass>]`):
          ```taxonomy subclasses       
                 {taxa.subclasses}
          ```
        Rule1 : The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. 
        Rule2: DO NOT ADD subclass fields that are NOT in the provided taxonomy list
        Rule3: If there is no subclass for a particular class in the taxonomy, leave it.
        - Sub-subclass (please follow the rules and refer to this taxonomy structure `<subclass>:[<sub-subclass>]`): 
        ```taxonomy structure
               {taxa.sub_subclasses}
        ```
        Rule1: Only find the sub-subclass relation in the provided taxonomy. The sub-subclass are children of subclass.
        Rule2: DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list. 
        Rule3: If a subclass in the taxonomy does not have a sub-subclass, leave it.
        Rule4: If none of the subclasses have sub-subclasses, just leave the field empty e.g. sub-subclass:[]
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
        =================Classification Fields====================
        STEP 3: Make sure your classification output follows such format:
        ```THIS IS AN EXAMPLE```
        {example_output_id_6}
        ```END OF EXAMPLE```
        
        DO NOT make up your own field. DO NOT use fields that are not in the list. DO NOT USE example 1 and example 2 output on different articles.

        return your classification output in JSON.
        """
    elif prompt_type == "ToT_CoT":
        return f"""
        Imagine three expert academic researchers trying to categorize and classify a list of incidents of irresponsible use of artificial intelligence technology.    
        Given the aggregated news article texts on relevant incidents, the three researchers will fill out the following classifications. Their responses are well-thought-out responses that are well-supported by the article text.
        The experts will share their reasoning for all their classifications.
        Each expert will share their thought process in detail, taking into account the previous thoughts of other and admitting any errors. 
        The experts will create a breadth-first search of the tree of probable classifications and will vote on which classification is the most promising and well-supported.
        Given the aggregated news article texts on relevant incidents, please extract the following information, the response should be well thought-out and well-supported by the content of the articles, please also follow instructions of this prompt.
        1. The experts will take a look at this taxonomy:
        ```taxonomy
          {taxanomy}
        ```, and take a close look at this these examples:
        ==============start of example 1===============
        step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_1}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_1}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_1}
        ```end of output example```
        ==============end of example 1=================

        ==============start of example 2===============
         step 1. Read article text. For an example article such as: 
        ```start of example article 1```
        {example_article_id_6}
        ```end of example article 1```
        step 2. Reason for the classifications: 
        Here is the reasoning for its classifications:
        ```start of response reasoning```
        {example_output_explanation_id_6}
        ```end of response reasoning```
        step 3. generate expected output 
        ```start of output example```
        {example_output_id_6}
        ```end of output example```
        ============== end of example 2=================

        2. Each expert's task is mainly this part. The experts each have to fill out the following fields according to the article content following the steps below:
        STEP 1: Read the article text:
        ================== Start of Article Content =================
        {article_text}
        ================== End of Article Content ===================
        STEP 2: State your reason for your classifications for the following:
        =================Classification Fields====================
        - Country (output "Worldwide" if the incident happened across multiple countries):
        - State (if not applicable leave blank):
        - City (if not applicable leave blank):
        - Continent (output "Worldwide" if the incident happened across multiple countries):
        - Company (i.e. the company that developed the technology involved in this incident):
        - Company city (the city where the headquarters of this company is located. If the company recently moved headquarters, please use the location of the new headquarter):
        - Company state (the state of the company city, if applicable, if not leave blank):
        - Affected population (let's think about which groups of people are directly affected by the incident in the article):
        - Number of people actually affected (let's check the number of people directly affected according to the article. Give a total number. If unknown output 'Unknown'):
        - Number of people potentially affected (let's check the article text to see if this information is provided or suggested, if not you may ouput 'Unknown'):
        - Classes of irresponsible AI use (please follow the rules and refer to this taxonomy: 
        ```taxonomy classes
                {taxa.classes} 
        ```   
        Rule1: There could be more than one classes the article classifies as. 
        Rule2: DO NOT create your own class, adhere strictly to the provided list.
        - Subclasses (please follow the rules and refer to this taxonomy structure `<class>:[<subclass>]`):
          ```taxonomy subclasses       
                 {taxa.subclasses}
          ```
        Rule1 : The subclasses should be the children of the classes. Let's think about which sub-categories of the class/classes this article belong in. 
        Rule2: DO NOT ADD subclass fields that are NOT in the provided taxonomy list
        Rule3: If there is no subclass for a particular class in the taxonomy, leave it.
        - Sub-subclass (please follow the rules and refer to this taxonomy structure `<subclass>:[<sub-subclass>]`): 
        ```taxonomy structure
               {taxa.sub_subclasses}
        ```
        Rule1: Only find the sub-subclass relation in the provided taxonomy. The sub-subclass are children of subclass.
        Rule2: DO NOT ADD OR CREATE sub-subclass fields that are not in the provided taxonomy list. 
        Rule3: If a subclass in the taxonomy does not have a sub-subclass, leave it.
        Rule4: If none of the subclasses have sub-subclasses, just leave the field empty e.g. sub-subclass:[]
        - Area of AI Application (e.g. content filtering, surveillance, illness prediction):
        - Online (yes or no):
        =================Classification Fields====================
        STEP 3: Share results with other experts and decide on the most promising and well-reasoned classification for each field.
        STEP 4: Can you confirm the "class", "subclass", and "sub-subclass" of your final classification you are listed in the taxonomy here?
        ```taxonomy
        {taxanomy}
        ```
        If not, remove anything that is not in the taxonomy.
        STEP 5: Make sure the final classification output follows such format:
        ```THIS IS AN EXAMPLE```
        {example_output_id_6}
        ```END OF EXAMPLE```

        DO NOT make up your own field. DO NOT use fields that are not in the list. DO NOT USE example 1 and example 2 output on different articles.

        return your classification output in JSON.
        """
def get_prompt_for_check(article_text,result):
    taxa = Taxonomies()
    
    return f"""
            Check if this classification for the following article makes sense:
            Step 1: Read the article
            Article Content:
            ================== Start of Article Content =================
            {article_text}
            ================== End of Article Content ===================
            Step 2: Check the initial classification result, do you see any immediate issue with the classification?
            ================== Initial Classification ===================
            {result}
            ====================End of Classification====================
            Step 3: Check the "Affected Population" field, reason how it should be classified according to the article. Compare with the initial classification, are they close? are they different? If they are quite different and unrelated, note it is a problem.
            Step 4: Check the "Class", "Subclass", "Subsubclass", do they follow the taxonomy structure here:
            =====================TAXONOMY====================
            {taxa}
            ======================TAXONOMY===================
            The taxonomy hierarchy should be like this:
            ```taxonomy hierarchy```
            {structure}
            ```taxonomy hierarchy```
            Is the classification only using fields in the taxonomy? if not, note it is a problem.
            If there is no significant problem with the classification, return False.
            If you feel the initial classification is not accurate, return True.
            """
