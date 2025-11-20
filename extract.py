
"""
Expected .env content:
  KAGGLE_USERNAME=your_username
  KAGGLE_KEY=your_api_key
"""

from __future__ import annotations

import argparse
import os
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Optional


DEFAULT_DATASET = "kazanova/sentiment140"
DEFAULT_FILE = "training.1600000.processed.noemoticon.csv"


def load_env_file_if_present(env_file: Path) -> Dict[str, str]:
    if not env_file.exists() or not env_file.is_file():
        return {}

    loaded: Dict[str, str] = {}
    with env_file.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                loaded[key] = value
    # Only set env vars if not already set
    for key, value in loaded.items():
        os.environ.setdefault(key, value)
    return loaded


def ensure_kaggle_credentials_present() -> None:
    username = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")

    kaggle_json_path = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_json_path.exists():
        return

    if not username or not key:
        raise RuntimeError(
            "Faltan credenciales de Kaggle. Configure KAGGLE_USERNAME y KAGGLE_KEY "
            "en su entorno o cree ~/.kaggle/kaggle.json. También puede suministrar un .env."
        )


def maybe_write_kaggle_json_from_env() -> Path | None:
    username = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")
    if not username or not key:
        return None

    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    kaggle_json_path = kaggle_dir / "kaggle.json"
    if not kaggle_json_path.exists():
        kaggle_json_path.write_text(
            f'{{"username":"{username}","key":"{key}"}}',
            encoding="utf-8",
        )
        kaggle_json_path.chmod(0o600)
        return kaggle_json_path
    return None


def download_single_file(dataset: str, file_name: str, output_dir: Path) -> Path:
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "El paquete 'kaggle' no está instalado. Instálelo con: pip install kaggle"
        ) from exc

    output_dir.mkdir(parents=True, exist_ok=True)

    tmp_dir_path = Path(tempfile.mkdtemp(prefix="kaggle_dl_", dir=str(output_dir)))
    try:
        api = KaggleApi()
        api.authenticate()

        api.dataset_download_file(
            dataset=dataset,
            file_name=file_name,
            path=str(tmp_dir_path),
            force=True,
            quiet=False,
        )

        destination = output_dir / file_name

        # Direct file path (most common case)
        direct_candidate = tmp_dir_path / file_name
        if direct_candidate.exists():
            shutil.move(str(direct_candidate), str(destination))
            return destination

        # If Kaggle delivered a zip, extract then move the exact file
        for zip_path in tmp_dir_path.rglob("*.zip"):
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp_dir_path)

        # Try again after extraction
        extracted_candidate = tmp_dir_path / file_name
        if extracted_candidate.exists():
            shutil.move(str(extracted_candidate), str(destination))
            return destination

        # Fallback: any match by name within tmp dir
        matches = list(tmp_dir_path.rglob(file_name))
        if matches:
            shutil.move(str(matches[0]), str(destination))
            return destination

        raise RuntimeError(
            f"No se pudo localizar el archivo '{file_name}' luego de la descarga."
        )
    finally:
        shutil.rmtree(tmp_dir_path, ignore_errors=True)


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Descarga solo el CSV del dataset de Kaggle (Sentiment140).")
    parser.add_argument(
        "--dataset",
        default=DEFAULT_DATASET,
        help=f"Slug del dataset de Kaggle (por defecto: {DEFAULT_DATASET})",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_FILE,
        help=f"Nombre del archivo a descargar (por defecto: {DEFAULT_FILE})",
    )
    parser.add_argument(
        "--output-dir",
        default=str(script_dir),
        help="Directorio de salida donde guardar el CSV descargado.",
    )
    parser.add_argument(
        "--create-kaggle-json",
        action="store_true",
        help="Crear ~/.kaggle/kaggle.json a partir de KAGGLE_USERNAME y KAGGLE_KEY si no existe.",
    )
    parser.add_argument(
        "--env-file",
        default="",
        help="Ruta a un archivo .env opcional con KAGGLE_USERNAME y KAGGLE_KEY.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    env_file_path = Path(args.env_file) if args.env_file else None
    if env_file_path:
        load_env_file_if_present(env_file_path)

    if args.create_kaggle_json:
        created = maybe_write_kaggle_json_from_env()
        if created:
            print(f"Archivo creado: {created}")

    ensure_kaggle_credentials_present()

    output_dir = Path(args.output_dir).resolve()

    print(f"Descargando archivo '{args.file}' del dataset '{args.dataset}' en: {output_dir}")
    downloaded_path = download_single_file(dataset=args.dataset, file_name=args.file, output_dir=output_dir)

    if downloaded_path.exists():
        print(f"CSV disponible: {downloaded_path}")
    else:
        print("Descarga finalizada, pero no se encontró el archivo esperado.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

