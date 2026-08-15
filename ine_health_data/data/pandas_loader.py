import pandas as pd
from pathlib import Path
import logging
import json

# If not modified, this will be the relative path of extraction of the CSV for ESdE Adultos 2023
PATH_ESdE_MICRO_ADULT = Path(r"data\raw\datos_2023\ESdEadulto_2023\CSV\ESdEadulto_2023.tab")

def load_csv_df_raw(
    csv_file_path:Path=PATH_ESdE_MICRO_ADULT, # Not sure if the function should remain path agnostic...
    sep:str = "\t",
    columns: None| list[str] = None,
    keep_na: bool|None = True
)-> pd.DataFrame:
    '''
        columns should be written as per "Variable" described in codebook sheet.        
    '''
    if not csv_file_path.is_file(): raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    df = pd.read_csv(
        csv_file_path,
        sep=sep,
        usecols=columns,
        dtype="string",
        keep_default_na=keep_na,
    )

    return df

