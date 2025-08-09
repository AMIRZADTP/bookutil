import json
import os
import shutil
import sys

json_path = 'file_name&title.json'
output_txt_file = 'output_raw_data.txt'
output_directory = "outputs"
books_source_directory = "Books"


def json_processor():
    os.path.exists(json_path)

    with open(json_path, 'r', encoding='utf-8') as opened_file:
        json_data = json.load(opened_file)

    json_data.sort(key=lambda x: x.get('title', '').lower())

    indexed_data = []
    for i, item in enumerate(json_data, 1):
        new_item = {'index': i, 'title': item.get(
            'title'), 'file_name': item.get('file_name')}
        indexed_data.append(new_item)

    with open(output_txt_file, 'w', encoding='utf-8') as written_file:
        json_string = json.dumps(
            indexed_data, indent=4, ensure_ascii=False)
        written_file.write(json_string)
    return indexed_data


def folder_creation(json_data):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for item in json_data:
        title = item.get("title")
        index = item.get("index")

        if title:
            invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            clean_title = title
            for char in invalid_chars:
                clean_title = clean_title.replace(char, ' ')

            clean_title = " ".join(clean_title.split()).rstrip()
            folder_name = f"{index}. {clean_title}"

            folder_path = os.path.join(output_directory, folder_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")

            source_file = os.path.join(
                books_source_directory, item.get("file_name"))
            if os.path.exists(source_file):
                shutil.copy(source_file, folder_path)
                print(f"Copied '{item.get('file_name')}' to '{folder_path}'")
            else:
                print(
                    f"Error: Source file not found - {source_file}")


def main():
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    try:
        processed_json = json_processor()
        folder_creation(processed_json)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from '{json_path}'. Ensure it's a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
