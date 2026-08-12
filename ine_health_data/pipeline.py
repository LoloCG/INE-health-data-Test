from data.codebook_builder import extract_raw_codebook
from data.extraction import extract_all_raw_files
from utils.json_helpers import save_json, load_json

from pathlib import Path

CODEBOOK_OUTPUT_PATH = Path(r"references\metadata\esde_adult_2023")


def start_setup():
    extract_all_raw_files()

    code_dict = extract_raw_codebook()
    save_json(data=code_dict, output_path=CODEBOOK_OUTPUT_PATH)

    return