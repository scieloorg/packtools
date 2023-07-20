# coding: utf-8
from lxml import etree as ET


def pipeline_pmc(xml_tree):
    xml_pmc_authors(xml_tree)
    xml_pmc_aff(xml_tree)
    xml_pmc_ref(xml_tree)

    return xml_tree


def xml_pmc_authors(xml_tree):
    authors = xml_tree.findall(".//contrib")
    for author in authors:
        contrib_id = author.find("./contrib-id")
        author.remove(contrib_id)
        label = author.find("./xref/sup")
        author.find("./xref").text = label.text
        author.find("./xref").remove(label)


