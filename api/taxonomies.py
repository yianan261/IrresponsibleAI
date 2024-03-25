class Taxonomies:
    def __init__(self):
        self.population_examples = ["Military","LGBTQ","Student","Facebook Users","African American","Online Female Population","EU Travelers", "Twitter Users"]
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
    
