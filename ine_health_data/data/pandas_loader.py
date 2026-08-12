import pandas as pd
from pathlib import Path
import logging
import json

# If not modified, this will be the relative path of extraction of the CSV for ESdE Adultos 2023
PATH_ESdE_MICRO_ADULT = Path(r"data\raw\datos_2023\ESdEadulto_2023\CSV\ESdEadulto_2023.tab")

def load_csv_df(
    csv_file_path:Path,
    sep:str = "\t",
    columns: None| list[str] = None    
)-> pd.DataFrame:
    if not csv_file_path.is_file(): raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

    df = pd.read_csv(
        csv_file_path,
        sep=sep,
        usecols=columns,
        dtype="string",
        keep_default_na=False
    )

    return df

    