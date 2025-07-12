# Hamsoorat

**Hamsoorat** is a specialized Python tool designed to link member records in spreadsheets to their corresponding image files by matching Persian names and surnames. It is built with the unique characteristics of Persian naming conventions in mind and is intended primarily for Persian-language datasets.

---

## Important Notice: Persian-Specific Tool

This project is **strictly tailored for Persian names and datasets** where the columns `نام` (Name) and `نام خانوادگی` (Surname) exist and the naming patterns follow Persian conventions. It is **not designed to work effectively with datasets in other languages or naming structures.**

If you want a generic name-to-image matching tool for other languages or naming formats, this might not suit your needs without significant modification.

---

## Features

- Reads Persian member data from CSV or Excel files containing `نام` and `نام خانوادگی` columns.
- Scans an image directory with configurable extensions (jpg, jpeg, png, gif).
- Matches records using concatenated Persian `name-surname` keys.
- Attempts exact filename matching first, then falls back to fuzzy matching using Python’s difflib with a configurable similarity threshold.
- Outputs an augmented spreadsheet with a new `pic_path` column linking matched images.
- Comprehensive logging of progress, exact and fuzzy matches, and unmatched entries.
- Built to handle messy Persian datasets with possible typos or filename inconsistencies.

---

## Requirements

- Python 3.7+
- pandas
- openpyxl
- python-dotenv

---

## Setup

1. Clone the repository.

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following environment variables:

   ```
   XLSX_INPUT=path/to/input.csv   # Persian data file with 'نام' and 'نام خانوادگی' columns
   XLSX_OUTPUT=path/to/output.csv
   IMAGE_DIR=path/to/images
   IMAGE_EXTENSIONS=jpg,jpeg,png,gif
   FUZZY_MATCH_THRESHOLD=0.7
   ```

---

## Usage

Run the script:

```bash
python hamsoorat.py
```

The script will:

* Load Persian member data from the specified spreadsheet.
* Collect images from the configured directory.
* For each record, attempt exact then fuzzy filename match on the combined `نام-نام خانوادگی` key.
* Append the matched image path to a new `pic_path` column.
* Save the output file.
* Log unmatched records with warnings.

---

## Code Overview

* Reads configuration from environment variables.
* Uses `glob` to list image files by extensions.
* Performs exact matching by filename with the pattern `name-surname.ext`.
* Falls back to fuzzy matching using `difflib.get_close_matches` with a configurable similarity cutoff.
* Supports CSV and Excel input/output using `pandas` and `openpyxl`.
* Uses Python’s logging module with timestamps and severity levels.
* Catches and logs exceptions per row to ensure the process continues.

---

## Limitations and Notes

* The tool **only works reliably for Persian names** and requires the input data to have columns exactly named `نام` and `نام خانوادگی`.
* It assumes image files are named following the pattern `name-surname.extension` (e.g., `علی-رضایی.jpg`).
* Fuzzy matching threshold may require tuning depending on your dataset quality.
* Not designed for multilingual datasets or Western naming conventions.
* Does not currently support nested image directories.

---

## Future Improvements

* Support recursive/nested image directories.
* Parallelize image scanning and matching for performance on large datasets.
* Develop a simple UI for non-technical users.
* Generate summary reports highlighting unmatched or ambiguous records.

---

## Testing

Run tests if available:

```bash
pytest
```

---

### Summary

**Hamsoorat is a Persian-centric name-to-image matcher — it works best on Persian-language datasets with the expected naming patterns. Use it only if your data and image filenames follow these conventions.**
