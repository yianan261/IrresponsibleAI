import json
import os


def get_id_to_title(base):
    file_path = f"{base}incidentsArray.json"
    try:
        with open(file_path, "r") as json_file:
            incidents = json.load(json_file)

        incidents_map = {}
        for i in incidents:
            incidents_map[i.get("incident id")] = i.get("title")
    except Exception as e:
        print(f"an unexpected error {e} occurred")

    return incidents_map


def concat_titles_to_articles():
    base = os.path.abspath(os.path.dirname(__file__))
    incidents_map = get_id_to_title(base)
    articles_file_path = f"{base}/article_texts"
    for i in range(1,639):
        

