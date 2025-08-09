import json
import os
import shutil
import sys
import logging

JSON_PATH = 'file_name&title.json'
OUTPUT_LIST_FILENAME = 'book_list.txt'
OUTPUT_DIRECTORY = "outputs"
BOOKS_SOURCE_DIRECTORY = "books"
LOG_FILE = 'app.log'


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, 'w', 'utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def process_book_data(file_path):
    logging.info(f"Reading and processing book data from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as opened_file:
            book_list = json.load(opened_file)
    except FileNotFoundError:
        logging.error(f"Input file not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Could not decode JSON from: {file_path}")
        raise

    book_list.sort(key=lambda x: x.get('title', '').lower())
    logging.info("Book list sorted successfully.")

    indexed_book_list = []
    for i, item in enumerate(book_list, 1):
        new_item = {
            'index': i,
            'title': item.get('title'),
            'file_name': item.get('file_name')
        }
        indexed_book_list.append(new_item)
    logging.info(f"Indexing complete. {len(indexed_book_list)} books indexed.")
    return indexed_book_list


def create_output_files(book_list):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        logging.info(f"Output directory created: {OUTPUT_DIRECTORY}")

    for book in book_list:
        title = book.get("title", "Untitled")
        index = book.get("index")
        file_name = book.get("file_name")

        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        clean_title = title
        for char in invalid_chars:
            clean_title = clean_title.replace(char, ' ')
        clean_title = " ".join(clean_title.split()).strip()

        folder_name = f"{index}. {clean_title}"
        folder_path = os.path.join(OUTPUT_DIRECTORY, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if file_name:
            source_file = os.path.join(BOOKS_SOURCE_DIRECTORY, file_name)
            if os.path.exists(source_file):
                shutil.copy(source_file, folder_path)
                logging.info(f"Copied '{file_name}' to '{folder_path}'")
            else:
                logging.warning(
                    f"Source file not found for book '{title}': {source_file}")

    final_list_path = os.path.join(OUTPUT_DIRECTORY, OUTPUT_LIST_FILENAME)
    logging.info(f"Creating final book list at: {final_list_path}")
    with open(final_list_path, 'w', encoding='utf-8') as written_file:
        json_string = json.dumps(book_list, indent=4, ensure_ascii=False)
        written_file.write(json_string)
    logging.info("Final book list file created successfully.")


def main():
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    setup_logging()
    logging.info("Starting the book processing script.")
    try:
        indexed_books = process_book_data(JSON_PATH)
        create_output_files(indexed_books)
        logging.info("Script finished successfully.")
    except Exception as e:
        logging.critical(
            f"A critical error occurred, and the program had to stop: {e}")


if __name__ == "__main__":
    main()
