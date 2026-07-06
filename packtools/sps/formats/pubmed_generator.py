import argparse
import sys

from packtools.sps.formats import pubmed
from packtools.sps.utils import xml_utils


def main():
    parser = argparse.ArgumentParser(
        description="Convert XML file from SciELO format to Pubmed format."
    )
    parser.add_argument(
        "-i",
        "--xml_scielo",
        action="store",
        dest="path_to_read",
        required=True,
        help="Path for reading the SciELO XML file.",
    )
    parser.add_argument(
        "-o",
        "--xml_pubmed",
        action="store",
        dest="path_to_write",
        required=True,
        help="Path for writing the PubMed XML file.",
    )
    arguments = parser.parse_args()

    xml_tree = xml_utils.get_xml_tree(arguments.path_to_read)
    try:
        xml_pubmed = pubmed.pipeline_pubmed(xml_tree)
    except pubmed.MissingRequiredPubDateError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        raise SystemExit(1)

    with open(arguments.path_to_write, "w", encoding="utf-8") as file:
        file.write(xml_pubmed)
        print(f"Arquivo criado em: {arguments.path_to_write}")


if __name__ == "__main__":
    main()
