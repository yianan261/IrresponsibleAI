class Taxonomies:
    def __init__(self):
        self.population_examples = '[Military,LGBTQ,Student,Facebook Users,African American,Online Female Population,EU Travelers, Twitter Users]'
        self.taxonomy = {
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
                        "Facial": [],
                        "Other":[],
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
        self.classes = """["Discrimination",
                    "Human Incompetence",
                    "Pseudoscience",
                    "Environmental Impact",
                    "Disinformation",
                    "Copyright Violation",
                    "Mental Health",
                    "Other"]
                    """
        self.subclasses =  """
                {
                    "Discrimination": [
                        "Data bias",
                        "Algorithmic bias"
                    ],
                    "Human Incompetence": [
                        "Administrative",
                        "Technical"
                    ],
                    "Pseudoscience": [
                        "Facial",
                        "Other"
                    ],
                    "Environmental Impact":[],
                    "Disinformation": [
                        "Textual",
                        "Image",
                        "Video",
                        "Audio",
                    ],
                    "Copyright Violation": [],
                    "Mental Health": [],
                    "Other": []
                    }
            """
        self.sub_subclasses= """
                    {
                        "Data bias": [
                        "Gender",
                        "Race",
                        "Sexual Orientation",
                        "Economic",
                        "Other"
                        ],
                        "Algorithmic bias": [
                        "Interaction",
                        "Feedback loop",
                        "Optimization function",
                        "Other"
                        ],
                        "Administrative":[],
                        "Technical":[],
                        "Facial": [],
                        "Textual": [],
                        "Image": [],
                        "Video": [],
                        "Audio": []
                    },

                """
        self.structure = "{ <class>: {<subclass>:{[<sub-subclass>]}} }"
        
    def get_category(self,field):
        taxa = self.taxonomy
        result = []
        if field == "class":
            return list(taxa.keys())
        for k,v in taxa.items():
            if field == "subclass":
                result.append(f"{k}(Class)->{list(v.keys())}(subclass list)")
            elif field == "sub-subclass":
                for key,val in taxa[k].items():
                    result.append(f"{key}(Subclass)->{val}(sub-subclass list)")
        return result
    
