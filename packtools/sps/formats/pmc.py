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


def xml_pmc_aff(xml_tree):
    affs = xml_tree.findall(".//aff")
    for aff in affs:
        aff_label = aff.find("./label").text
        aff_intitution = aff.find("./institution[@content-type='original']").text

        aff.remove(aff.find("./label"))

        for institution in aff.findall(".//institution"):
            aff.remove(institution)

        aff.remove(aff.find('./addr-line'))

        aff.remove(aff.find("./country"))

        aff_el = ET.Element('label')
        aff_el.text = aff_label
        aff.insert(0, aff_el)

        aff.text = aff_intitution


def xml_pmc_ref(xml_tree):
    refs = xml_tree.findall(".//ref")
    for ref in refs:
        ref.remove(ref.find("./mixed-citation"))

