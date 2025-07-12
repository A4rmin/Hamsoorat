import os
import glob
import logging
import pandas as pd
from difflib import get_close_matches
from dotenv import load_dotenv

# ===== Load Configuration =====
load_dotenv()

# ===== Logging Setup =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("hamsoorat")

# ===== Helper Functions for Configuration =====

def get_input_file():
    path = os.getenv('XLSX_INPUT')
    if not path:
        raise ValueError("Environment variable 'XLSX_INPUT' not set")
    return path


def get_output_file():
    path = os.getenv('XLSX_OUTPUT')
    if not path:
        raise ValueError("Environment variable 'XLSX_OUTPUT' not set")
    return path


def get_image_dir():
    path = os.getenv('IMAGE_DIR')
    if not path:
        raise ValueError("Environment variable 'IMAGE_DIR' not set")
    return path


def get_image_extensions():
    return os.getenv('IMAGE_EXTENSIONS', 'jpg,jpeg,png,gif').split(',')


def get_fuzzy_threshold():
    try:
        return float(os.getenv('FUZZY_MATCH_THRESHOLD', '0.7'))
    except ValueError:
        raise ValueError("Environment variable 'FUZZY_MATCH_THRESHOLD' must be a float")

# ===== Core Matching Functions =====

def exact_match(key):
    image_dir = get_image_dir()
    for ext in get_image_extensions():
        pattern = os.path.join(image_dir, f"{key}.{ext}")
        matches = glob.glob(pattern)
        if matches:
            logger.debug(f"Exact match found: {matches[0]}")
            return matches[0]
    return None


def fuzzy_match(key, all_files):
    threshold = get_fuzzy_threshold()
    base_names = [os.path.splitext(os.path.basename(f))[0] for f in all_files]
    close = get_close_matches(key, base_names, n=1, cutoff=threshold)
    if close:
        matched_base = close[0]
        for f in all_files:
            if os.path.splitext(os.path.basename(f))[0] == matched_base:
                logger.warning(f"Fuzzy match used: '{key}' → '{matched_base}'")
                return f
    return None


def collect_images():
    image_dir = get_image_dir()
    all_files = []
    for ext in get_image_extensions():
        all_files.extend(glob.glob(os.path.join(image_dir, f"*.{ext}")))
    return all_files

# ===== File I/O Functions =====

def read_input_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        logger.info(f"Reading CSV file: {file_path}")
        return pd.read_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        logger.info(f"Reading Excel file: {file_path}")
        # Use openpyxl for both .xlsx and .xls (accepts xlsx data regardless of extension)
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported input format: {ext}")


def write_output_file(df, file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        logger.info(f"Writing CSV file: {file_path}")
        df.to_csv(file_path, index=False)
    elif ext in ['.xlsx', '.xls']:
        logger.info(f"Writing Excel file: {file_path}")
        # Use openpyxl for both .xlsx and .xls
        df.to_excel(file_path, index=False, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported output format: {ext}")

# ===== Main Execution =====

def main():
    logger.info("Hamsoorat - Name-to-Image Matching Tool Started")

    input_file = get_input_file()
    output_file = get_output_file()

    df = read_input_file(input_file)
    df['pic_path'] = None

    image_files = collect_images()
    logger.info(f"Loaded {len(image_files)} image files from: {get_image_dir()}")

    unmatched = []

    for idx, row in df.iterrows():
        try:
            name = str(row.get('نام', '')).strip()
            surname = str(row.get('نام خانوادگی', '')).strip()
            key = f"{name}-{surname}"

            path = exact_match(key) or fuzzy_match(key, image_files)

            if path:
                df.at[idx, 'pic_path'] = path
                logger.info(f"Matched: {key} → {os.path.basename(path)}")
            else:
                logger.error(f"No match found for: {key}")
                unmatched.append(key)

        except Exception as e:
            logger.exception(f"Error processing row {idx}: {e}")

    write_output_file(df, output_file)

    if unmatched:
        logger.warning("Unmatched entries:")
        for key in unmatched:
            logger.warning(f" - {key}")
    else:
        logger.info("All entries matched successfully.")

if __name__ == '__main__':
    main()
