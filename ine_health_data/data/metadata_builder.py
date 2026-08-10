from pathlib import Path
import json
from openpyxl import Workbook, load_workbook, worksheet
import logging

wb = Workbook()

# Path for the original raw catalogue supplied from INE
RAW_ESdE_CATALOG_PATH = Path(r"data\raw\datos_2023\ESdEadulto_2023\dr_ESdEadulto_2023.xlsx")
# Path for the resulting json file
ESdE_MICRO_METADATA_PATH = Path(r"references\metadata\esde_adult_2023")


def read_raw_catalog(
    catalog:Path=RAW_ESdE_CATALOG_PATH
)->None:
    if not catalog.is_file():
        raise FileNotFoundError(f"Catalogo de variables no encontrado: {catalog}")

    wb = load_workbook(filename = catalog) # read_only=True would cause hyperlinks and merged cells to not work properly

    sheet_diseño:worksheet = wb['Diseño']
    extract_sheet_diseño(sheet_diseño)

    return

def extract_sheet_diseño(wsheet:worksheet):
    header_type_list = wsheet['A2':'J2'][0] # Select the only existing row

    dictionary_list:list[dict] = []
    variable_group:str|None = None

    for row in wsheet.iter_rows(min_row=3, max_row=7, min_col=1, max_col=12):
        row_map = {}

        for cell in row:
            if cell.column == 12:
                if cell.value is not None:
                    variable_group = cell.value

            elif cell.column <= len(header_type_list):
                value_type = header_type_list[cell.column - 1].value
                row_map[value_type] = cell.value

            # Col 11 stores URL about explanation of the statistic parameter... Not used for now in the project. 
            # elif cell.column == 11:
            #     row_map["URL_clasificacion"] = cell.value

        row_map["Grupo"] = variable_group
        dictionary_list.append(row_map)

    return 


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    read_raw_catalog()

    for map in dictionary_list:
        logging.info(map)
