import json
import os
import sys

json_path = 'file_name&title.json'
output_txt_file = 'output_raw_data.txt'
output_directory = "outputs"


def json_processor():
    os.path.exists(json_path)

    with open(json_path, 'r', encoding='utf-8') as opened_file:
        json_data = json.load(opened_file)

    with open(output_txt_file, 'w', encoding='utf-8') as written_file:
        json_string = json.dumps(json_data, indent=4, ensure_ascii=False)
        written_file.write(json_string)
    return json_data


def folder_creation(json_data):
    main_output_path = output_directory
    duplicate_output_path = os.path.join(main_output_path, "!Duplicates")

    if not os.path.exists(main_output_path):
        os.makedirs(main_output_path)

    if not os.path.exists(duplicate_output_path):
        os.makedirs(duplicate_output_path)
        print(
            f"Created a dedicated folder for duplicates: {duplicate_output_path}")

    for item in json_data:
        title = item.get("title")

        if title:
            folder_name = "".join(c for c in title if c.isalnum()
                                  or c in (' ', '.', '_')).rstrip()

            folder_path = os.path.join(main_output_path, folder_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
            else:
                duplicate_folder_path = os.path.join(
                    duplicate_output_path, folder_name)

                counter = 1
                while os.path.exists(duplicate_folder_path):
                    duplicate_folder_path = os.path.join(
                        duplicate_output_path, f"{folder_name}_{counter}")
                    counter += 1

                os.makedirs(duplicate_folder_path)
                print(
                    f"Folder '{folder_name}' already exists. New created in '!Duplicates' folder: {duplicate_folder_path}")


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
