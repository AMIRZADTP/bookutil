# Book Organizer Utility

This Python script organizes a collection of digital books into a structured directory hierarchy based on their titles.

## Description

The script reads a list of book titles and their corresponding filenames from a JSON file. It then sorts the books by title, creates a numbered folder for each book, and copies the book file into its respective folder. This is useful for creating a clean, organized, and browseable library of digital books.

## Features

-   Sorts books alphabetically by title.
-   Creates a numbered directory for each book (e.g., `1. Book Title`).
-   Handles titles with special characters and non-English languages.
-   Copies book files into their respective directories.

## File Structure

The project expects the following file structure:

```
.
├── Books/
│   ├── book1.pdf
│   └── book2.epub
├── BooksUtil.py
├── file_name&title.json
└── ...
```

-   `BooksUtil.py`: The main script to run.
-   `file_name&title.json`: The input JSON file containing the book metadata.
-   `Books/`: A directory containing all the source book files.

## How to Use

1.  **Prerequisites**:
    -   Ensure you have Python 3 installed.
    -   No external libraries are required.

2.  **Prepare your data**:
    -   Create a directory named `Books` and place all your book files inside it.
    -   Create a JSON file named `file_name&title.json` in the root directory. This file should contain a list of objects, with each object having a `title` and a `file_name` key.

    **Example `file_name&title.json`:**
    ```json
    [
      {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "file_name": "hitchhiker.pdf"
      },
      {
        "title": "The Lord of the Rings",
        "file_name": "lotr.epub"
      }
    ]
    ```

3.  **Run the script**:
    Execute the script from your terminal:
    ```bash
    python3 BooksUtil.py
    ```

## Output

After the script runs, you will find a new directory named `outputs` in the root of the project. This directory will contain a set of numbered folders, each corresponding to a book from your JSON file.

```
.
├── outputs/
│   ├── 1. The Hitchhiker's Guide to the Galaxy/
│   │   └── hitchhiker.pdf
│   └── 2. The Lord of the Rings/
│       └── lotr.epub
└── ...
```

The script will also create an `output_raw_data.txt` file, which contains the sorted and indexed list of your books in JSON format.
