import argparse

from packtools.sps.formats import pmc
from packtools.sps.utils import xml_utils


def main():
    parser = argparse.ArgumentParser(
        description="Convert XML file from SciELO format to PMC format."
    )
    parser.add_argument(
        "-i",
        "--xml_scielo",
        action="store",
        dest="xml_scielo",
        required=True,
        help="XML file in SciELO format to be converted.",
    )
    parser.add_argument(
        "-o",
        "--xml_pmc",
        action="store",
        dest="path_to_write",
        required=True,
        help="Path for writing the PMC XML file.",
    )
    arguments = parser.parse_args()

    xml_tree = xml_utils.get_xml_tree(arguments.xml_scielo)
    xml_string = pmc.pipeline_pmc(xml_tree)

    with open(arguments.path_to_write, "w", encoding="utf-8") as file:
        file.write(xml_string)
        print(f"Arquivo criado em: {arguments.path_to_write}")


if __name__ == "__main__":
    main()
