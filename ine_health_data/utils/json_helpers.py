import json
import logging
from pathlib import Path
from typing import Any

def save_json(
    codebook: list[dict],
    output_path: Path,
) -> bool:
    # output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with output_path.open("w", encoding="utf-8") as json_file:
            json.dump(codebook, json_file, ensure_ascii=False, indent=2)
    except (OSError, TypeError) as error:
        logging.error("Could not write metadata JSON to %s: %s", output_path, error)
        return False

    logging.info("Wrote metadata JSON to %s", output_path)
    return True

def load_json(
    json_path: Path,
    encoding: str = "utf-8",
) -> Any:
    json_path = Path(json_path)
    if not json_path.is_file():
        raise FileNotFoundError(f"Metadata no encontrada: {json_path}")

    with json_path.open(encoding=encoding) as file:
        return json.load(file)
