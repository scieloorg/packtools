import argparse
from lxml import etree as ET
import xml.dom.minidom as minidom

from packtools.sps.formats import crossref
from packtools.sps.utils import xml_utils


def main():
    parser = argparse.ArgumentParser(description='Convert XML file in SciELO format to CrossRef format.')
    parser.add_argument('-i', '--path to xml file in scielo format', action='store', dest='path_to_read', required=True,
                        help='Path for reading the SciELO XML file.')
    parser.add_argument('-n', '--depositor name', action='store', dest='depositor_name', required=False,
                        help='Value of the depositor name attribute.')
    parser.add_argument('-e', '--depositor email address', action='store', dest='depositor_email_address', required=False,
                        help='Value of the depositor email address attribute.')
    parser.add_argument('-r', '--registrant', action='store', dest='registrant', required=False,
                        help='Value of the registrant attribute.')
    parser.add_argument('-o', '--path to xml file in crossref format', action='store', dest='path_to_write', required=True,
                        help='Path for writing the CrossRef XML file.')
    arguments = parser.parse_args()

    data = {
        'depositor_name': arguments.depositor_name,
        'depositor_email_address': arguments.depositor_email_address,
        'registrant': arguments.registrant
    }

    xml_tree = xml_utils.get_xml_tree(arguments.path_to_read)
    xml_crossref = ET.ElementTree(crossref.pipeline_crossref(xml_tree, data))
    xml_string = ET.tostring(xml_crossref, encoding="utf-8")
    xml_crossref_formated = minidom.parseString(xml_string).toprettyxml(indent="  ")

    with open(arguments.path_to_write, "w", encoding="utf-8") as file:
        file.write(xml_crossref_formated)


if __name__ == '__main__':
    main()
