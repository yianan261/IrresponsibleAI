import os


def check_tokens(base, char_limit=30500):
    flagged = []
    for i in range(1, 639):
        file_path = f"{base}/article_texts/{i}.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            char_count = len(content)
            if char_count > char_limit:
                flagged.append(i)

        except FileNotFoundError:
            print(f"Error: File {i}.txt not found.")

    return flagged


if __name__ == "__main__":
    base = os.path.abspath(os.path.dirname(__file__))
    flagged_files = check_tokens(base)
    print("Flagged files (excessive tokens)", flagged_files)
