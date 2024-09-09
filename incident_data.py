import os
import json


class IncidentData:
    def __init__(self):
        self.base = os.path.abspath(os.path.dirname(__file__))

    # get incident ids of 2023
    def get_incidents_2023(self):
        base = self.base
        path_to_file = f"{base}/ids_2023.json"
        with open(path_to_file, "r") as file:
            ids_2023 = json.load(file)
        set_ids_2023 = set(str(i) for i in ids_2023)
        return set_ids_2023

    def get_handpicked_id_set(self, start: int, end: int):
        id_set = set([num for num in range(start, end + 1)])
        id_int_to_string = set(str(i) for i in id_set)
        return id_int_to_string

    # data that are un-scrapable or too large or incident is missing from AIID database
    def get_empty_data(self):
        to_remove = set(
            [
                21,
                90,
                62,
                44,
                65,
                130,
                247,
                237,
                269,
                338,
                365,
                273,
                342,
                287,
                298,
                375,
                400,
                512,
                522,
                539,
                442,
                552,
                559,
                576,
                542,
            ]
        )
        return set(str(i) for i in to_remove)
