from ine_health_data.data.codebook_builder import extract_raw_codebook
from ine_health_data.data.extraction import extract_all_raw_files
from ine_health_data.utils.json_helpers import save_json, load_json
from ine_health_data.data.pandas_loader import load_csv_df_raw

from pathlib import Path
import pandas as pd
import logging

# This is a sloppy solution. Will fix later...
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CODEBOOK_OUTPUT_PATH = (
    PROJECT_ROOT / "references" / "metadata" / "esde_adulto_2023.json"
)
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_ESdE_DIRECTORY = RAW_DATA_DIR / "datos_2023" / "ESdEadulto_2023"
RAW_ESdE_CODEBOOK_PATH = RAW_ESdE_DIRECTORY / "dr_ESdEadulto_2023.xlsx"
RAW_ESdE_MICRODATA_PATH = RAW_ESdE_DIRECTORY / "CSV" / "ESdEadulto_2023.tab"

def start_setup():
    extract_all_raw_files(raw_dir=RAW_DATA_DIR)
    code_dict = extract_raw_codebook(RAW_ESdE_CODEBOOK_PATH)
    save_json(data=code_dict, output_path=CODEBOOK_OUTPUT_PATH)

def load_variables(
    variables: str | list[str],
    codebook_json_path:Path=CODEBOOK_OUTPUT_PATH
)->pd.DataFrame:
    codebook = load_json(codebook_json_path)

    if isinstance(variables,str):
        variables = [variables]

    unkn_var = []
    for var in variables:
        if var not in codebook: unkn_var.append(var)
    if unkn_var:
        raise KeyError(f"Variables not in the ESdE codebook: {unkn_var!r}")

    return load_csv_df_raw(csv_file_path=RAW_ESdE_MICRODATA_PATH, columns=variables)

def add_value_labels(
    df_raw:pd.DataFrame,
    codebook: dict[str, dict]|None =None,
    overwrite: bool = False,
)->pd.DataFrame:
    if codebook is None: 
        codebook = load_json(json_path=CODEBOOK_OUTPUT_PATH)

    df = df_raw.copy()

    for column_name in df.columns:
        variable_metadata = codebook.get(column_name)

        if variable_metadata is None:
            # logging.warning(f"Variable metadata for {column_name} is None")
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

def get_all_variables(
)->list[str]:
    codebook = load_json(json_path=CODEBOOK_OUTPUT_PATH)
    return codebook.keys()

if __name__ == "__main__":
    # start_setup()
    logging.basicConfig(level=logging.DEBUG)

    cols = ["CCAA"] #,"EDADa"
    df:pd.DataFrame = load_csv_df_raw(columns=cols)

    counts_raw = df.value_counts().reset_index() # sort=True,

    codebook = load_json(json_path=CODEBOOK_OUTPUT_PATH)
    df_final = add_value_labels(df_raw=counts_raw,codebook=codebook)

    logging.debug(f"\n{df_final}")