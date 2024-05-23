import json


class FormatChecker:

    def check_format(self, results):

        fields = [
            "Country",
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
            "Class of irresponsible AI use",
            "Subclasses",
            "Subclasses",
            "Sub-subclass",
            "Area of AI Application",
            "Online",
        ]

        for f in results.keys():
            if f not in set(fields):
                return False
        return True
