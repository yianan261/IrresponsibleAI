import json

class FormatChecker:

    def check_format(self,result):

        fields = ["Country", 
                "State",
                "City",
                "Continent",
                "Company",
                "Company city",
                "Company state",
                "Affected population", 
                "Number of people actually affected", 
                "Number of people potentially affected", 
                "Classes of irresponsible AI use", 
                "Subclasses",
                "Sub-subclass",
                "Area of AI Application",
                "Online"
                ]
        
        for f in fields:
            if f not in set(result.keys()):
                return False
        return True
