import json
import os


def get_id_to_title(base):
    """
    Reads a JSON file containing incident data and constructs a dictionary
    mapping incident IDs to titles, with each title prefixed by "ARTICLE TITLE: ".

    Parameters:
    - base (str): The base directory path where the JSON file is located.

    Returns:
    - dict: A dictionary mapping each incident ID to its corresponding prefixed title.
            If the file is not found or an error occurs, an empty dictionary is returned.

    Raises:
    - Exception: An exception is raised and caught internally if the JSON file cannot
                 be read or parsed, with an error message printed to the console.
    """
    file_path = f"{base}/incidentsArray.json"
    try:
        with open(file_path, "r") as json_file:
            incidents = json.load(json_file)

        incidents_map = {}
        for i in incidents:
            title = "ARTICLE TITLE: " + i.get("title", "")
            incidents_map[i.get("incident id")] = title
    except Exception as e:
        print(f"an unexpected error {e} occurred")

    return incidents_map


def concat_titles_to_articles(base, incidents_map):
    """
    Iterates over a range of IDs and attempts to prepend a title from the incidents_map
    to the content of each corresponding text file in the directory '/article_texts/'.

    Parameters:
    - base (str): The base directory path for the script execution context.
    - incidents_map (dict): A dictionary containing incident IDs as keys and titles as values.

    Raises:
    - IOError: If a file cannot be opened, read, or written, the error is caught and
               an error message is printed.
    - Exception: Catches and logs unexpected errors that may occur during file handling.
    """

    for i in range(1, 639):
        article_file_path = f"{base}/article_texts/{i}.txt"
        if not os.path.exists(article_file_path):
            print(f" file with id {i} doesn't exist, skipping")
            continue
        try:
            with open(article_file_path, "r") as file:
                content = file.read()
            title = incidents_map.get(i)
            if title:
                updated_content = title + "\n" + content
                with open(article_file_path, "w") as file:
                    file.write(updated_content)
                print(f"Updated file with id {i}")
            else:
                print(f"no title found for id {i}, file not updated")

        except IOError as e:
            print(f"Failed to update id {i}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred with id {i}: {e}")


if __name__ == "__main__":
    base = os.path.abspath(os.path.dirname(__file__))
    incidents_map = get_id_to_title(base)
    concat_titles_to_articles(base, incidents_map)
