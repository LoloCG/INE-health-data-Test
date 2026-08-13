from data.codebook_builder import extract_raw_codebook
from data.extraction import extract_all_raw_files
from utils.json_helpers import save_json, load_json
from data.pandas_loader import load_csv_df_raw

from pathlib import Path
import pandas as pd
import logging

CODEBOOK_OUTPUT_PATH = Path(r"references\metadata\esde_adult_2023.json")

def start_setup():
    extract_all_raw_files()
    code_dict = extract_raw_codebook()
    save_json(data=code_dict, output_path=CODEBOOK_OUTPUT_PATH)

    return

def add_value_labels(
    df_raw:pd.DataFrame,
    codebook: dict[str, dict],
    overwrite: bool = False,
)->pd.DataFrame:
    df = df_raw.copy()

    for column_name in df.columns:
        variable_metadata = codebook.get(column_name)

        if variable_metadata is None:
            logging.warning(f"Variable metadata for {column_name} is None")
            continue

        value_labels = variable_metadata.get("value_labels")
        if not value_labels:
            continue


        label_column_name = f"{column_name}_label"

        if label_column_name in df.columns and not overwrite:
            raise ValueError(
                f"Column '{label_column_name}' already exists. "
                "Choose another suffix or set overwrite=True."
            )
        
        df[label_column_name] = df[column_name].map(value_labels)

    return df

if __name__ == "__main__":
    # start_setup()
    logging.basicConfig(level=logging.DEBUG)

    cols = ["CCAA"] #,"EDADa"
    df:pd.DataFrame = load_csv_df_raw(columns=cols)

    counts_raw = df.value_counts().reset_index() # sort=True,

    codebook = load_json(json_path=CODEBOOK_OUTPUT_PATH)
    df_final = add_value_labels(df_raw=counts_raw,codebook=codebook)

    logging.debug(f"\n{df_final}")