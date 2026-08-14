"""..."""

import logging
from zipfile import ZipFile
from pathlib import Path

def extract_zip(
    zip_path: Path,
    output_dir: Path | None = None,
) -> Path:
    
    output_dir:Path = zip_path.parent if output_dir is None else Path(output_dir)

    if not zip_path.is_file(): raise FileNotFoundError(f"Microdata archive not found: {zip_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir_resolved = output_dir.resolve()

    with ZipFile(zip_path) as archive:
        for member in archive.infolist():
            target = (output_dir / member.filename).resolve()
            if not target.is_relative_to(output_dir_resolved):
                raise ValueError(f"Unsafe path in archive {zip_path}: {member.filename}")

        archive.extractall(output_dir)

    logging.info("Extracted %s into %s", zip_path.name, output_dir)
    return output_dir

def extract_all_raw_files(
    raw_dir: Path,
    output_dir: Path | None = None,
) -> list[Path]:
    r"""
    Extracts every zip file in `data\raw\` iteratively, including nested files, inside the
    same path location. 

    Accepts other output locations with `output_dir`.
    """

    output_dir:Path = raw_dir if output_dir is None else Path(output_dir)

    if not raw_dir.is_dir(): raise FileNotFoundError(f"Raw data directory not found: {raw_dir}")

    extracted: list[Path] = []
    processed: set[Path] = set()

    while True:
        # TODO: possibly add extracted check to avoid re-extraction
        archives = [archive for archive in raw_dir.rglob("*.zip") if archive not in processed]

        if not archives:
            return extracted

        for archive in archives:
            relative_parent = archive.parent.relative_to(raw_dir)
            archive_output_dir = output_dir / relative_parent / archive.stem

            extracted_path = extract_zip(archive, archive_output_dir)
            processed.add(archive)
            extracted.append(extracted_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_all_raw_files()
