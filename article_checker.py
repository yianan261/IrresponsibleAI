import os
import time
import concurrent.futures


def process_file(file_id_pair):
    file_path, id = file_id_pair
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.readlines()
        line_count = len(file_content)
        word_count = sum(len(line.split()) for line in file_content)

        if line_count < 10:
            flag = "FLAGGED: less than 10 lines"
            return (id, word_count, flag)
        else:
            flag = "OK"
        return (id, word_count, flag)

    except FileNotFoundError:
        return f"Error: {os.path.basename(file_path)} not found"


def concurrent_processor(base):
    flagged = []
    files = [f"{base}/article_texts/{i}.txt" for i in range(1, 639)]
    files_id = zip(files, range(1, 639))
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(process_file, files_id)

        for result in results:
            if isinstance(result, tuple) and "FLAGGED" in result[2]:
                flagged.append(result)
                print(
                    f"File {result[0]}.txt: Words = {result[1]}, Status = {result[2]}"
                )
            elif isinstance(result, str):
                print(result)
    return flagged


def processor(base):
    flagged = []
    for i in range(1, 639):
        file_path = f"{base}/article_texts/{i}.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.readlines()
            line_count = len(file_content)
            word_count = sum(len(line.split()) for line in file_content)

            if line_count < 1:
                flag = "FLAGGED: Less than 1 lines"
                flagged.append((i, word_count))
            else:
                flag = "OK"

            print(
                f"File {i}.txt: Lines = {line_count}, Words = {word_count}, Status = {flag}"
            )

        except FileNotFoundError:
            print(f"Error: File {i}.txt not found.")

    return flagged


def check_articles(base):
    start_time = time.time()
    flagged = processor(base)
    duration = time.time() - start_time
    print(f"Processed in {duration} seconds")
    return flagged


if __name__ == "__main__":
    base = os.path.abspath(os.path.dirname(__file__))
    flagged_files = check_articles(base)
    print("Flagged files", flagged_files)
