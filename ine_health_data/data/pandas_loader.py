import pandas as pd
from pathlib import Path
import logging
import json

# If not modified, this will be the relative path of extraction of the CSV for ESdE Adultos 2023
PATH_ESdE_MICRO_ADULT = Path(r"data\raw\datos_2023\ESdEadulto_2023\CSV\ESdEadulto_2023.tab")
PATH_ESdE_CODEBOOK = Path(r"references\metadata\esde_adult_2023.json")

def load_csv_df(
    csv_file_path:Path,
    sep:str = "\t",
    columns: None| list[str] = None    
)-> pd.DataFrame:
    if not csv_file_path.is_file(): raise FileNotFoundError(f"Archivo CSV no encontrado: {csv_file_path}")

    df = pd.read_csv(
        csv_file_path,
        sep=sep,
        usecols=columns
        # TODO: dtype needs to use a lookfor for a dictionary obtained from the metadata excel provided by the INE
        # dtype={"IDENTHOGAR": "string", "NORDENa": "string"},
    )
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) 
    load_csv_df()

    