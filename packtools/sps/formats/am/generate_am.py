import json
import logging
from pathlib import Path
from typing import Optional

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import am
from packtools.sps.exceptions import SPSLoadToXMLError


# Configura logger
logging.basicConfig(
    filename="generate_am.log",
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def load_json_data(path_str: Optional[str]) -> dict:
    if not path_str:
        return {}
    path = Path(path_str)
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def process_xml_file(
    xml_path: Path,
    external_data: dict
):
    try:
        xml_tree = xml_utils.get_xml_tree(str(xml_path))
        articlemeta = am.build(
            xml_tree=xml_tree,
            external_data=external_data
        )

        output_path = xml_path.with_suffix(".am.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(articlemeta, f, indent=2, ensure_ascii=False)

        print(f"[OK] Gerado: {output_path}")

    except Exception as exc:
        logging.error(f"Erro ao processar '{xml_path}': {exc}")
        print(f"[ERRO] Falha ao processar {xml_path.name}. Veja 'generate_am.log'.")


def is_leaf_directory(path: Path) -> bool:
    """Retorna True se a pasta não contiver subpastas."""
    return path.is_dir() and all(not p.is_dir() for p in path.iterdir())


def process_input_path(
    input_path_str: str,
    external_data_path: Optional[str] = None
):
    input_path = Path(input_path_str)
    if not input_path.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {input_path}")

    external_data = load_json_data(external_data_path)

    if input_path.is_file() and input_path.suffix.lower() == ".xml":
        process_xml_file(input_path, external_data)
    elif input_path.is_dir():
        leaf_dirs = [d for d in input_path.rglob("*") if is_leaf_directory(d)]
        xml_files = [f for d in leaf_dirs for f in d.glob("*.xml")]

        if not xml_files:
            print("[AVISO] Nenhum XML encontrado em pastas folha.")
        for xml_file in xml_files:
            process_xml_file(xml_file, external_data)
    else:
        raise ValueError("Entrada inválida: deve ser um arquivo .xml ou um diretório.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python generate_am.py <arquivo_ou_pasta> [external_article_data.json]")
        sys.exit(1)

    input_path = sys.argv[1]
    external_data_path = sys.argv[2] if len(sys.argv) > 2 else None

    process_input_path(input_path, external_data_path)
