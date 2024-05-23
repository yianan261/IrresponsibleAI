import os
import json
from format_checker import FormatChecker
import re


def check_result():
    checker = FormatChecker()
    base = os.path.abspath(os.path.dirname(__file__))
    files = [
        "2024_05_17_00_43",
        "2024_05_17_14_20",
        "2024_05_17_15_21",
        "2024_05_17_16_03",
        "2024_05_18_12_06",
        "2024_05_21_00_00",
    ]
    replace = []
    for file in files:
        try:
            file_path = f"{base}/processed_output/ToT_CoT_Multi_turn/processed_results_{file}.json"
            with open(file_path, "r") as json_file:
                file_content = json.load(json_file)
            for k, v in file_content.items():
                if not checker.check_format(v):
                    replace.append(k)

        except FileNotFoundError:
            print(f"File {file} does not exist, skipping...")
            continue

    return replace


def rerun():
    flagged = []
    shorten = []
    issue1 = {
        "29": "Expecting value: line 102 column 12 (char 1612)",
        "19": "Expecting value: line 102 column 12 (char 1612)",
        "88": "Expecting value: line 2 column 112 (char 112)",
        "86": "Expecting value: line 2 column 112 (char 112)",
        "5": "Expecting value: line 2 column 112 (char 112)",
        "11": "Expecting value: line 102 column 12 (char 1612)",
        "20": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 17479 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "12": "Expecting value: line 2 column 112 (char 112)",
    }
    issue2 = {
        "133": "Expecting value: line 102 column 12 (char 1612)",
        "110": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16392 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "136": "Expecting value: line 102 column 12 (char 1612)",
    }
    issue3 = {
        "285": "Expecting value: line 102 column 12 (char 1612)",
        "231": "Unterminated string starting at: line 17 column 9 (char 612)",
        "255": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16456 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "263": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 17186 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "260": "Expecting property name enclosed in double quotes: line 9 column 12 (char 250)",
        "205": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 17493 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "259": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16400 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
    }
    issue4 = {
        "316": "'items'",
        "369": "Expecting value: line 102 column 12 (char 1612)",
    }
    issue5 = {
        "405": "Expecting value: line 2 column 112 (char 112)",
        "420": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16684 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "415": "Expecting value: line 102 column 12 (char 1612)",
        "404": "Expecting value: line 102 column 12 (char 1612)",
    }
    issue6 = {
        "562": "Expecting value: line 102 column 12 (char 1612)",
        "536": "Expecting value: line 3202 column 1 (char 3213)",
        "517": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16826 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "603": "Expecting value: line 2 column 112 (char 112)",
    }
    issue7 = {
        "420": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16541 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
        "133": "Expecting value: line 3202 column 1 (char 3213)",
        "12": "Expecting value: line 2 column 112 (char 112)",
        "86": "Expecting value: line 2 column 112 (char 112)",
        "19": "Expecting value: line 102 column 12 (char 1612)",
        "88": "Expecting value: line 2 column 112 (char 112)",
        "562": "Expecting value: line 102 column 12 (char 1612)",
        "404": "Error code: 400 - {'error': {'message': \"This model's maximum context length is 16385 tokens. However, your messages resulted in 16462 tokens. Please reduce the length of the messages.\", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}",
    }
    issues = [issue7]
    length_error = r"Error code: 400"
    for issue in issues:
        for id, error in issue.items():
            if re.search(length_error, error):
                shorten.append(id)
            flagged.append(id)
    return shorten, flagged


if __name__ == "__main__":
    format_issues = check_result()
    length_issues, agg_issues = rerun()
    all_issues = format_issues + agg_issues
    print("length", length_issues)
    print("agg_issues", agg_issues)
    print("all issues", all_issues)
