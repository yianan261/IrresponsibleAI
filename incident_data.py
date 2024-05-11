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

    def get_handpicked_id_set(self):
        # id_set = set([0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 451, 382, 505, 167])
        # id_set = set([1, 14, 9, 4, 10, 3, 505])
        # id_set = set([3])
        id_set = set([i for i in range(101, 201)])
        # id_set = set([494, 560, 602])
        id_int_to_string = set(str(i) for i in id_set)
        return id_int_to_string

    # data that are un-scrapable or too large or incident is missing from AIID database
    def get_empty_data(self):
        to_remove = set(
            [90, 62, 44, 65, 130, 273, 287, 298, 375, 400, 522, 539, 552, 559, 576]
        )
        return set(str(i) for i in to_remove)
