import os
import json


class IncidentData:
    def __init__(self):
        self.base = os.path.abspath(os.path.dirname(__file__))

    # get incident ids of 2023
    def get_incidents_2023(self) -> set[str]:
        base = self.base
        print("base", base)
        path_to_file = f"{base}/ids_2023.json"
        with open(path_to_file, "r") as file:
            ids_2023 = json.load(file)
        set_ids_2023 = set(str(i) for i in ids_2023)
        return set_ids_2023

    def get_handpicked_id_set(self) -> set[str]:
        # id_set = set([0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 451, 382, 505, 167])
        id_set = set([1, 9, 167, 382, 505])
        # id_set = set([i for i in range(1,16)])
        id_int_to_string = (str(i) for i in id_set)
        return id_int_to_string
