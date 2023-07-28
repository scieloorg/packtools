# coding: utf-8
from lxml import etree as ET


def pipeline_pmc(xml_tree):
    xml_pmc_aff(xml_tree)
    xml_pmc_ref(xml_tree)

    return xml_tree


def xml_pmc_aff(xml_tree):
    affs = xml_tree.findall(".//aff")
    for aff in affs:
        aff_institution = aff.find("./institution[@content-type='original']").text

        for institution in aff.findall(".//institution"):
            aff.remove(institution)

        aff.remove(aff.find('./addr-line'))

        aff.remove(aff.find("./country"))

        node_label = aff.find("./label")

        if node_label is not None:
            node_label.tail = aff_institution
        else:
            aff.text = aff_institution


def xml_pmc_ref(xml_tree):
    refs = xml_tree.findall(".//ref")
    for ref in refs:
        ref.remove(ref.find("./mixed-citation"))

