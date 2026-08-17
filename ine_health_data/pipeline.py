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
    if not RAW_ESdE_MICRODATA_PATH.is_file() or not RAW_ESdE_CODEBOOK_PATH.is_file():
        logging.debug(f"microdata files not found. Extracting zip file")
        extract_all_raw_files(raw_dir=RAW_DATA_DIR)
    else: 
        logging.info(f"Skipping extraction of adult microdata: {RAW_ESdE_MICRODATA_PATH}")

    code_dict = extract_raw_codebook(RAW_ESdE_CODEBOOK_PATH)
    save_json(data=code_dict, output_path=CODEBOOK_OUTPUT_PATH)

def load_variables(
    variables: str | list[str] | None = None,
    codebook_json_path:Path=CODEBOOK_OUTPUT_PATH
)->pd.DataFrame:
    codebook = load_json(codebook_json_path)

    if variables is not None:
        if isinstance(variables,str):
            variables = [variables]

        unkn_var = []
        for var in variables:
            if var not in codebook: unkn_var.append(var)
        if unkn_var:
            raise KeyError(f"Variables not in the ESdE codebook: {unkn_var!r}")

    df = load_csv_df_raw(csv_file_path=RAW_ESdE_MICRODATA_PATH, columns=variables, keep_na=True)
    for column_name in df.columns:
        variable_metadata = codebook.get(column_name)
        if variable_metadata["Tipo"] == "N":
            df[column_name] = pd.to_numeric(df[column_name],errors="raise")
            logging.debug(f"Converted variable {column_name} to numeric.") 

    return df

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

        if variable_metadata["Tipo"] == "N":
            df[label_column_name] = df[column_name].astype("string").map(value_labels)
        else:
            df[label_column_name] = df[column_name].map(value_labels)

    return df

def is_nonresponse(
    df:pd.DataFrame,
    nona_labels: str | tuple[str,...] = ("No contesta", "No consta", "No aplicable"),
    codebook=None
)->pd.DataFrame:
    """Return a Boolean mask for codebook-defined non-answer responses.

    The returned DataFrame has the same index and columns as ``df``. A cell is
    ``True`` when its raw value maps to one of ``nona_labels`` in that
    variable's codebook; physical missing values remain ``False`` and should
    be identified with :meth:`pandas.DataFrame.isna`. By default, the mask
    includes ``No contesta``, ``No consta``, and ``No aplicable``. Columns not
    present in the codebook are returned as ``False``.
    """
    if codebook is None: 
        codebook = load_json(json_path=CODEBOOK_OUTPUT_PATH)

    if isinstance(nona_labels, str):
        nona_labels = (nona_labels,)   

    new_df = df.copy()

    for column_name in new_df.columns:
        variable_metadata = codebook.get(column_name)
        if variable_metadata is None:
            new_df[column_name] = False
            continue
        
        value_labels = variable_metadata.get("value_labels") or {}

        nonresponse_codes = set()
        for code, label in value_labels.items():
            clean_label = label.strip()
    
            is_selected_label = any(
                clean_label == requested_label
                # This is required due to existing "No aplicable (nunca lo ha intentado)" label
                or clean_label.startswith(f"{requested_label} ")
                for requested_label in nona_labels
            )

            if is_selected_label:
                nonresponse_codes.add(code)

        new_df[column_name] = new_df[column_name].astype("string").isin(
            nonresponse_codes
        )

    return new_df
    
def get_codebook()->map:
    '''Used as getter abstraction for jupyter notebooks.'''
    codebook = load_json(json_path=CODEBOOK_OUTPUT_PATH)
    return codebook

def get_variables_list(
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