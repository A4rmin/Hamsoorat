Hamsoorat

A Python-based name-to-image matching tool built to streamline the process of linking member records to their photos. Originally created to solve a real-world problem—messy image folders and a mismatched spreadsheet—this script has evolved into a reusable, cross-platform utility.

Features

Read member data from CSV or Excel files

Scan a directory of images (jpg, jpeg, png, gif)

Exact filename matching by name-surname key

Fuzzy matching to handle typos and filename variations

Configurable image extensions and fuzzy-match threshold

Detailed logs for matches, fallbacks, and unmatched entries

Output spreadsheet augmented with a pic_path column

Prerequisites

Python 3.7+

pandas

openpyxl

python-dotenv

Installation

Clone the repository

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Add a .env file:

XLSX_INPUT=path/to/input.csv   # or .xlsx
XLSX_OUTPUT=path/to/output.csv # or .xlsx
IMAGE_DIR=path/to/images
IMAGE_EXTENSIONS=jpg,jpeg,png,gif
FUZZY_MATCH_THRESHOLD=0.8

Usage

python hamsoorat.py

The script will:

Load records from the spreadsheet

Collect image files

Match each name-surname to an image (exact then fuzzy)

Fill the pic_path column

Save the output file

Log any unmatched entries

Testing

Run pytest to validate exact matches, fuzzy logic, file collection, and I/O:

pytest

Author Skills

Python scripting and automation

File system operations and batch processing

Fuzzy matching algorithms

Configurable, environment-driven code design

Cross-platform compatibility

Future Improvements

Support nested directories

Add parallel processing for large datasets

Build a lightweight UI for non-technical users

Generate a review report for unmatched entries

License

MIT License

